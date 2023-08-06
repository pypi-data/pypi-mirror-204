import json

from termkit._formatter import TermkitDefaultFormatter
from termkit.options import *
from termkit.options import __PROFILES__
from termkit._helpers import command_format, get_help


def get_filtered_args(arguments: argparse.Namespace):
    args = arguments.__dict__.copy()
    for k, v in args.copy().items():
        if k[:9] == '_Termkit_':
            del args[k]
    return args


def run(func: typing.Callable, with_named_profile=False, with_argcomplete=False):
    if inspect.isfunction(func):
        kit = Termkit(name=command_format(func.__name__),
                      description=get_help(func),
                      with_named_profile=with_named_profile,
                      with_argcomplete=with_argcomplete)
        kit._add_callback(func)
        kit._run()

    elif isinstance(func, Termkit):
        func._build_parser()
        func._run()


class Termkit:
    _callback: typing.Callable = None
    _cli: typing.Dict = None
    _named_profile: str = None

    _parser: argparse.ArgumentParser = None
    _formatter: argparse.HelpFormatter = TermkitDefaultFormatter
    _with_named_profile: bool
    _with_argcomplete: bool

    def __repr__(self):
        return json.dumps(self._cli, default=lambda o: f"<function {o.__name__}>" if inspect.isfunction(o) else o._cli,
                          indent=2)

    def __init__(self,
                 name: str = os.path.basename(sys.argv[0]),
                 description: str = None,
                 with_named_profile: bool = False,
                 with_argcomplete: bool = False,
                 formatter: argparse.HelpFormatter = TermkitDefaultFormatter):
        self.name = name
        self.description = description
        self._with_named_profile = with_named_profile
        self._with_argcomplete = with_argcomplete
        self._cli = dict()
        self._formatter = formatter

    def _setup_profile(self):
        parser = argparse.ArgumentParser(exit_on_error=False, add_help=False)
        self._build_parser(parser, add_help=False)
        args, unrecognized = parser.parse_known_args()
        self.profile = args.__dict__.get('profile', None)

    def _run(self):
        parser = self._build_parser()
        if self._with_argcomplete:
            import argcomplete
            argcomplete.autocomplete(parser)
        args = parser.parse_args()
        try:
            args.__CALLABLE(**get_filtered_args(args))
        except AttributeError:
            if self._callback is not None:
                self._callback(**get_filtered_args(args))
            else:
                parser.print_help()
        sys.exit(0)

    def _setup_named_profile_defaults(self):
        pass

    def __call__(self, *args, **kwargs):
        self._run()

    def callback(self) -> typing.Callable:
        def _decorator(func: typing.Callable):
            self._add_callback(func)

        return _decorator

    def add(self, term) -> None:
        self._cli.update({term.name: term})

    def command(self, name: str = None) -> typing.Callable:
        def _decorator(callback: typing.Callable, name: str = name):
            if name is None:
                name = callback.__name__
            self._cli.update({name: callback})

        return _decorator

    def default_handler(self, inspect_default):
        if isinstance(inspect_default, FromNamedProfile):
            print("FROM NAMED PROFILE", self.profile)
            if self.profile is not None:
                print('inspect_default: ', inspect_default)
                v = __PROFILES__.get(self.profile, {})
                for l in inspect_default.loc:
                    print(v, l)
                    if isinstance(v, dict):
                        v = v.get(l, {})
                    else:
                        v = v.get(l, inspect_default.if_unset)
                return v

            return inspect_default.if_unset

        else:
            return inspect_default

    def _build_parser(self, parser=None, level=0, add_help=True, positional_args=None, required_args=None,
                      optional_args=None):

        if self._with_named_profile and level:
            self._setup_profile()

        if parser is None:
            parser = argparse.ArgumentParser(prog=self.name, add_help=False,
                                             description=self.description,
                                             formatter_class=self._formatter)
            positional_args = parser.add_argument_group("Positional arguments")
            required_args = parser.add_argument_group("Required arguments")
            optional_args = parser.add_argument_group("Optional arguments")
            optional_args.add_argument("-h", "--help", action="help", help="show this help message and exit")

        if inspect.isfunction(self._callback):
            _populate(parser, '_callback', self._callback, positional_args, required_args, optional_args)

        if inspect.isfunction(self._cli):
            _populate(parser, "_cli", self._cli, positional_args, required_args, optional_args)

        if isinstance(self._cli, typing.Dict) and len(self._cli.keys()) > 0:
            _parser = parser.add_subparsers(title="commands")

            for c_name, c_spec in self._cli.items():
                p = _parser.add_parser(name=c_name, help=get_help(c_spec, single_line=True),
                                       description=get_help(c_spec),
                                       formatter_class=self._formatter, add_help=False)
                positional_args = p.add_argument_group("Positional arguments")
                required_args = p.add_argument_group("Required arguments")
                optional_args = p.add_argument_group("Optional arguments")
                optional_args.add_argument("-h", "--help", action="help", help="show this help message and exit")
                if isinstance(c_spec, Termkit):
                    c_spec._build_parser(parser=p, level=level + 1, add_help=add_help, positional_args=positional_args,
                                         required_args=required_args,
                                         optional_args=optional_args)
                    if self._with_named_profile:
                        optional_args.add_argument('--profile', help="Named Profile", dest="_Termkit__PROFILE",
                                                   required=False, default=None, )
                    continue

                _populate(p, c_name, c_spec, positional_args, required_args, optional_args)

        return parser

    def _add_callback(self, func: typing.Callable):
        self._callback = func


def _populate(parser, arg_name, arg_spec, positional_args, required_args, optional_args):
    if callable(arg_spec):
        parser.add_argument('--_Termkit__CALLABLE', help=argparse.SUPPRESS, default=arg_spec, required=False)

        signature = inspect.signature(arg_spec)

        for arg, spec in signature.parameters.items():
            if isinstance(spec.default, MutuallyExclusiveGroup):
                spec.default._populate(parser, arg)

            elif isinstance(spec.default, Choice):
                spec.default._populate(required_args, arg) if spec.default.required else spec.default._populate(
                    optional_args, arg)

            elif isinstance(spec.default, Option):
                if spec.default.required:
                    spec.default._populate(required_args, dest=arg)
                else:
                    spec.default._populate(optional_args, dest=arg)

            # Implicit arguments
            elif spec.default == signature.empty:
                default_type = spec.annotation if not issubclass(spec.annotation, inspect.Parameter.empty) else str
                positional_args.add_argument(arg, type=default_type, help=get_help(spec))
            else:
                default_type = spec.annotation if not issubclass(spec.annotation, inspect.Parameter.empty) else str
                optional_args.add_argument('--' + arg.replace('_', '-'), default=spec.default, type=default_type,
                                           required=False,
                                           help=get_help(spec, is_flag_argument=True), metavar=get_help(spec), dest=arg)
