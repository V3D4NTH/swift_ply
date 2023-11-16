

# It's a class that holds the constants used by the PL/0 compiler
class Pl0Const:

    def __init__(self):

        self.types = [int]

        # A dictionary that maps the operators to the functions that generate the code for the operators.
        self.expressions = {"expression_sum": self.gen_opr_add, "expression_minus": self.gen_opr_sub,
                            "expression_multiply": self.gen_opr_mul, "expression_divide": self.gen_opr_div,
                            "expression_term": self.gen_term, "const_expression_term": self.gen_term}

        # A dictionary that maps the operators to the functions that generate the code for the operators.
        self.var_modifications = {"-=": self.gen_sub, "+=": self.gen_add, "*=": self.gen_mulby,
                                  "/=": self.gen_divby, "=": self.gen_equals}

        # A dictionary that maps the operators to the functions that generate the code for the operators.
        self.cond_expressions = {"<": self.gen_lesser, "!=": self.gen_not_equal, "<=": self.gen_lesser_equals,
                                 ">": self.gen_greater, ">=": self.gen_greater_equals, "==": self.gen_dos_equals, }

    def gen_lesser(self):
        """
        It returns a list of all the numbers in the range of the input number that are less than the input number
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_not_equal(self):
        """
        It generates a list of all the numbers from 1 to 100 that are not equal to the number passed in
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_lesser_equals(self):
        """
        It generates a list of all the numbers less than or equal to the number passed in
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_greater(self):
        """
        It returns a generator that yields all the elements of the list that are greater than the given number
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_greater_equals(self):
        """
        It generates a function that returns a boolean value indicating
         whether the first argument is greater than or equal
        to the second argument
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_dos_equals(self):
        """
        It generates a function that compares two objects
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_sub(self, operator):
        """
        It generates a subtraction function.

        :param operator: The operator to use
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_add(self, operator):
        """
        It takes a string, and returns a function that takes
         two arguments, and returns the result of applying the operator
        to the two arguments

        :param operator: The operator to generate
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_mulby(self, operator):
        """
        It takes a number and returns a function that multiplies that number by the number
         passed to the returned function

        :param operator: The operator to use
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_divby(self, operator):
        """
        It takes a number and returns a function that takes another number and returns the result of dividing the first
        number by the second

        :param operator: The operator to use
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_equals(self, operator):
        """
        does nothing
        """
        pass

    def gen_term(self, operator):
        """
        It adds two numbers.

        :param const1: The first constant to add
        :param const2: The second constant to add to the first
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_opr_add(self, const1, const2):
        """
        It adds two numbers.

        :param const1: The first constant to add
        :param const2: The second constant to add to the first
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_opr_sub(self, const1, const2):
        """
        It subtracts two numbers.

        :param const1: The first constant to be used in the operation
        :param const2: The constant to be subtracted from
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_opr_mul(self, const1, const2):
        """
        It generates a new constant
        that is the product of two other constants

        :param const1: The first constant to be multiplied
        :param const2: The second constant to be multiplied
        """
        raise NotImplementedError("Method not yet implemented.")

    def gen_opr_div(self, const1, const2):
        """
        It divides two numbers.

        :param const1: The first constant to be used in the operation
        :param const2: The constant to divide by
        """
        raise NotImplementedError("Method not yet implemented.")

