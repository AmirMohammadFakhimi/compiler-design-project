import scanner


def create_files():
    create_symbol_table_file()
    create_tokens_file()
    create_errors_file()


def create_symbol_table_file():
    symbol_table_file = open("symbol_table.txt", 'w')
    symbol_table = scanner.symbol_table

    symbol_number: int
    for symbol_number in range(1, len(symbol_table) + 1):
        symbol_table_file.write(f'{symbol_number}.\t{symbol_table[symbol_number - 1]}\n')

    for keyword in scanner.keywords:
        if keyword not in scanner.symbol_table_set:
            ++symbol_number
            symbol_table_file.write(f'{symbol_number}.\t{keyword}\n')

    symbol_table_file.close()


def create_tokens_file():
    tokens_file = open("tokens.txt", 'w')

    for line_number in scanner.tokens:
        tokens_file.write(f'{line_number}.\t')

        for (token, lexeme) in scanner.tokens[line_number]:
            tokens_file.write(f'({token}, {lexeme}) ')

        tokens_file.write("\n")

def create_errors_file():
    tokens_file = open("lexical_errors.txt", 'w')

    for (line_number, lexeme, error_message) in scanner.errors:
        tokens_file.write(f'{line_number}.\t({lexeme}, {error_message}) \n')

if __name__ == '__main__':
    scanner.run_scanner()
    create_files()
