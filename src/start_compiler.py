import ply.lex
import ply.yacc as yy
import src.syntax_analyzer as syntax
import src.lex_analyzer as lexical
import src.pl0_code_generator as gen
from src.generate_results import generate_output_files, save_generated_code, visualize_dst
from src.semantics_analyzer.analyzer import Analyzer
from src.syntax_analyzer.symbol_table import generate_table_of_symbols
def start_compiler(input_file_name: str, output_dir="./", show_tree_with_pyqt5=False):
    """
    > This function takes a file name as input, and returns a list of lists of strings
    :param input_file_name: The name of the file to be parsed
    :type input_file_name: str
    :param output_dir: The directory where the output files will be saved, defaults to ./ (optional)
    :param show_tree_with_pyqt5: If True, the tree will be displayed using PyQt5, defaults to False (optional)
    """
    with open(input_file_name) as f:
        formatted_input_code = f.read()
    # Parsing the code_input.
    lexer = \
        ply.lex.lex(module=lexical)
    y = yy.yacc(module=syntax, debug=False, write_tables=False)
    dst = y.parse(formatted_input_code)
    if dst is None:
        raise Exception(f"Input file {input_file_name} contains an syntactical error. Compilation to PL0 is therefore not possible.")
    # Generating a table of symbols.
    table_of_symbols = {}
    generate_table_of_symbols(table_of_symbols, symbols=dst.get_leaves())
    generated_code = gen.Pl0(dst, table_of_symbols)
    # Generating the output files.
    output_dir = generate_output_files(dst, generated_code, output_dir)
    # Showing the tree.
    visualize_dst(dst, show_tree_with_pyqt5)
    semantics_analyzer = Analyzer(dst, table_of_symbols)
    if not semantics_analyzer.Analyze():
        raise Exception(f"Input file {input_file_name} contains semantical error. Compilation to PL0 is therefore not possible.")
    # Generating the instructions for the PL/0 compiler.
    generated_code.generate_instructions()
    # Saving the generated code to a file.
    save_generated_code(generated_code, formatted_input_code, output_dir)
    return generated_code.return_code()
