
import os

from src.pl0_vm.p_machine import run_pl0_code


def generate_output_files(dst, generated_code, output_dir):
    """
    It generates output files

    :param dst: syntax tree
    :param generated_code: a list of strings, each of which is a line of generated code
    """
    if "output" not in os.listdir(output_dir):
        if output_dir[-1] != "/":
            output_dir += "/"
        os.mkdir(output_dir + "output")
    output_dir += "output"
    with open(output_dir + "/full_tree.txt", mode="w") as tree:
        tree.writelines(dst.get_ascii(attributes=["name", "dist", "label", "complex"]))
    with open(output_dir + "/tree.txt", mode="w") as tree:
        tree.writelines(str(dst))
    with open(output_dir + "/symbol_table.txt", mode="w") as table:
        generated_code.print_symbol_table(table.writelines)
    return output_dir


def visualize_dst(dst, show_tree_with_pyqt5):
    # # ###### Showing the tree. with pyqt5 ##################
    if show_tree_with_pyqt5:
        from ete3 import TreeStyle
        tree_style = TreeStyle()
        tree_style.show_leaf_name = True
        tree_style.mode = "c"
        tree_style.arc_start = -180  # 0 degrees = 3 o'clock
        dst.show(
            tree_style=tree_style
        )


def save_generated_code(generated_code, formatted_input_code, output_dir):
    """
    It saves the generated code to a file

    :param generated_code: The code that was generated by the model
    :param formatted_input_code: The input code, formatted with the correct indentation
    """
    if generated_code.return_code() != "":
        # Writing the generated code to a file.
        with open(output_dir + "/generated_code_only.txt", mode="w") as txt:
            txt.writelines(generated_code.return_code())
        with open(output_dir + "/generated_code_with_input.txt", mode="w") as txt:
            txt.writelines("----------input code----------------\n")
            txt.writelines(formatted_input_code)
            txt.writelines("\n")
            txt.writelines("----------generated code------------\n")
            txt.writelines(generated_code.return_code())
            txt.writelines("-------------PL/0 start-------------\n")
            txt.writelines(run_pl0_code(generated_code.code))
            txt.writelines("------------------------------------")