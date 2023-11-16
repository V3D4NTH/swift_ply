
from src.syntax_analyzer.symbol_record import SymbolRecord


def find_real_level(symbols, index):
    real_level_result = 0
    for i in symbols[index].get_ancestors():
        if i.name == "compound_block":
            real_level_result += 1
    return real_level_result


def find_entry_in_symbol_table(symbol_table, level, real_level, symbol_name):
    # [JT] global scope
    if real_level == 0:
        if symbol_name not in symbol_table:
            return None
        return symbol_table[symbol_name]
    # [JT] we are searching for entry of identifier in glob al scope
    if level == 0:
        # [JT] we are indented in some block
        # start searching bottom - up in indented scopes
        scope_count = len(symbol_table['_scopes'])
        while real_level > 0:
            # no variables are indented in this block, the symbol must exist in global scope
            if scope_count == 0:
                break
            real_level -= 1
            # current identation does not have any local variables, go up
            if real_level >= scope_count:
                continue
            indent_dic = symbol_table['_scopes'][real_level]
            if symbol_name in indent_dic:
                return indent_dic[symbol_name]

        if symbol_name not in symbol_table:
            return None

        # we did not find the variable in indented blocks => it must be in global scope
        return symbol_table[symbol_name]
    else:
        # retrieve variables in the function block
        function_symbol_table = symbol_table[level]
        scope_count = len(function_symbol_table.locals) if function_symbol_table.locals is not None else 0
        # again we have to search bottom up from our current indentation
        while real_level > 0 and scope_count > 0:
            real_level -= 1
            if real_level >= scope_count:
                continue
            indent_dic = function_symbol_table.locals[real_level]
            if symbol_name in indent_dic:
                return indent_dic[symbol_name]

        if symbol_name in function_symbol_table.params:
            return function_symbol_table.params[symbol_name]
        if symbol_name in symbol_table:
            return symbol_table[symbol_name]
        return None


