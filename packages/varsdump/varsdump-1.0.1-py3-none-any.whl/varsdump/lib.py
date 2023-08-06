import builtins
import pprint
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter


def varsdump(variable) -> None:
    """
    :param variable:
    :return:
    """
    print(
        highlight(
            pprint.PrettyPrinter(indent=2).pformat(variable),
            PythonLexer(),
            TerminalFormatter()
        )
    )

builtins.var_dump = var_dump
