


# A list of keywords that are used in the language.
keywords = (
    'let', 'var', 'func', 'for', 'return', 'if', 'else', 'and', 'or', 'while', 'repeat'
)

# A list of tokens that the lexer will recognize.
tokens = keywords + (
    'equals', 'equals_equals', 'plus', 'minus', 'divide', 'multiply', 'int_type', 'boolean_type', 'string_type',
    'array', 'int', 'bool'
    , 'id', 'semicolon', 'rparent', 'lparent', 'lt', 'le', 'gt', 'Void',
    'ge', 'arrow', 'rcparent', 'lcparent', 'lsparent', 'rsparent', 'ddot', 'comma', 'add', 'sub', 'not_equal', 'divby',
    'mulby',
    'question_mark', 'quote', 'exclamation_mark'
)

reserved_set = set(tokens)

reserved_map = {}
for r in tokens:
    reserved_map[r.lower()] = r


def t_comment(t):
    r'\/\/.*'
    pass


def t_Int(t):
    r'Int'
    t.type = reserved_map.get(t.value, "int_type")
    return t


def t_Boolean(t):
    r'Boolean'
    t.type = reserved_map.get(t.value, "boolean_type")
    return t


def t_String(t):
    r'String'
    t.type = reserved_map.get(t.value, "string_type")
    return t


def t_Array(t):
    r'Array'
    t.type = reserved_map.get(t.value, "array")
    return t


def t_OR(t):
    r'\|\|'
    t.type = reserved_map.get(t.value, "or")
    return t


def t_AND(t):
    r'&&'
    t.type = reserved_map.get(t.value, "and")
    return t


def t_bool(t):
    r'true|false'
    return t


def t_Void(t):
    r'Void'
    return t


# chytam identifikatory
# pokud je identifikator klicove slovo, zachyt to do typu
def t_id(t):
    r'[A-Za-z][A-Za-z0-9\_]*'
    if t.value in reserved_set:
        t.type = t.value
    return t


# token newline -> inkrementuj line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# neznamy token, zahlas chybu
def t_error(t):
    print(f"Syntax error: '{t.value[0]}' at {t.lineno}")


# zadefinuj token jako funkci - umozni k tomu pribalit nejaky vykonny kod
def t_int(t):
    r'\-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Number {t.value} is not integer.")
        t.lexer.skip(1)
    return t


# Defining the tokens that the lexer will recognize.
t_equals = r'='
t_equals_equals = r'=='
t_add = r'\+='
t_sub = r'\-='
t_divby = r'\/='
t_mulby = r'\*='
t_plus = r'\+'
t_minus = r'\-'
t_divide = r'\/'
t_multiply = r'\*'
t_semicolon = r'\;'
t_lparent = r'\('
t_rparent = r'\)'
t_lt = r'\<'
t_not_equal = r'!='
t_le = r'\<\='
t_gt = r'\>'
t_ge = r'\>\='
t_arrow = r'\-\>'
t_rcparent = r'\}'
t_lcparent = r'\{'
t_lsparent = r'\['
t_rsparent = r'\]'
t_ddot = r'\:'
t_comma = r'\,'
t_question_mark = r'\?'
t_quote = r'\"'
t_exclamation_mark = r'\!'
# Telling the lexer to ignore spaces and tabs.
t_ignore = " \t"
