from src.start_compiler import start_compiler

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Not so swift compiler.')
    parser.add_argument('-i', '--f_input',
                        help='path to input file...',  required=True)
    parser.add_argument('-o', '--out',  default="./",
                        help='path to output dir...')
    parser.add_argument('-qt', '--show_tree_with_pyqt5',  default=False,  type=bool,
                        help='True/False')
    args = parser.parse_args()

    start_compiler(input_file_name=args.f_input, output_dir=args.out, show_tree_with_pyqt5=args.show_tree_with_pyqt5)
