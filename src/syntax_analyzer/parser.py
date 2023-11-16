

from ete3 import Tree

from src.lex_analyzer.lexer import tokens
from src.syntax_analyzer.utils import make_node,is_integer,get_integer_node_value



# set priority of operations - plus minus multiply and divide will branch out the tree to the left
# the cfg is ambiguous, therefore precedence must be defined
precedence = (
    ('nonassoc', 'lt', 'gt', 'le', 'ge', 'equals_equals','and','or'),
    ('left', 'plus', 'minus', 'var', 'let','id'),
    ('left', 'multiply', 'divide'),
    ('left','lparent'),
    ('right', 'uminus'),
)


# entry point of program, the 'root' of the tree
def p_program(p):
    """program : dekl_list"""
    root = Tree(name='program')
    root.add_child(p[1])
    p[0] = root


# program is just a bunch of declaration statements, this is the core of the grammar
# declartion can produce functions, variables and general expressions, such as function calls or math expressions
def p_dekl_list(p):
    """
    dekl_list : dekl
              | expression semicolon
              | var_modification semicolon
              | var_modification semicolon dekl_list
              | dekl dekl_list
              | block
    """
    n = len(p)
    # block or single declaration
    if n == 2:
        p[0] = make_node('declaration', [p[1]],lineno=p.lexer.lineno)
    # modification of existing variable
    elif n == 4:
        p[0] = make_node('var_modification_dekl', [p[1], p[3]],lineno=p.lexer.lineno)
    # expression, modification or declaration list
    elif n == 3:
        # expression or modification
        if p[2] == ";":
            p[0] = make_node('statement', [p[1]],lineno=p.lexer.lineno)
        # declaration list
        else:
            p[0] = make_node('declaration_list', [p[1], p[2]],lineno=p.lexer.lineno)

def p_var_modification_error(p):
    """
     var_modification : id sub error
                     | id add error
                     | id mulby error
                     | id divby error
                     | id equals error
                     | id lsparent int rsparent equals error
    """
    raise Exception(f"Error on line {p.lexer.lineno}. Syntax error in modification of variable {p[1]}. Bad expression.")
# modification of existing variable
def p_var_modification(p):
    """
    var_modification : id sub expression
                     | id add expression
                     | id mulby expression
                     | id divby expression
                     | id equals expression
                     | id lsparent int rsparent equals expression
    """
    if len(p) == 4:
        p[0] = make_node("var_modification", [p[1], p[2], p[3]],lineno=p.lexer.lineno)
    elif len(p) == 7:
        p[0] = make_node("array_var_modification",[p[1],p[3],p[5],p[6]],lineno=p.lexer.lineno)

def p_dekl_error(p):
    """
    dekl : var error
    |      let error
    |       error
    """
    if len(p) == 3:
        raise Exception(f"Error on line {p.lexer.lineno}. "
                        f"Syntax error in variable declaration. Bad expression.")
    elif len(p) == 2:
        raise Exception(
            f"Error on line {p.lexer.lineno}. Syntax error in function declaration of variable {p[1]}. Bad expression.")


# declaration statement
# here we declare variable, constant or a function
def p_dekl(p):
    """
    dekl :   var var_dekl
    | let var_dekl
    | fun_dekl
    """

    if len(p) == 2:
        p[0] = make_node('function_declaration', [p[1]],lineno=p.lexer.lineno)
    elif len(p) == 3:
        p[0] = make_node('variable_declaration', [p[1], p[2]],lineno=p.lexer.lineno)

def p_var_dekl_error(p):
    """
    var_dekl : id ddot error equals error semicolon
    """
    if len(p) == 7:
        raise Exception(
            f"Error on line {p.lexer.lineno}. Syntax error in variable declaration '{p[1]}'.")
    else:
        raise Exception(
            f"Error on line {p.lexer.lineno}. Syntax error in variable declaration '{p[1]}'. Unknown data type {p[3].value}")


# This function is used to declare a variable.
def p_var_dekl(p):
    """
    var_dekl : id ddot dtype equals expression semicolon
    """
    if len(p) == 7:
        p[0] = make_node('var_declaration_expression', [p[1], p[3], p[5]],lineno=p.lexer.lineno)

def p_dtype_error(p):
    """
    dtype : error
    """
    raise Exception(f"Error on line {p.lexer.lineno}. Unknown data type '{p[1].value}'.")
# data type, can be expanded in the future, so far our language accepts only integers and booleans
def p_dtype(p):
    """
    dtype : int_type
    | boolean_type
    | array_dekl
    | string_type
    """
    p[0] = make_node('data_type', [p[1]],lineno=p.lexer.lineno)

