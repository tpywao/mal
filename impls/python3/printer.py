from itertools import chain

from mal_types import MalSequence, MalHashMap


def pr_str(ast):
    type_ = type(ast)
    if MalSequence in type_.mro():
        s = type_.start
        if type_ is MalHashMap:
            ret = chain.from_iterable(
                (pr_str(k), pr_str(v))
                for k, v in ast.items()
            )
            s += ' '.join(ret)
        else:
            s += ' '.join(map(lambda e: pr_str(e), ast))
        s += type_.end
        return s
    elif type_ is str:
        return f'"{ast}"'
    elif ast is None:
        return 'nil'
    elif ast is True:
        return 'true'
    elif ast is False:
        return 'false'
    else:
        # int, symbol
        return ast.__str__()
