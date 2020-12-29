import sys
import traceback
from typing import Union

from mal_types import MalType
from reader import read_str
from printer import pr_str


def READ(string: str) -> Union[MalType, bool, None]:
    return read_str(string)


def EVAL(ast):
    return ast


def PRINT(exp):
    return pr_str(exp)


def REP(line):
    return PRINT(EVAL(READ(line)))


while True:
    try:
        line = input('user> ')
        if line == '':
            continue
        print(REP(line))
    except KeyboardInterrupt:
        print()
        continue
    except EOFError:
        break
    except Exception:
        print("".join(traceback.format_exception(*sys.exc_info())))
