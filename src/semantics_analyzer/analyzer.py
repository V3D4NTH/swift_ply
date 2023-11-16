# class responsible from semantic analysis

from src.syntax_analyzer.symbol_table import find_entry_in_symbol_table


class Analyzer:
    def __init__(self, dst, symbol_table):
        self.__dst = dst
        self.__symbol_table = symbol_table
        self.__visited_nodes = set()
        self.__var_types = {"let", "var"}
        self.__data_types = {"Int", "Boolean", "Array", "String"}
        # actual inception
        self.real_level = 0
        # global scope (0) or name of func
        self.level = 0
        # ret_statement_count in curr function max is 1
        self.ret_statement_count = 0
        # ret val type
        self.ret_value = None
        self.__subtree_leaf_dtype = None
        self.__subtree_leaf_value = None
        self.__identifier_table_entry = None
        self.__last_stmt_in_block = None

    # preorder tree traversal
    # build symbol table
    # check for semantics
    def Analyze(self) -> bool:
        root = self.__dst
        # traverse the tree, parent -> left subtree -> right subtree
        for node in root.traverse("preorder"):
            # subtree already visited
            if node in self.__visited_nodes:
                continue
            is_okay = self.__eval_node(node)
            if not is_okay:
                raise Exception("Program contains an error. Compilation to PL0 is not possible.")
        return True

    # method evaluates semantic "correctness" of tree node
    # if the node is not correct, False value is returned
    def __eval_node(self, node) -> bool:
        node_name = node.name
        subtree_okay = True
        if node_name == "variable_declaration":
            subtree_okay = self.__eval_var_declaration(node)
        elif node_name == "var_declaration_expression":
            subtree_okay = self.__eval_var_declaration_expression(node)
        elif node_name == "data_type":
            subtree_okay = self.__eval_data_type(node)
        elif node_name == "expression_term":
            subtree_okay = self.__eval_expression_term(node)
        elif node_name == "expression_multiply":
            subtree_okay = self.__eval_expression_multiply(node)
        elif node_name == "expression_sum":
            subtree_okay = self.__eval_expression_sum(node)
        elif node_name == "expression_minus":
            subtree_okay = self.__eval_expression_minus(node)
        elif node_name == "expression_divide":
            subtree_okay = self.__eval_expression_divide(node)
        elif node_name == "expression_in_parent":
            subtree_okay = self.__eval_expression_in_parenthesis(node)
        elif node_name == "factor_expression":
            subtree_okay = self.__eval_factor_expression(node)
        elif node_name == "factor":
            subtree_okay = self.__eval_factor(node)
        elif node_name == "function_call":
            subtree_okay = self.__eval_function_call(node)
        elif node_name == "var_value" or node_name == "var_value_boolean" or node_name == "var_value_string" or node_name == "var_value_identifier":
            subtree_okay = self.__eval_var_value(node)
        elif node_name == "function_declaration":
            subtree_okay = self.__eval_function_declaration(node)
        elif node_name == "params":
            subtree_okay = self.__eval_function_parameters(node)
        elif node_name == "function_signature":
            subtree_okay = self.__eval_function_signature(node)
        elif node_name == "compound_block":
            subtree_okay = self.__eval_comp_block(node)
        # [JT] names of all nodes whose children represent a block, either a function body, if/if-else body or loop body
        elif node_name == "block" or node_name == "block_var_dekl" or node_name == "block_expression" or node_name == "block_statement":
            subtree_okay = self.__eval_block(node)
        elif node_name == "for_loop_block":
            subtree_okay = self.__eval_for_loop_block(node)
        elif node_name == "loop_step":
            subtree_okay = self.__eval_loop_step(node)
        elif node_name == "loop_var":
            subtree_okay = self.__eval_loop_var(node)
        elif node_name == "condition":
            subtree_okay = self.__eval_condition(node)
        elif node_name == "compound_condition":
            subtree_okay = self.__eval_compound_condition(node)
        elif node_name == "simple_condition":
            subtree_okay = self.__eval_simple_condition(node)
        elif node_name == "id_compound_condition":
            subtree_okay = self.__eval_id_compound_condition(node)
        elif node_name == "compound_negation_condition":
            subtree_okay = self.__eval_compound_negation_condition(node)
        elif node_name == "var_modification":
            subtree_okay = self.__eval_var_modification(node)
        elif node_name == "array_var_modification":
            subtree_okay = self.__eval_array_var_modification(node)
        elif node_name == "if_stmt":
            subtree_okay = self.__eval_if_stmt(node)
        elif node_name == "if_else_stmt":
            subtree_okay = self.__eval_if_else_stmt(node)
        elif node_name == "return_statement":
            subtree_okay = self.__eval_return_statement(node)
        elif node_name == "ternary_operator":
            subtree_okay = self.__eval_ternary_operator(node)
        elif node_name == "while_loop_block":
            subtree_okay = self.__eval_while_statement(node)
        elif node_name == "repeat_loop_block":
            subtree_okay = self.__eval_repeat_statement(node)
        elif node_name == "unary_minus":
            subtree_okay = self.__eval_unary_minus(node)
        elif node_name == "negation_condition":
            subtree_okay = self.__eval_negation_condition(node)
        elif node_name == "const_expression_term":
            subtree_okay = True
        elif node_name == "array_var_modification":
            subtree_okay = self.__eval_array_var_modification(node)
        elif node_name == "array_value":
            subtree_okay = self.__eval_array_value(node)

        self.__mark_visited(node)
        return subtree_okay

    def __eval_array_value(self, node):
        children = node.get_children()
        int_list = children[0]
        int_count = 1
        while True:
            val = int_list.get_children()
            if len(val) == 1:
                break
            # value assigned to array index - can be only integer - no need to check it
            array_value = val[0]
            int_list = val[1]
            int_count += 1
        self.__subtree_leaf_value = int_count
        self.__subtree_leaf_dtype = "Array"
        return True

    def __eval_compound_negation_condition(self, node):
        lineno = node.lineno
        children = node.get_children()
        left_cond = children[0]
        right_cond = children[2]
        if not self.__eval_node(left_cond):
            raise Exception(
                f"Error on line {lineno}. Condition {self.__get_string_aprox_of_subtree(left_cond)} contains an error.")
        if not self.__eval_node(right_cond):
            leaves = left_cond.get_leaves()
            str = ""
            for i in range(leaves):
                str += leaves[i].str
            raise Exception(
                f"Error on line {lineno}. Condition {self.__get_string_aprox_of_subtree(right_cond)} contains an error.")

        return True

    def __eval_array_var_modification(self, node):
        lineno = node.lineno
        children = node.get_children()
        identifier = children[0].name
        index = children[1].name
        # if array assignment cannot be done for every operation (for some reason), we can catch it here
        operation = children[2].name
        expression = children[3]
        if not self.__find_identifier(identifier, lineno):
            raise Exception(f"Error on line {lineno}. Variable {identifier} on line {lineno} is not defined.")

        if self.__identifier_table_entry.size <= index:
            raise Exception(f"Error on line {lineno}. Array out of bounds. Index value {index} is too large. "
                            f"Lenght of array {identifier} is {self.__identifier_table_entry.size}.")

        if not self.__eval_node(expression):
            raise Exception(
                f"Error on line {lineno}. Expression {self.__get_string_aprox_of_subtree(expression)} contains an error. "
                f"That value cannot be assigned to array.")
        if self.__subtree_leaf_dtype != "Int":
            raise Exception(f"Error on line {lineno}. Only integers can be assigned to array {identifier}."
                            f" Array with values of type:  {self.__subtree_leaf_dtype} is not supported.")

        return True

    def __eval_id_compound_condition(self, node):
        lineno = node.lineno
        children = node.get_children()
        expr = children[0]
        condition = children[2]
        if not self.__eval_node(expr):
            raise Exception(
                f"Error on line {lineno} in condition. Expression {self.__get_string_aprox_of_subtree(expr)} contains an error.")
        if self.__subtree_leaf_dtype != "Boolean":
            raise Exception(f"Error on line {lineno} in condition. Only boolean values can be used in condition.")
        if not self.__eval_node(condition):
            raise Exception(
                f"Error on line {lineno}. Condition {self.__get_string_aprox_of_subtree(condition)} contains an error.")
        return True

    # only value in condition
    # the value must be an identifier
    # and the variable must be a boolean
    def __eval_simple_condition(self, node):
        lineno = node.lineno
        tmp = self.__subtree_leaf_value
        children = node.get_children()
        var_value = children[0]
        is_value_okay = self.__eval_node(var_value)
        if not is_value_okay:
            raise Exception(f"Error on line {lineno} in condition."
                            f" Expression: {self.__get_string_aprox_of_subtree(var_value)} contains an error.")
        if self.__subtree_leaf_dtype != "Boolean":
            raise Exception(f"Error on line {lineno} in condition. Only boolean values can be used in conditions.")
        self.__subtree_leaf_value = tmp
        return True

    def __eval_ternary_operator(self, node):
        lineno = node.lineno
        children = node.get_children()
        condition = children[0]
        expression_true = children[1]
        expression_false = children[2]

        is_condition_ok = self.__eval_node(condition)
        if not is_condition_ok:
            raise Exception(f"Error on line {lineno}."
                            f" Condition in ternary operator : {self.__get_string_aprox_of_subtree(condition)}"
                            f" contains an error.")
        is_true_exp_ok = self.__eval_node(expression_true)
        if not is_true_exp_ok:
            raise Exception(f"Error on line {lineno}."
                            f" Expression in ternary operator: {self.__get_string_aprox_of_subtree(expression_true)}"
                            f" on the left side contains an error.")
        if self.__check_if_is_function():
            raise Exception(
                f"Error on line {lineno}. Function call {self.__get_string_aprox_of_subtree(expression_true)}"
                f" cannot be used in ternary operator.")

        left_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        is_false_exp_ok = self.__eval_node(expression_false)
        if not is_false_exp_ok:
            print(f"Error on line {lineno}. Expression in ternary operator:"
                  f" {self.__get_string_aprox_of_subtree(expression_false)}"
                  f" on the right side contains an error.")
            return False
        if self.__check_if_is_function():
            raise Exception(
                f"Error on line {lineno}. Function call {self.__get_string_aprox_of_subtree(expression_true)}"
                f" cannot be used in ternary operator.")

        right_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if left_side_info[1] != right_side_info[1]:
            raise Exception(f"Error on line {lineno}. Type mismatch."
                            f" Both expressions of ternary operator must be of the same type.")
        return True

    def __eval_negation_condition(self, node):
        lineno = node.lineno
        children = node.get_children()
        condition = children[0]
        condition_ok = self.__eval_node(condition)
        if not condition_ok:
            raise Exception(f"Error on line {lineno}. Condition {self.__get_string_aprox_of_subtree(condition)} ")
        if self.__subtree_leaf_dtype != "Int" and self.__subtree_leaf_dtype != "Boolean":
            raise Exception(f"Error on line {lineno}. Negation is only defined for integers or booleans."
                            f" Got {self.__subtree_leaf_dtype}.")
        return True

    def __eval_expression_in_parenthesis(self, node):
        lineno = node.lineno
        children = node.get_children()
        expression = children[0]
        is_expression_okay = self.__eval_node(expression)
        if not is_expression_okay:
            raise Exception(
                f"Error on line {lineno}. Expression: {self.__get_string_aprox_of_subtree(expression)} contains an error.")
        return True

    def __eval_unary_minus(self, node):
        lineno = node.lineno
        children = node.get_children()
        expression = children[1]
        is_expression_okay = self.__eval_node(expression)
        if not is_expression_okay:
            raise Exception(f"Error on line {lineno} in unary minus operation."
                            f" Expression {self.__get_string_aprox_of_subtree(expression)} contains an error.")
        if self.__subtree_leaf_dtype != "Int":
            raise Exception(f"Error on line {lineno} in unary minus operation. "
                            f"Unary minus can only be performed on integers.")
        return True

    def __eval_compound_condition(self, node):
        lineno = node.lineno
        children = node.get_children()
        left_side = children[0]
        right_side = children[2]
        chained_condition = children[4]

        left_side_okay = self.__eval_node(left_side)
        if not left_side_okay:
            raise Exception(f"Error on line {lineno}. "
                            f"Condition {self.__get_string_aprox_of_subtree(left_side)} contains an error.")
        left_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        is_function_call = self.__check_if_is_function()
        if is_function_call:
            raise Exception(f"Error on line {lineno}, function call cannot be used in condition!")
        right_side_okay = self.__eval_node(right_side)
        if not right_side_okay:
            raise Exception(
                f"Error on line {lineno}. Condition {self.__get_string_aprox_of_subtree(right_side)} contains an error.")
        is_function_call = self.__check_if_is_function()
        if is_function_call:
            raise Exception(f"Error on line {lineno}, function call cannot be used in condition.")
        right_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)

        if left_side_info[1] != right_side_info[1]:
            raise Exception("Type mismatch in addition. Addition can only be performed with integers.")
        is_chained_condition_okay = self.__eval_node(chained_condition)
        if not is_chained_condition_okay:
            raise Exception(f"Error on line {lineno}. Compound condition contains an error.")
        return True

    def __eval_while_statement(self, node):
        lineno = node.lineno
        children = node.get_children()
        condition = children[0]
        body = children[1]
        is_condition_okay = self.__eval_node(condition)
        if not is_condition_okay:
            raise Exception(f"Error on line {lineno}. "
                            f"Condition {self.__get_string_aprox_of_subtree(condition)} "
                            f"in while loop contains an error!")
        is_body_okay = self.__eval_node(body)
        if not is_body_okay:
            raise Exception(f"Error on line {lineno}. Compound block of while statement contains an error.")
        return True

    def __eval_repeat_statement(self, node):
        lineno = node.lineno
        children = node.get_children()
        body = children[0]
        condition = children[1]
        is_condition_okay = self.__eval_node(condition)
        if not is_condition_okay:
            raise Exception(f"Error on line {lineno}. Condition"
                            f" {self.__get_string_aprox_of_subtree(condition)} of repeat statement contains an error.")
        is_body_okay = self.__eval_node(body)
        if not is_body_okay:
            raise Exception(f"Error on line {lineno}. Compound block of repeat statement contains an error.")
        return True

    def __eval_return_statement(self, node):
        lineno = node.lineno
        children = node.get_children()
        expression = children[0]
        is_expression_okay = self.__eval_node(expression)
        if not is_expression_okay:
            raise Exception(f"Error on line {lineno}."
                            f" Expression of return statement {self.__get_string_aprox_of_subtree(expression)} contains an error.")
        self.ret_statement_count += 1
        self.ret_value = expression
        return True

    def __eval_expression_sum(self, node):
        lineno = node.lineno
        children = node.get_children()
        term = children[0]
        factor = children[1]
        is_term_expression_okay = self.__eval_node(term)
        left_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)

        if not is_term_expression_okay:
            raise Exception(
                f"Error on line {lineno}. Addition expression {self.__get_string_aprox_of_subtree(term)} contains an error.")
        is_factor_okay = self.__eval_node(factor)
        right_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if not is_factor_okay:
            raise Exception(
                f"Error on line {lineno}. Addition expression {self.__get_string_aprox_of_subtree(factor)} contains an error.")

        if left_side_info[1] != right_side_info[1]:
            raise Exception(
                f"Error on line {lineno}. Type mismatch in addition. Addition can only be performed with integers.")
        return True

    def __eval_expression_divide(self, node):
        lineno = node.lineno
        children = node.get_children()
        factor = children[0]
        expression = children[1]
        is_dividend_okay = self.__eval_node(factor)
        dividend_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if not is_dividend_okay:
            raise Exception(f"Error on line {lineno}. Division expression {self.__get_string_aprox_of_subtree(factor)}."
                            f" Dividend is not a valid expression.")
        is_divisor_okay = self.__eval_node(expression)
        divisor_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if dividend_info[1] != divisor_info[1]:
            raise Exception("Type mismatch in division. Division can only be performed with integers.")

        if not is_divisor_okay:
            raise Exception(f"Error on line {lineno} in division."
                            f" Expression {self.__get_string_aprox_of_subtree(expression)} contains an error. "
                            f"Divisor is not a valid expression.")
        if type(self.__subtree_leaf_value) is int and self.__subtree_leaf_value == 0:
            raise Exception(f"Error on line {lineno}. Division by zero is not defined.")
        return True

    def __eval_expression_minus(self, node):
        lineno = node.lineno
        children = node.get_children()
        term = children[0]
        factor = children[1]
        is_term_expression_okay = self.__eval_node(term)
        left_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if not is_term_expression_okay:
            raise Exception(f"Error on line {lineno} in subtraction expression. Expression "
                            f"{self.__get_string_aprox_of_subtree(term)} contains an error.")
        is_factor_okay = self.__eval_node(factor)
        if not is_factor_okay:
            raise Exception(f"Error on line {lineno}."
                            f" Expression {self.__get_string_aprox_of_subtree(factor)} contains an error.")

        right_side_info = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if left_side_info[1] != right_side_info[1]:
            raise Exception(
                f"Error on line {lineno}. Type mismatch in subtraction. Subtraction can only be performed with integers.")
        return True

    def __eval_if_else_stmt(self, node):
        lineno = node.lineno
        children = node.get_children()
        condition = children[0]
        if_body = children[1]
        else_body = children[2]
        is_condition_okay = self.__eval_node(condition)
        if not is_condition_okay:
            raise Exception(
                f"Error on line {lineno} in if statement. Condition {self.__get_string_aprox_of_subtree(condition)} contains an error.")
        is_if_body_okay = self.__eval_node(if_body)
        if not is_if_body_okay:
            raise Exception(f"Error on line {lineno} in body of if statement.")
        is_else_body_okay = self.__eval_node(else_body)
        if not is_else_body_okay:
            raise Exception(f"Error on line {lineno} in body of else statement.")
        return True

    def __eval_if_stmt(self, node):
        lineno = node.lineno
        children = node.get_children()
        condition = children[0]
        body = children[1]
        is_condition_okay = self.__eval_node(condition)
        if not is_condition_okay:
            raise Exception(
                f"Error on line {lineno} in if statement. "
                f"Condition {self.__get_string_aprox_of_subtree(condition)} contains an error.")
        is_if_body_okay = self.__eval_node(body)
        if not is_if_body_okay:
            raise Exception(f"Error on line {lineno} in body of if statement.")
        return True

    def __eval_var_modification(self, node):
        lineno = node.lineno
        children = node.get_children()
        identifier = children[0].name
        modification_operator = children[1].name
        expression = children[2]
        is_valid_identifier = self.__find_identifier(identifier, lineno)
        if not is_valid_identifier:
            raise Exception(f"Error on line {lineno}. Identifier {identifier} is not defined.")
        if self.__identifier_table_entry.const:
            raise Exception(f"Error on line {lineno} in variable modification identifier {identifier} is a constant. "
                            f"Its value cannot be adjusted at runtime.")
        is_valid_expression = self.__eval_node(expression)
        if not is_valid_expression:
            raise Exception(
                f"Error on line {lineno} in variable modification when updating value of variable {identifier}. "
                f"The assigned expression {self.__get_string_aprox_of_subtree(expression)} is not valid.")
        if modification_operator != "=" and self.__check_if_is_function():
            raise Exception(
                f"Error on line {lineno} in variable modification when updating value of variable {identifier}."
                f" Function call can be only used with assignment operator, '='.")
        return True

    def __eval_function_declaration(self, node):
        lineno = node.lineno
        children = node.get_children()
        is_function_okay = self.__eval_node(children[0])
        if not is_function_okay:
            raise Exception(f"Error on line {lineno}. Function declaration contains an error")
        return True

    def __eval_for_loop_block(self, node):
        lineno = node.lineno
        children = node.get_children()
        loop_var = children[0]
        condition = children[1]
        step = children[2]
        body = children[3]

        is_loop_var_okay = self.__eval_node(loop_var)
        if not is_loop_var_okay:
            raise Exception(f"Error on line {lineno} in declaration of controlling variable"
                            f" {self.__get_string_aprox_of_subtree(loop_var)} in for loop statement")
        is_loop_condition_okay = self.__eval_node(condition)
        if not is_loop_condition_okay:
            raise Exception(
                f"Error on line {lineno}. for loop condition {self.__get_string_aprox_of_subtree(condition)} is not correct.")
        is_step_okay = self.__eval_node(step)
        if not is_step_okay:
            raise Exception(
                f"Error on line {lineno}, step statement of for loop {self.__get_string_aprox_of_subtree(step)} is not correct.")
        is_body_okay = self.__eval_node(body)
        if not is_body_okay:
            raise Exception(f"Error on line {lineno} in body of for loop.")
        return True

    def __eval_condition(self, node):
        lineno = node.lineno
        children = node.get_children()
        left_side = children[0]
        right_side = children[2]
        is_left_side_okay = self.__eval_node(left_side)
        if not is_left_side_okay:
            raise Exception(f"Error on line {lineno}."
                            f" Expression {self.__get_string_aprox_of_subtree(left_side)}"
                            f" on left side of condition contains an error.")
        is_function_call = self.__check_if_is_function()
        if is_function_call:
            raise Exception(f"Error on line {lineno}. Condition cannot contain function call.")
        is_right_side_okay = self.__eval_node(right_side)
        is_function_call = self.__check_if_is_function()
        if is_function_call:
            raise Exception(f"Error on line {lineno}. Condition cannot contain function call.")

        if not is_right_side_okay:
            raise Exception(f"Error on line {lineno}. "
                            f"Expression {self.__get_string_aprox_of_subtree(right_side)} on right side of condition.")
        return True

    def __eval_loop_step(self, node):
        lineno = node.lineno
        children = node.get_children()
        identifier = children[0].name
        is_valid_identifier = self.__find_identifier(identifier, lineno)
        if not is_valid_identifier:
            raise Exception(f"Error on line {lineno} in for loop step. {identifier} is not declared.")
        if self.__identifier_table_entry.const:
            raise Exception(f"Error on line {lineno} in for loop step. "
                            f"{identifier} is a constant. Value cannot be changed.")
        return True

    def __eval_loop_var(self, node):
        lineno = node.lineno
        children = node.get_children()
        expr = children[0]
        if len(children) == 2:
            expr = children[1]
        is_variable_okay = self.__eval_node(expr)
        if not is_variable_okay:
            raise Exception(f"Error on line {lineno} in declaration of for loop variable. "
                            f"Expression {expr} contains an error.")
        return True

    def __eval_function_signature(self, node):
        lineno = node.lineno
        children = node.get_children()
        function_name = children[0].name
        params = children[1]
        return_type = children[2]
        body = children[3]
        # save previous scope
        previous_level = self.level
        previous_return_count = self.ret_statement_count
        previous_return_val = self.ret_value
        # update scope
        self.level = function_name
        params_ok = self.__eval_node(params)

        if not params_ok:
            raise Exception(f"Error on line {lineno}. Parameters of function {function_name} contain an error.")
        return_type_val = return_type.name
        if return_type_val != "Void":
            return_type_okay = self.__eval_node(return_type)
            if not return_type_okay:
                raise Exception(f"Error on line {lineno}. Return type of function {function_name} "
                                f"contains and error. Valid types: Int, Boolean")
            return_type_val = return_type.get_children()[0].name
        else:
            self.__mark_visited(return_type)
        body_ok = self.__eval_node(body)
        if not body_ok:
            raise Exception(f"Error on line {lineno}. Body of function {function_name} contains an error.")
        last_stmt_in_body = self.__last_stmt_in_block
        if return_type_val != "Void":
            if self.ret_statement_count == 0:
                raise Exception(
                    f"Error on line {lineno}. Body of function: {function_name} does not contain one return statement. ")
            elif self.ret_statement_count > 1:
                raise Exception(f"Error on line {lineno}. Function {function_name} can have only one return statement.")
            elif last_stmt_in_body != "return_statement":
                raise Exception(f" Error on line {lineno}. "
                                f"Last statement in function block of function {function_name} "
                                f"which is of type {return_type_val} must be a return statement.")

        # restore previous scope
        self.level = previous_level
        self.ret_statement_count = previous_return_count
        self.ret_value = previous_return_val
        return True

    # parameters are very strictly defined in grammar, they can't really be wrong.
    def __eval_function_parameters(self, node):
        # children = node.get_children()
        return True

    def __eval_block(self, node):
        lineno = node.lineno
        tmp_node = node
        # traverse through block subtree - taking over "control" from the main traversal loop
        while True:
            children = tmp_node.get_children()
            n = len(children)
            tmp = children[0]
            # block variable declaration, the relevant subtree is on index 1 instead of 0
            if n == 3:
                tmp = children[1]
            is_statement_okay = self.__eval_node(tmp)
            if not is_statement_okay:
                raise Exception(f"Error on line {lineno} in block.")

            if len(children) == 1:
                if tmp.name != "block":
                    self.__last_stmt_in_block = tmp.name
                break
            tmp_node = children[1]
            if n == 3:
                tmp_node = children[2]

        return True

    def __eval_comp_block(self, node):
        lineno = node.lineno
        self.real_level += 1
        block_node = node.get_children()[0]
        is_block_okay = self.__eval_node(block_node)
        if not is_block_okay:
            raise Exception(f"Error on line {lineno} in compound block.")
        self.real_level -= 1
        return True

    # check if variable declaration is semantically correct
    # ie if integer is really an integer and if the variable does not exist in the current scope
    def __eval_var_declaration(self, node):
        lineno = node.lineno
        children = node.get_children()
        var_type = children[0]
        self.__mark_visited(var_type)
        # check variable type
        if var_type.name not in self.__var_types:
            raise Exception(f"Error on line {lineno}."
                            f" Incorrect variable declaration, unknown variable type {var_type.name}."
                            f" Allowed types: {self.__var_types}")
        # continue evaluation
        return self.__eval_node(children[1])

    def __eval_var_declaration_expression(self, node):
        lineno = node.lineno
        children = node.get_children()
        tmp = self.__subtree_leaf_dtype
        data_type = children[1]
        identifier = children[0].name
        data_type_valid = self.__eval_node(data_type)
        if not data_type_valid:
            raise Exception(f"Error on line {lineno}. "
                            f"Invalid data type {self.__get_string_aprox_of_subtree(data_type)} when declaring a variable.")
        data_type = data_type.get_children()[0]
        expression = children[2]
        # type_operation_valid = self.__check_type_value_compatibility(data_type.name,expression)
        self.__subtree_leaf_dtype = tmp
        expression_valid = self.__eval_node(expression)
        if data_type.name == "Boolean" and (self.__subtree_leaf_value == 1 or self.__subtree_leaf_value == 0):
            self.__subtree_leaf_dtype = "Boolean"

        if not expression_valid:
            raise Exception(f"Error on line {lineno}. Invalid expression "
                            f"{self.__get_string_aprox_of_subtree(expression)} value in variable declaration")
        if expression.name == "const_expression_term":
            return True
        if data_type.name == "array_type":
            data_type = data_type.get_children()[0]
            if self.__identifier_table_entry.size != self.__subtree_leaf_value:
                raise Exception(
                    f"Error on line {lineno} when declaring an array with values. Expected {self.__identifier_table_entry.size} items, got only {self.__subtree_leaf_value}.")
        data_type_compatible = data_type.name == self.__subtree_leaf_dtype
        if not data_type_compatible:
            raise Exception(f"Type mismatch, cannot assign expression of type {self.__subtree_leaf_dtype}"
                            f" to variable with type {data_type.name}")
        return data_type_compatible

    def __eval_expression_term(self, node):
        lineno = node.lineno
        children = node.get_children()
        expression = children[0]
        expression_valid = self.__eval_node(expression)
        if not expression_valid:
            raise Exception(f"Error on line {lineno}. Invalid value of expression {expression}.")
        return True

    # only int type can be multiplied
    def __eval_expression_multiply(self, node):
        lineno = node.lineno
        children = node.get_children()
        factor_valid = self.__eval_node(children[0])
        subtree_value = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if not factor_valid:
            raise Exception(f"Error on line {lineno}."
                            f" Multiplication expression {self.__get_string_aprox_of_subtree(children[0])} contains an "
                            f"error.")

        factor_expression_valid = self.__eval_node(children[1])
        if not factor_expression_valid:
            raise Exception(
                f"Error on line {lineno}. Multiplication expression {self.__get_string_aprox_of_subtree(children[1])} contains an error.")
        sub_sub_tree_value = (self.__subtree_leaf_value, self.__subtree_leaf_dtype)
        if subtree_value[1] != sub_sub_tree_value[1]:
            raise Exception(
                f"Error on line {lineno}. Type mismatch, cannot multiply types: {subtree_value[1]}, {sub_sub_tree_value[1]}."
                f" Multiplication is only allowed with Int data type. ")
        return True

    def __eval_factor_expression(self, node):
        lineno = node.lineno
        children = node.get_children()
        value_valid = self.__eval_node(children[0])
        if not value_valid:
            raise Exception(
                f"Error on line {lineno}. Invalid expression {self.__get_string_aprox_of_subtree(children[0])}")
        return value_valid

    def __eval_factor(self, node):
        lineno = node.lineno
        children = node.get_children()
        factor_value_valid = self.__eval_node(children[0])
        if not factor_value_valid:
            raise Exception(f"Error on line {lineno}. Invalid value {self.__get_string_aprox_of_subtree(children[0])}")
        return True

    def __eval_var_value(self, node):
        lineno = node.lineno
        node_name = node.name
        value = node.get_children()[0].name
        self.__mark_visited(node.get_children()[0])
        self.__subtree_leaf_value = value
        if node_name == "var_value":
            self.__subtree_leaf_dtype = "Int"
            return True
        elif node_name == "var_value_boolean":
            self.__subtree_leaf_dtype = "Boolean"
            return True
        elif node_name == "var_value_string":
            self.__subtree_leaf_dtype = "String"
            return True
        elif node_name == "var_value_identifier":
            self.__subtree_leaf_dtype = "identifier"
        valid_identifier = self.__find_identifier(value, lineno)
        if not valid_identifier:
            raise Exception(f"Error on line {lineno}. Invalid identifier {value}.")
        self.__subtree_leaf_value = self.__identifier_table_entry

        return True

    def __eval_function_call(self, node):
        lineno = node.lineno
        children = node.get_children()
        function_name = children[0].name
        is_valid_identifier = self.__find_identifier(function_name, lineno)
        if not is_valid_identifier:
            raise Exception(f"Error on line {lineno}. Function {function_name} is not declared.")
        function_prototype = self.__identifier_table_entry
        function_arguments = children[1]

        function_params = function_prototype.params
        function_call_ok = self.__check_function_call(function_params, function_arguments, lineno)
        if not function_call_ok:
            raise Exception(f"Error on line {lineno}. Function call {function_name} contains an error. ")
        self.__subtree_leaf_value, self.__subtree_leaf_dtype = function_prototype.name, function_prototype.return_type
        return function_call_ok

    def __eval_data_type(self, node):
        lineno = node.lineno
        data_type = node.get_children()[0]
        self.__mark_visited(node.get_children()[0])
        if data_type.name == "array_type":
            data_type = data_type.get_children()[0]
        if data_type.name not in self.__data_types:
            raise Exception(
                f"Error on line {lineno}. Invalid data type {data_type.name}. Valid data types: Int, Boolean, Array, String")
        self.__subtree_leaf_dtype = data_type.name
        return True

    # mark node as visited
    def __mark_visited(self, node):
        self.__visited_nodes.add(node)

    def __check_function_call(self, function_params, function_arguments, lineno):
        tmp = list(function_params.keys())
        walker = 0
        param_count = len(tmp)
        kiddos = function_arguments.get_children()
        # argument list
        if len(kiddos) == 2:
            while True:
                if walker >= param_count:
                    raise Exception(
                        f"Error on line {lineno}. Too many arguments, expected {param_count}, got at least {walker}.")

                # single argument
                if len(kiddos) == 1:
                    kiddos = kiddos[0]
                    break
                argument_ok = self.__compare_argument_and_parameter(kiddos[0], function_params[tmp[walker]], lineno)
                if not argument_ok:
                    return False
                self.__mark_visited(kiddos[1])
                kiddos = kiddos[1].get_children()
                walker += 1
        # single argument of function
        else:
            kiddos = kiddos[0]
            # no arguments provided
            if kiddos.name == '':
                if param_count != 0:
                    raise Exception(
                        f"Error on line {lineno}. No arguments provided in function call, expected {param_count} arguments.")
                return True

        argument = kiddos
        argument_ok = self.__compare_argument_and_parameter(argument, function_params[tmp[walker]], lineno)
        walker += 1
        if walker != param_count:
            raise Exception(
                f"Error on line {lineno}. Invalid number of argument in function call, expected {param_count}, instead got {walker}.")
        return argument_ok

    def __compare_argument_and_parameter(self, argument, parameter, lineno):
        value_ok = self.__eval_node(argument)
        if not value_ok:
            raise Exception(
                f"Error on line {lineno}. Invalid argument value {argument.get_children()[0].name} for parameter {parameter.name}")
        argument_type = self.__subtree_leaf_dtype
        function_param_type = parameter.type
        if function_param_type != argument_type:
            raise Exception(
                f"Error on line {lineno}. Argument missmatch, expected argument with type {function_param_type} for parameter {parameter.name},\
             instead got argument with type {argument_type}.")
        if parameter.type == "Array" and self.__subtree_leaf_value != parameter.size:
            raise Exception(f"Error on line {lineno}."
                            f"Argument missmatch, "
                            f"expected array with length {parameter.size}, "
                            f"got array with length {self.__subtree_leaf_value}")
        return True

    def __find_identifier(self, identifier, lineno):
        symbol = find_entry_in_symbol_table(self.__symbol_table, self.level, self.real_level, identifier)
        if symbol is None or (symbol.type != "func" and symbol.lineno > lineno):
            raise Exception(f"Error on line {lineno}. Identifier {identifier} not declared!")
        self.__identifier_table_entry = symbol
        self.__subtree_leaf_dtype = symbol.type
        return True

    # util function, saves information about identifier
    def __save_ident_values(self, symbol_table_record):
        self.__identifier_table_entry = symbol_table_record

    # check if last found identifier is a function or not
    def __check_if_is_function(self):
        val = self.__identifier_table_entry
        if not val:
            return False
        if val.type == "func":
            return True
        return False

    # generate some vague string representation of statement
    def __get_string_aprox_of_subtree(self, node):
        leaves = node.get_leaves()
        str = ""
        for i in range(len(leaves)):
            str += leaves[i].name
        return str
