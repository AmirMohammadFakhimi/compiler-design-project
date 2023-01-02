# check with original output
if __name__ == '__main__':
    for i in range(1, 6):
        to_check_token = open(f"meow/tokens{i}.txt", 'r').read()
        to_check_error = open(f"meow/lexical_errors{i}.txt", 'r').read()
        to_check_symbol = open(f"meow/symbol_table{i}.txt", 'r').read()

        original_token = open(f"mamad/tokens{i}.txt", 'r').read()
        original_error = open(f"mamad/lexical_errors{i}.txt", 'r').read()
        original_symbol = open(f"mamad/symbol_table{i}.txt", 'r').read()

        is_pass = True
        if to_check_token != original_token:
            print(f"tokens{i}.txt is not correct!")
            is_pass = False
        if to_check_error != original_error:
            print(f"lexical_errors{i}.txt is not correct!")
            is_pass = False
        if to_check_symbol != original_symbol:
            print(f"symbol_table{i}.txt is not correct!")
            is_pass = False

        if is_pass:
            print(f"Test {i} is passed!")