import traceback
from itertools import chain

from mal_types import (
    MalHashMap, MalTypes,
    MalSymbol,
    MalList, MalVector,
    mal_string, mal_symbol,
    mal_list, mal_vector, mal_hash_map,
    ReplFunc, ReplEnv,
)
from reader import read_str
from printer import pr_str


def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)


def READ(string: str) -> MalTypes:
    return read_str(string)


def eval_ast(ast: MalTypes, env: ReplEnv) -> MalTypes:
    if isinstance(ast, MalSymbol):
        try:
            return env[ast]
        except KeyError:
            raise Exception(f"'{ast}' not found")
    elif isinstance(ast, (MalList, MalVector)):
        gen = (EVAL(e, env) for e in ast)
        if isinstance(ast, MalList):
            return mal_list(*gen)
        elif isinstance(ast, MalVector):
            return mal_vector(*gen)
    elif isinstance(ast, MalHashMap):
        gen = (
            (mal_string(k), EVAL(v, env))
            for k, v in ast.items()
        )
        hm = mal_hash_map(*flatten(gen))
        return hm
    else:
        return ast


def EVAL(ast, env: ReplEnv) -> MalTypes:
    if not isinstance(ast, MalList):
        return eval_ast(ast, env)
    if ast.is_empty():
        return ast
    res = eval_ast(ast, env)
    if not isinstance(res, MalList):
        raise Exception(f"it must be MalList")
    func: ReplFunc = res[0]
    return func(*res[1:])


def PRINT(exp: MalTypes) -> str:
    return pr_str(exp)


repl_env: ReplEnv = {
    mal_symbol('+'): lambda a, b: a+b,
    mal_symbol('-'): lambda a, b: a-b,
    mal_symbol('*'): lambda a, b: a*b,
    mal_symbol('/'): lambda a, b: int(a/b),
}


def REP(line):
    ast = READ(line)
    res = EVAL(ast, repl_env)
    return PRINT(res)


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
        print("".join(traceback.format_exc()))