def p_array_dekl(p):
    """
    array_dekl : array lparent int rparent
    """
    p[0] = make_node("array_type",[p[1],p[3]])


def p_expression_error(p):
    """
    expression : error minus error
    |            error plus error
    |            error
    """
    raise Exception(f"Error on line {p.lexer.lineno}. Bad expression. ")
# general expression - math expressions, variable assignments, functions calls, ...
def p_expression(p):
    """
    expression : expression minus term
    | expression plus term
    | term
    | ternary
    """
    if len(p) == 2:
        p[0] = make_node('expression_term', [p[1]],lineno=p.lexer.lineno)
    elif p[2] == '+':
        if is_integer(p[1]) and is_integer(p[3]):
            p[0] = make_node('const_expression_term',[get_integer_node_value(p[1])+get_integer_node_value(p[3])],lineno=p.lexer.lineno)
        else:
            p[0] = make_node('expression_sum', [p[1], p[3]],lineno=p.lexer.lineno)
    elif p[2] == '-':
        if is_integer(p[1]) and is_integer(p[3]):
            p[0] = make_node('const_expression_term', [get_integer_node_value(p[1]) - get_integer_node_value(p[3])],lineno=p.lexer.lineno)
        else:
            p[0] = make_node('expression_minus', [p[1], p[3]],lineno=p.lexer.lineno)

def p_ternary_error(p):
    """
    ternary : error question_mark error ddot error
    """
    raise Exception(f"Error on line {p.lexer.lineno}. Error in ternary operator.")

def p_ternary(p):
    """
    ternary : condition question_mark expression ddot expression
    """
    p[0] = make_node("ternary_operator",[p[1],p[3],p[5]],lineno=p.lexer.lineno)

def p_term_error(p):
    """
    term : error multiply error
    |      error divide error
    |       error
    """
    if len(p) == 2:
        raise Exception(f"Error on line {p.lexer.lineno}. Unknown value {p[1].value}")
    raise Exception(f"Error on line {p.lexer.lineno}. Expression contains an error.")
