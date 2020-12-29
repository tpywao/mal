import sys
import traceback


def READ(str):
    return str


def EVAL(ast):
    return ast


def PRINT(exp):
    return exp


def REP(str):
    return PRINT(EVAL(READ(str)))


while True:
    try:
        line = input('user> ')
        if line == '':
            continue
        print(REP(line))
    except KeyboardInterrupt:
        continue
    except EOFError:
        break
    except Exception:
        print("".join(traceback.format_exception(*sys.exc_info())))
