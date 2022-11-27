import scanner

if __name__ == '__main__':
    scanner.initial_input_file()
    symbol_table = scanner.symbol_table
    symbol_table_file = open("symbol_table.txt", 'w')
    for i in range(len(symbol_table)):
        symbol_table_file.write(f'{i} {symbol_table[i]}\n')