def p_term(p):
    """
    term : term multiply factor
    |  term divide factor
    | factor
    """
    if len(p) == 2:
        p[0] = make_node('factor', [p[1]],lineno=p.lexer.lineno)
    elif p[2] == '*':
        #pokud jsou to cisla, zvladnu to vyhodnotit pri prekladu
        if is_integer(p[1]) and is_integer(p[3]):
            p[0] = make_node('const_expression_term',[get_integer_node_value(p[1]) * get_integer_node_value(p[3])],lineno=p.lexer.lineno)
        #inak nemam tucha, co to je za vysledek
        else:
            p[0] = make_node('expression_multiply', [p[1], p[3]],lineno=p.lexer.lineno)
    elif p[2] == '/':
        if is_integer(p[1]) and is_integer(p[3]):
            p[0] = make_node('const_expression_term', [get_integer_node_value(p[1]) // get_integer_node_value(p[3])],lineno=p.lexer.lineno)
        else:
            p[0] = make_node('expression_divide', [p[1], p[3]],lineno=p.lexer.lineno)

def p_factor_error(p):
    """
    factor : lparent error rparent
    |       minus error %prec uminus
    |       error
    """
    if len(p) == 4:
        raise Exception(f"Error on line {p.lexer.lineno}. Expression '{p[2].value}' contains an error.")
    elif len(p) == 3:
        raise Exception(f"Error on line {p.lexer.lineno}. Unary minus operation contains an error '{p[2].value}'")
    raise Exception(f"Error on line {p.lexer.lineno}. Invalid value of expression '{p[1].value}'")

def p_factor(p):
    """
    factor : lparent expression rparent
    | minus expression %prec uminus
    | val
    | call
    """
    if len(p) == 4:
        p[0] = make_node('expression_in_parent', [p[2]],lineno=p.lexer.lineno)
    elif len(p) == 3:
        if is_integer(p[2]):
            p[0] = make_node('const_expression_term',[-get_integer_node_value(p[2])],lineno=p.lexer.lineno)
        else:
            p[0] = make_node('unary_minus', [p[1], p[2]],lineno=p.lexer.lineno)
    elif len(p) == 2:
        p[0] = make_node('factor_expression', [p[1]],lineno=p.lexer.lineno)


# empty rule, do nothing
def p_empty(p):
    """empty : """
    pass

def p_call_errr(p):
    """
    call : id lparent error rparent
    """
    raise Exception(f"Error on line {p.lexer.lineno}. Arguments '{p[3]}' contain an error.")
# function call rule, tree make_node stores operation and value
# value contains id of called function and function arguments
def p_call(p):
    """
    call : id lparent arguments rparent
    """
    p[0] = make_node('function_call', [p[1], p[3]],lineno=p.lexer.lineno)

def p_val_err(p):
    """
    val : error
    |   quote error quote
    |    lsparent error rsparent

    """
    if len(p) == 1:
        raise Exception(f"Error on line {p.lexer.lineno}. Value '{p[1].value}' in expression is invalid.")
    if p[1] == '"':
        raise Exception(f"Error on line {p.lexer.lineno}. String value {p[2].value} is invalid.")
    else:
        raise Exception(f"Error on line {p.lexer.lineno}. Integer array contains an error.")

# value assignment is integer
def p_val_num(p):
    """
    val : int
    """
    # vim, ze mi prisel int, castnu to ze stringu na int
    try:
        value = int(p[1])
    except OverflowError:
        print("Out of bounds")
        value = 0
    p[0] = make_node('var_value', [value],lineno=p.lexer.lineno)

def p_val_bool(p):
    """
    val : bool
    """
    boolean_val = 1 if p[1] == "true" else 0
    p[0] = make_node('var_value_boolean', [ boolean_val ],lineno=p.lexer.lineno)

# value assignment is an identifier
def p_val_id(p):
    """
    val : id
    """
    p[0] = make_node('var_value_identifier', [ p[1] ],lineno=p.lexer.lineno)
def p_val_string(p):
    """
    val : quote id quote
    """
    p[0] = make_node("var_value_string",[p[2],len(p[2])],lineno=p.lexer.lineno)

def p_val_array(p):
    """
    val : lsparent integer_list rsparent
    """
    p[0] = make_node("array_value",[p[2]],lineno=p.lexer.lineno)
def p_integer_list(p):
    """
    integer_list : int comma integer_list
    |               int
    """
    if len(p) == 2:
        p[0] = make_node("integer_list_tail",[p[1]],lineno=p.lexer.lineno)
    elif len(p) == 4:
        p[0] = make_node("integer_list",[p[1],p[3]],lineno=p.lexer.lineno)
# rule for function declaration make_node contains operation and val, val contains the relevant information about
# function, such as name, params, body and return type 'fun_dekl : func id lparent params rparent arrow dtype
# comp_block'

def p_fun_dekl_error(p):
    """
    fun_dekl : func id lparent error rparent arrow error error
    """
    raise Exception(f"Error on line {p.lexer.lineno}. Declaration of function {p[2]} contains an error.")
def p_fun_dekl(p):
    """
    fun_dekl : func id lparent params rparent arrow dtype comp_block
    |          func id lparent params rparent arrow Void comp_block
    """
    p[0] = make_node('function_signature', [p[2], p[4], p[7], p[8]],lineno=p.lexer.lineno)

def p_params_error(p):
    """
    params : error
    """
    raise Exception(f" Error on line {p.lexer.lineno}. Parameters declaration contains an error.")
# rule for function parameters, ie (<this>)
def p_params(p):
    """
    params : params_var
    | empty
    """
    p[0] = make_node('params', [p[1]],lineno=p.lexer.lineno)

# function parameter declaration
# initial variable value set to 0
def p_params_var(p):
    """
    params_var : id ddot dtype comma params_var
               | id ddot dtype
    """
    if len(p) == 6:
        p[0] = make_node('parameters_declaration_list', [p[1], p[3], p[5]],lineno=p.lexer.lineno)
    elif len(p) == 4:
        p[0] = make_node('parameter_declaration', [p[1], p[3]],lineno=p.lexer.lineno)


# function arguments rule, multiple values separated by comma
def p_arguments(p):
    """
    arguments : val comma arguments
    |   val
    | empty
    """
    if len(p) == 4:
        p[0] = make_node('arguments_list', [p[1], p[3]],lineno=p.lexer.lineno)
    elif len(p) == 2:
        p[0] = make_node('argument', [p[1]],lineno=p.lexer.lineno)


# compound block rule, ie {<block>}
def p_comp_block(p):
    """
    comp_block : lcparent block rcparent
    """
    p[0] = make_node('compound_block', [p[2]],lineno=p.lexer.lineno)


# generic block statement rule
# je docela blbe napsane, ale refactor gramatiky se mi uplne delat nechce
def p_block(p):
    """
    block : comp_block dekl_list
        | loop_block dekl_list
        | cond_block dekl_list
        | let var_dekl dekl_list
        | var var_dekl dekl_list
        | var_modification semicolon dekl_list
        | expression semicolon dekl_list
        | return expression semicolon
        | loop_block
        | cond_block
        | let var_dekl
        | var var_dekl
        | expression semicolon
        | var_modification semicolon
    """
    n = len(p)
    if p[1] == 'return':
        p[0] = make_node('return_statement', [p[2]],lineno=p.lexer.lineno)
    elif n == 3 and p[2] != ';':
        p[0] = make_node('block', [p[1], p[2]],lineno=p.lexer.lineno)
    elif n == 4 and p[1] == "var" or p[1] == "let":
        p[0] = make_node('block_var_dekl', [p[1], p[2], p[3]],lineno=p.lexer.lineno)
    elif n == 4:
        p[0] = make_node('block_expression', [p[1], p[3]],lineno=p.lexer.lineno)
    elif n == 2 or (n == 3 and p[2] == ';'):
        p[0] = make_node('block_statement', [p[1]],lineno=p.lexer.lineno)


# loop statement, for / while cycle
def p_loop_block(p):
    """
    loop_block : for lparent loop_var condition semicolon step semicolon rparent comp_block
    |           while condition comp_block
    |           repeat comp_block while condition semicolon

    """
    if len(p) == 10:
        p[0] = make_node('for_loop_block', [p[3], p[4], p[6], p[9]],lineno=p.lexer.lineno)
    elif len(p) == 4:
        p[0] = make_node('while_loop_block', [p[2], p[3]],lineno=p.lexer.lineno)
    elif len(p) == 6:
        p[0] = make_node('repeat_loop_block', [p[2], p[4]],lineno=p.lexer.lineno)


# condition block, if or if else statement. Switch-case might be added in future
def p_cond_block(p):
    """
    cond_block : if lparent condition rparent comp_block
    |            if lparent condition rparent comp_block else comp_block
    """
    if len(p) == 8:
        p[0] = make_node('if_else_stmt', [p[3], p[5], p[7]],lineno=p.lexer.lineno)
    elif len(p) == 6:
        p[0] = make_node('if_stmt', [p[3], p[5]],lineno=p.lexer.lineno)


# loop variable responsible for loop behavior
def p_loop_var(p):
    """
    loop_var : var var_dekl
    | id semicolon
    """
    if p[2] != ";":
        p[0] = make_node('loop_var', [p[1], p[2]],lineno=p.lexer.lineno)
    else:
        p[0] = make_node('loop_var', [p[1]],lineno=p.lexer.lineno)


# step in for loop
def p_step(p):
    """
    step : id add int
    | id sub int
    """
    p[0] = make_node('loop_step', [p[1], p[2], p[3]],lineno=p.lexer.lineno)


# condition statement
def p_condition(p):
    """
    condition : expression relation_operator expression and condition
    |           expression relation_operator expression or condition
    |           exclamation_mark lparent condition rparent
    |           expression relation_operator expression
    |           val
    |           expression and condition
    |           expression or condition
    |           exclamation_mark lparent condition rparent and condition
    |           exclamation_mark lparent condition rparent or condition


    """
    if len(p) == 4 and (p[2] == "&&" or p[2] == "||"):
        p[0] = make_node("id_compound_condition",[p[1],p[2],p[3]],lineno=p.lexer.lineno)
    elif len(p) == 4:
        p[0] = make_node('condition', [p[1], p[2], p[3]],lineno=p.lexer.lineno)
    elif len(p) == 2:
        p[0] = make_node("simple_condition",[p[1]],lineno=p.lexer.lineno)
    elif len(p) == 6:
        p[0] = make_node('compound_condition',[p[1],p[2],p[3],p[4],p[5]],lineno=p.lexer.lineno)
    elif len(p) == 5:
        p[0] = make_node("negation_condition",[p[3]],lineno=p.lexer.lineno)
    elif len(p) == 7:
        p[0] = make_node("compound_negation_condition",[p[3],p[5],p[6]],lineno=p.lexer.lineno)




# This function is used to parse the relational operators in the input.
def p_relation_operator(p):
    """
    relation_operator : equals_equals
    | lt
    | gt
    | le
    | ge
    | not_equal
    """
    p[0] = make_node('relation_operator', [p[1]],lineno=p.lexer.lineno)


def p_error(p):
    if not p:
        print(f"syntax error {p}")
    raise Exception (f"Unrecognized token {p.value} on line {p.lineno}")
# for lparent loop_var condition semicolon step semicolon rparent
# y = yacc.yacc(debug=True)
# r = y.parse('func a() -> int {if (a<5){return 3;} return 10;}',lexer=lex)
# print(f" {r}")
