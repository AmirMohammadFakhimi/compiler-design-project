import compiler
import parser
import scanner

if __name__ == '__main__':
    for i in range(1, 9):
        file_name = f'T0{i}'

        scanner.initial_scanner(f'p2_testcases/{file_name}/input.txt')
        parser.run_parser()
        compiler.create_files_for_parser_phase()

        to_check_parse_tree = open(f"parse_tree.txt", 'r').read()
        to_check_syntax_errors = open(f"syntax_errors.txt", 'r').read()

        original_parse_tree = open(f"p2_testcases/{file_name}/parse_tree.txt", 'r').read()
        original_syntax_errors = open(f"p2_testcases/{file_name}/syntax_errors.txt", 'r').read()

        is_pass = True
        if to_check_parse_tree != original_parse_tree:
            print(f"parse_tree{i}.txt is not correct!")
            is_pass = False
        if to_check_syntax_errors != original_syntax_errors:
            print(f"syntax_errors{i}.txt is not correct!")
            is_pass = False

        if is_pass:
            print(f"Test {i} is passed!")