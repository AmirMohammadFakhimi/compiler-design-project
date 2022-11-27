import scanner
symbol_table = ['al', 'b', 'c']

if __name__ == '__main__':
    scanner.initial_input_file()

    symbol_table_file = open("symbol_table.txt", 'w')
    for i in range(len(symbol_table)):
        symbol_table_file.write(f'{i} {symbol_table[i]}\n')