# first run through the tree to generate table of symbols
def generate_table_of_symbols(symbol_table, symbols: list, level="0", real_level=0, address=3, index=0):
    """
        It generates a table of symbols
        """
    position_in_tree = index
    index = 0
    # [JT] indented scopes in global scope
    symbol_table["_scopes"] = []
    while index < len(symbols):
        ancestor = symbols[index].get_ancestors()[0]
        if ancestor.name == "function_signature":
            real_level = find_real_level(symbols, index)
            if symbols[index].name in symbol_table.keys():
                raise Exception("Duplicate symbol:", symbols[index].name, "in", symbol_table.keys())
            params = {}
            local_address = 3
            ids_and_types = symbols[index].get_sisters()[0].get_leaf_names()
            lineno = symbols[index].get_sisters()[1].lineno
            if len(ids_and_types) > 1:
                i = 0
                # [JT] while loop had to be used instead of for loop so i could dynamically change the driving variable 'i'
                while i < len(ids_and_types):
                    identifier_name = ids_and_types[i]
                    # [JT] array parameters consists of 3 values, name, type, size.
                    # If i pointer hits the type or size, we want to force another iteration
                    if identifier_name == "Array":
                        continue
                    if type(identifier_name) is int:
                        i += 1
                        if i >= len(ids_and_types):
                            break
                        identifier_name = ids_and_types[i]

                    dtype = ids_and_types[i + 1]
                    size = 1
                    if dtype == "Array":
                        size = ids_and_types[i + 2]
                    if ids_and_types[i] in params.keys():
                        raise Exception("Duplicate symbol:", ids_and_types[i], "in", params.keys())

                    params[ids_and_types[i]] = (
                        SymbolRecord(identifier_name, dtype, size=size, param=True, level=level,
                                     tree_position=position_in_tree + index,
                                     real_level=real_level, lineno=lineno,
                                     address=local_address))
                    i += 2

                    local_address += 1
            func_name = symbols[index].name
            symbol_table[func_name] = (
                SymbolRecord(symbols[index].name, "func", params=params, level=level, real_level=real_level,
                             tree_position=position_in_tree + index,
                             address=address,
                             lineno=lineno,
                             return_type=symbols[index].get_sisters()[1].get_leaf_names()[0]))
            address += 1
            func_body = symbols[index].get_sisters()[2].get_leaves()
            # shifting index to skip duplicates
            index += len(func_body)
            # recursive call
            generate_table_of_symbols(symbol_table, level=symbol_table[func_name].name, real_level=real_level,
                                      symbols=func_body, address=local_address, index=index)

        if ancestor.name == "var_declaration_expression" or ancestor.name == "var_declaration":
            real_level = find_real_level(symbols, index)
            lineno = symbols[index].get_sisters()[0].lineno
            if level != "0" and symbol_table[level].locals is None:
                # stack of local variables inside function scope
                symbol_table[level].locals = []
                symbol_type = symbols[index].get_sisters()[0].children[0]
                size = 1
                # workaround for array_type, because the subtree for array type is deeper than for any other type
                if symbol_type.name == "array_type":
                    tmp = symbol_type.get_children()
                    symbol_type = tmp[0]
                    size = tmp[1].name
                symbol_table[level].locals.append({symbols[index].name: (SymbolRecord(symbols[index].name,
                                                                                      symbol_type=symbol_type.name,
                                                                                      level=level,
                                                                                      size=size,
                                                                                      lineno=lineno,
                                                                                      real_level=real_level,
                                                                                      tree_position=position_in_tree + index,
                                                                                      address=address))})
                if ancestor.get_sisters()[0].name == "let":
                    symbol_table[level].locals[real_level - 1][symbols[index].name].const = True
            elif level != "0":
                # if we are indented inside local scope of function, we push a new map into stack
                if real_level > len(symbol_table[level].locals):
                    symbol_table[level].locals.append({})
                current_scope_dic = symbol_table[level].locals[real_level - 1]
                if symbols[index].name in current_scope_dic.keys():
                    raise Exception("Duplicate symbol:", symbols[index].name, "in", current_scope_dic.keys())
                symbol_type = symbols[index].get_sisters()[0].children[0]
                size = 1
                if symbol_type.name == "array_type":
                    tmp = symbol_type.get_children()
                    symbol_type = tmp[0]
                    size = tmp[1].name
                current_scope_dic[symbols[index].name] = (SymbolRecord(symbols[index].name,
                                                                       symbol_type=symbol_type.name,
                                                                       level=level,
                                                                       size=size,
                                                                       real_level=real_level,
                                                                       tree_position=position_in_tree + index,
                                                                       address=address))
                if ancestor.get_sisters()[0].name == "let":
                    current_scope_dic[symbols[index].name].const = True
            else:

                dic = symbol_table
                if real_level != 0:
                    if real_level > len(symbol_table["_scopes"]):
                        symbol_table["_scopes"].append({})
                    dic = symbol_table["_scopes"][real_level - 1]
                if symbols[index].name in dic.keys():
                    raise Exception("Duplicate symbol:", symbols[index].name, "in", symbol_table.keys())
                symbol_type = symbols[index].get_sisters()[0].children[0]
                size = 1
                if symbol_type.name == "array_type":
                    tmp = symbol_type.get_children()
                    symbol_type = tmp[0]
                    size = tmp[1].name
                lineno = symbols[index].get_sisters()[0].lineno
                dic[symbols[index].name] = (SymbolRecord(symbols[index].name,
                                                         symbol_type=symbol_type.name,
                                                         size=size,
                                                         lineno=lineno,
                                                         level=level,
                                                         real_level=real_level,
                                                         tree_position=position_in_tree + index,
                                                         address=address))

                if ancestor.get_sisters()[0].name == "let":
                    dic[symbols[index].name].const = True
            address += 1
        index += 1
