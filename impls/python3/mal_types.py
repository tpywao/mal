# from typing import Union
from collections import UserDict, UserList


class MalType:
    pass


class MalInt(MalType, int):
    pass


def mal_int(val):
    return MalInt(val)


# Sequence
class MalSequence(MalType):
    start = '('
    end = ')'


class MalHashMap(MalSequence, UserDict):
    start = '{'
    end = '}'


def mal_hash_map(*key_vals):
    kvs = zip(key_vals[::2], key_vals[1::2])
    return MalHashMap(kvs)


class MalList(MalSequence, UserList):
    pass


def mal_list(*vals):
    return MalList(vals)


class MalVector(MalSequence, UserList):
    start = '['
    end = ']'


def mal_vector(*vals):
    return MalVector(vals)


# Symbol
class MalSymbol(MalType, str):
    pass


def mal_symbol(string):
    return MalSymbol(string)
