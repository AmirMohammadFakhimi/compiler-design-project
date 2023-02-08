# Amir Mohammad Fakhimi : 99170531
# Erfan Sadraiye : 99101835
import code_gen
import scanner
import parser


def create_files_for_scanner_phase():
    create_symbol_table_file()
    create_file_from_dict(open("tokens.txt", 'w'), scanner.tokens)
    create_file_from_dict(open("lexical_errors.txt", 'w'), scanner.errors, "There is no lexical error.")


def create_symbol_table_file():
    symbol_table_file = open("symbol_table.txt", 'w')
    symbol_table = scanner.NewSymbolTable.symbol_table

    symbol_table_file.write(
        "{:<8} {:<15} {:<10} {:<10} {:<10} {:<8}\n".format(" ", "lexeme", "type", "address", "kind", "no_args"))
    symbol_number = 1
    for keyword in scanner.keywords:
        symbol_number += 1
        symbol_table_file.write("{:<8} {:<15}\n".format(symbol_number, keyword))
    symbol_number = len(scanner.keywords)
    for i in range(len(symbol_table)):
        row = symbol_table[i]
        row = [symbol_number, row.lexeme, row.type, row.address, row.kind, row.no_of_args]
        row = [str(a) for a in row]
        symbol_table_file.write("{:<8} {:<15} {:<10} {:<10} {:<10} {:<8}\n".format(*row))
        symbol_number += 1

    symbol_table_file.close()


def create_file_from_dict(file, dictionary, write_on_empty_dict=None):
    if len(dictionary) == 0 and write_on_empty_dict is not None:
        file.write(write_on_empty_dict)

    for line_number in dictionary:
        file.write(f'{line_number}.\t')

        for (key, value) in dictionary[line_number]:
            file.write(f'({key}, {value}) ')

        file.write("\n")


def create_files_for_parser_phase():
    create_error_file()
    create_parse_tree_file()


def create_error_file():
    error_file = open("syntax_errors.txt", 'w')
    if len(parser.errors) == 0:
        error_file.write("There is no syntax error.")
    else:
        for error in parser.errors:
            error_file.write(f'{error}\n')


def create_parse_tree_file():
    parse_tree_file = open("parse_tree.txt", 'w')
    parse_tree_file.write(parser.get_parse_tree())


def create_pb_file():
    pb_file = open("output.txt", 'w')
    pb = code_gen.pb

    line_number = 0
    for line in pb:
        pb_file.write(f'{line_number}\t{line}\n')
        line_number += 1


def create_semantic_errors_file():
    semantic_errors_file = open("semantic_errors.txt", 'w')
    semantic_errors = code_gen.semantic_errors

    if len(semantic_errors) == 0:
        semantic_errors_file.write("The input program is semantically correct")
    else:
        for error in semantic_errors:
            semantic_errors_file.write(f'#{scanner.number_of_line} : {error}\n')


def reset_compiler():
    scanner.reset_scanner()
    parser.reset_parser()
    code_gen.reset_code_gen()


if __name__ == '__main__':
    scanner.initial_scanner()
    # create_files_for_scanner_phase()
    # scanner.run_scanner()
    # create_files_for_parser_phase()
    parser.run_parser()
    create_pb_file()
    create_symbol_table_file()
    create_semantic_errors_file()
