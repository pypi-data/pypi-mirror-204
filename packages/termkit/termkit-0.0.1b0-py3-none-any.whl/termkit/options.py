#!/usr/bin/env python

import argparse
import inspect
import typing
import os
import sys

__PROFILES__ = {
    "test": {
        "bamboo": {
            "name": "Overwrite"
        }
    }
}


class Choice:
    def __init__(self, *flags, choices: typing.List, help="", required=False, default=None):
        self.flags = flags
        self.help = help
        self.required = required
        self.default = default
        self.choices = choices

    def _get_metavar(self):
        if self.default is None:
            return "STRING"

        out = f"{type(self.default).__name__.upper()}"
        return "STRING" if out == "STR" else out

    def _get_default_type(self):
        return str if self.default is None else type(self.default)

    def get_help(self):
        if self.default is not None:
            return f"{self.help} (default: %(default)s)".strip()
        return self.help

    def _populate(self, parser: argparse.ArgumentParser, dest=None):
        parser.add_argument(*self.flags,
                            choices=self.choices,
                            metavar=self._get_metavar(),
                            type=self._get_default_type(),
                            default=self.default,
                            required=self.required,
                            help=self.get_help(),
                            dest=dest.strip())


class Option:
    def __init__(self, *flags, help="", required=False, default=None):
        self.flags = flags
        self.help = help
        self.required = required
        self.default = default

    def _get_metavar(self):
        if self.default is None:
            return "STRING"

        out = f"{type(self.default).__name__.upper()}"
        return "STRING" if out == "STR" else out

    def _get_default_type(self):
        return str if self.default is None else type(self.default)

    def get_help(self):
        if self.default is not None:
            return f"{self.help} (default: %(default)s)".strip()
        return self.help

    def _populate(self, parser: argparse.ArgumentParser, dest=None):
        parser.add_argument(*self.flags,
                            metavar=self._get_metavar(),
                            type=self._get_default_type(),
                            default=self.default,
                            required=self.required,
                            help=self.get_help(),
                            dest=dest.strip())


class MutuallyExclusiveGroup:

    def __init__(self, *args: Option, name=None, required=False):
        self.args = args
        self.name = name
        self.required = required

    def _populate(self, parser: argparse.ArgumentParser, group_name: str):
        if self.name is None:
            self.name = group_name

        if self.required:
            self.name += ' (required)'

        g_parser = parser.add_argument_group(self.name)
        parser._action_groups.pop()
        parser._action_groups.insert(0, g_parser)
        group = g_parser.add_mutually_exclusive_group(required=False)
        for option in self.args:
            option._populate(group, dest=group_name)


class FromNamedProfile:
    def __init__(self, *loc, if_unset: typing.Any):
        self.loc = loc
        self.if_unset = if_unset


class EBHelpFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog: str):
        super().__init__(prog, width=80, max_help_position=35)

    def _format_action(self, action):
        if type(action) == argparse._SubParsersAction:
            # inject new class variable for subcommand formatting
            subactions = action._get_subactions()
            invocations = [self._format_action_invocation(a) for a in subactions]
            self._subcommand_max_length = max(len(i) for i in invocations)

        if type(action) == argparse._SubParsersAction._ChoicesPseudoAction:
            # format subcommand help line
            subcommand = self._format_action_invocation(action)  # type: str
            width = self._subcommand_max_length
            help_text = ""
            if action.help:
                help_text = self._expand_help(action)

            if len(help_text) > 0:
                return "  {} {} {}\n".format(subcommand, "." * (width + 3 - len(subcommand)), help_text, width=width)
            else:
                return "  {}\n".format(subcommand, width=width)

        elif type(action) == argparse._SubParsersAction:
            # process subcommand help section
            msg = ''
            for subaction in action._get_subactions():
                msg += self._format_action(subaction)
            return msg
        else:
            return super(EBHelpFormatter, self)._format_action(action)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s' % option_string)
                parts[-1] += ' %s' % args_string
            return ', '.join(parts)

# app = Termkit("nxp-tools", help="General utility to interact with NXP Services")
#
# bamboo_app = Termkit("bamboo", help="Set of command related to Bamboo")
#
#
# @app.command()
# def test(count: int,
#          name: str = "test"):
#     """
#     Simple Hello world command
#     :param count:
#     :param name:
#     :return:
#     """
#     for e in range(count):
#         print(name)
#
#
# @bamboo_app.command()
# def test_2(profile: str = Option(flag="--profile"),
#            name: str = Option(flag="--name", default=FromNamedProfile("bamboo", "name", if_unset="Thomas")),
#            auth: typing.Any = MutuallyExclusiveGroup(Option(flag='--user'),
#                                                      Option(flag='--access-token'))):
#     print(f"{profile=}")
#     print(f"{name=}")
#
#
# @bamboo_app.command()
# def test_3(name: str = "test"):
#     """
#     Simple command
#     :param name:
#     :return:
#     """
#     print(name)
#
#
# app.add(bamboo_app)
#
# if __name__ == '__main__':
#     app()
