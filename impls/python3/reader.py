from re import compile as re_compile

from mal_types import (
    MalHashMap, MalList, MalVector, MalSequence,
    mal_int,
    mal_hash_map, mal_list, mal_vector,
    mal_symbol,
)


class Reader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self) -> str:
        token = self.peek()
        self.position += 1
        return token

    def peek(self) -> str:
        return self.tokens[self.position]


def tokenize(string: str) -> list:
    token_re = re_compile(r'''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}()'"`,;]*)''')
    return [token for token in token_re.findall(string)]


def read_sequence(
    reader: Reader,
    type_func: MalSequence = mal_list,
    start='(',
    end=')',
) -> list:
    token = reader.next()
    # if token != start:
    #     raise Exception("excepted '{start}'")

    ast = type_func()
    token = reader.peek()
    while token != end:
        if not token:
            raise Exception(f"excepted '{end}', got EOF")
        ast.append(read_form(reader))
        token = reader.peek()
    reader.next()
    return ast


def read_hash_map(reader: Reader) -> MalHashMap:
    list_ = read_sequence(reader, list, '{', '}')
    return mal_hash_map(*list_)


def read_list(reader: Reader) -> MalList:
    return read_sequence(reader, mal_list)


def read_vector(reader: Reader) -> MalVector:
    return read_sequence(reader, mal_vector, '[', ']')


def read_atom(reader: Reader):
    int_re = re_compile(r'-?[0-9]+')
    # float_re = re_compile(r'-?[0-9][0-9.]*')
    string_re = re_compile(r'"(:?[\\].|[^\\"])*"')
    token = reader.next()
    if int_re.match(token):
        return mal_int(token)
    # elif float_re.match(token):
    #     return float(token)
    elif string_re.match(token):
        return token[1:-1]
    elif token[0] == '"':
        raise Exception("excepted '\"', got EOF")
    elif token == 'nil':
        return None
    elif token == 'true':
        return True
    elif token == 'false':
        return False
    else:
        return mal_symbol(token)


def read_form(reader: Reader):
    token = reader.peek()
    # comment
    if token[0] == ';':
        reader.next()
        return None

    # ?
    elif token == '\'':
        reader.next()
        return mal_list(mal_symbol('quote'), read_form(reader))
    elif token == '`':
        reader.next()
        return mal_list(mal_symbol('quasiquote'), read_form(reader))
    elif token == '~':
        reader.next()
        return mal_list(mal_symbol('unquote'), read_form(reader))
    elif token == '~@':
        reader.next()
        return mal_list(mal_symbol('splice-unquote'), read_form(reader))
    # meta よくわからん
    # elif token == '^':
    #     reader.next()
    #     meta = read_form(reader)
    #     return mal_list(mal_symbol('with-meta'), read_form(reader), meta)
    elif token == '@':
        reader.next()
        return mal_list(mal_symbol('deref'), read_form(reader))

    # sequence
    elif token == '{':
        return read_hash_map(reader)
    elif token == '(':
        return read_list(reader)
    elif token == '[':
        return read_vector(reader)

    # atom
    else:
        return read_atom(reader)


def read_str(string: str):
    tokens = tokenize(string)
    reader = Reader(tokens)
    ast = read_form(reader)
    return ast
