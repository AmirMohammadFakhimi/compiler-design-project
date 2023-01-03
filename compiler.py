import scanner
import parser
import anytree

def create_files_for_scanner_phase():
    create_symbol_table_file()
    create_file_from_dict(open("tokens.txt", 'w'), scanner.tokens)
    create_file_from_dict(open("lexical_errors.txt", 'w'), scanner.errors, "There is no lexical error.")


def create_symbol_table_file():
    symbol_table_file = open("symbol_table.txt", 'w')
    symbol_table = scanner.symbol_table

    symbol_number: int
    for symbol_number in range(1, len(symbol_table) + 1):
        symbol_table_file.write(f'{symbol_number}.\t{symbol_table[symbol_number - 1]}\n')

    for keyword in scanner.keywords:
        if keyword not in scanner.symbol_table_set:
            symbol_number += 1
            symbol_table_file.write(f'{symbol_number}.\t{keyword}\n')

    symbol_table_file.close()


def create_file_from_dict(file, dictionary, write_on_empty_dict=None):
    if len(dictionary) == 0 and write_on_empty_dict is not None:
        file.write(write_on_empty_dict)

    for line_number in dictionary:
        file.write(f'{line_number}.\t')

        for (key, value) in dictionary[line_number]:
            file.write(f'({key}, {value}) ')

        file.write("\n")


if __name__ == '__main__':
    scanner.initial_scanner()
    # create_files_for_scanner_phase()
    # scanner.run_scanner()
    parser.run_parser()
    root = parser.root
    for pre, _, node in anytree.RenderTree(root):
        print("%s%s" % (pre, node.name))
