import inspect

from termkit.options import Option


def command_format(id: str):
    return id.replace('_', '-').lower()


def get_help(item, single_line=False, is_flag_argument=False):
    if item.__class__.__name__ == "Termkit":
        doc = item.description
    elif inspect.isfunction(item):
        doc = inspect.getdoc(item)
    elif isinstance(item, inspect.Parameter):
        default_type = item.annotation if not issubclass(item.annotation, inspect.Parameter.empty) else str
        if is_flag_argument:
            doc = "(default: %(default)s)"
        else:
            doc = f'{default_type.__name__.upper()}'
            doc = "STRING" if doc == "STR" else doc
    elif isinstance(item, Option):
        doc = ' '
    else:
        doc = ' '

    if doc in [None, ""]:
        doc = ' '

    if single_line and len(doc.splitlines()) > 1:
        return doc.splitlines()[0].strip()
    return doc.strip()
