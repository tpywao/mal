from collections import UserDict, UserList
from typing import Union, Callable, Dict


class MalType:
    pass


class MalInt(MalType, int):
    pass


def mal_int(val):
    return MalInt(val)


class MalString(MalType, str):
    pass


def mal_string(val):
    return MalString(val)


def mal_keyword(val):
    if val[0] == '\u029e':
        # it isn't keyword
        return MalString(val)
    else:
        return MalString('\u029e' + val)


def is_mal_keyword(val):
    return val[0] == '\u029e'


# Sequence
class MalSequence(MalType):
    start = '('
    end = ')'


class MalHashMap(MalSequence, UserDict):
    start = '{'
    end = '}'


def mal_hash_map(*key_vals) -> MalHashMap:
    kvs = zip(key_vals[::2], key_vals[1::2])
    return MalHashMap(dict(kvs))


class MalList(MalSequence, UserList):
    def is_empty(self):
        return len(self.data) == 0


def mal_list(*vals) -> MalList:
    return MalList(vals)


class MalVector(MalSequence, UserList):
    start = '['
    end = ']'


def mal_vector(*vals) -> MalVector:
    return MalVector(vals)


# Symbol
class MalSymbol(MalType, str):
    pass


def mal_symbol(string) -> MalSymbol:
    return MalSymbol(string)


ReplFunc = Callable[..., Union[MalType, bool, None]]
ReplEnv = Dict[MalSymbol, ReplFunc]
MalTypes = Union[MalType, ReplFunc, bool, None]
