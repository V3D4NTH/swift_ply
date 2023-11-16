
# This class is used to store information about a symbol in table
class SymbolRecord:

    def __init__(self, name, symbol_type, const=False, level=0, real_level=0, address=3, size=0,
                 params=None, return_type=None, param=False, tree_position=0, locals_vars=None,lineno=False):
        """
        This function initializes the symbol record

        :param name: The name of the symbol
        :param symbol_type: The type of the symbol
        :param const: True if the symbol is a constant, defaults to False (optional)
        :param level: the level of the symbol (0 for global, 1 for local, etc.), defaults to 0 (optional)
        :param address: The address of the symbol in memory, defaults to 0 (optional)
        :param size: size of the variable in bytes, defaults to 0 (optional)
        :param params: a list of parameters
        :param return_type: The return type of the function
        :param param: name of the variable, defaults to False (optional)
        """
        self.id = id(self)
        self.name = name
        self.type = symbol_type
        self.const = const
        self.level = level
        self.real_level = real_level
        self.address = address
        self.size = size
        self.lineno = lineno
        self.param = param
        self.tree_position = tree_position
        if self.type == "func":
            self.params = params
            self.return_type = return_type
            self.locals = locals_vars

    def __str__(self):
        ret_val = ""
        ret_val += "--------record------\n"
        ret_val += (str(self.id) + "\t|" + "id\n")
        ret_val += (str(self.name) + "\t\t\t\t|" + "name\n")
        ret_val += (str(self.real_level) + "\t\t\t\t|" + "real_level\n")
        ret_val += (str(self.type) + "\t\t\t|" + "symbol_type\n")
        ret_val += (str(self.const) + "\t\t\t|" + "const\n")
        ret_val += (str(self.level) + "\t\t\t\t|" + "level\n")
        ret_val += (str(self.address) + "\t\t\t\t|" + "address\n")
        ret_val += (str(self.size) + "\t\t\t\t|" + "size\n")
        if self.type == "func":
            ret_val += (str(self.return_type) + "\t\t\t\t|" + "return_type\n")
        if self.param:
            ret_val += (str(self.param) + "\t\t\t\t|" + "param\n")
        ret_val += "--------------------\n"
        return ret_val