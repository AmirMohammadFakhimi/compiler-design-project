import compiler
import parser
import scanner

break_s = []
semantic_stack = []
semantic_errors = []
pb = [""]
i = 1
temp_addr = 500
return_addresses = []
scope_stack = [0]
scope = 0
current_function = None
arg_num = 1


def reset_code_gen():
    global break_s, semantic_stack, pb, i, temp_addr
    break_s = []
    semantic_stack = []
    pb = []
    i = 0
    temp_addr = 500


def check_mismatch_oprand(op1, op2):
    symbol1 = scanner.NewSymbolTable.get_row_by_address(op1)
    symbol2 = scanner.NewSymbolTable.get_row_by_address(op2)
    if symbol1.type != symbol2.type:
        semantic_errors.append(
            f'#{scanner.number_of_line} : Semantic Error! Type mismatch in operands, Got {symbol2.type} instead of {symbol1.type}.')


def generate_code(op, first_op, second_op="", third_op=""):
    return f'({op}, {first_op}, {second_op}, {third_op})'


def pop_semantic_stack(num):
    global semantic_stack
    for _ in range(num):
        semantic_stack.pop()


def getaddr(inpt):
    inpt_scope = scanner.NewSymbolTable.get_scope(inpt)
    if inpt in [symbol.lexeme for symbol in scanner.NewSymbolTable.get_current_scope_symbols()] or inpt_scope < scope:
        return scanner.NewSymbolTable.get_address(inpt)
    else:
        semantic_errors.append(f"Semantic Error! '{inpt}' is not defined.")


def gettemp():
    global temp_addr
    temp_addr += 4
    return temp_addr - 4


def action_routine(symbol_action):
    global i, scope, scope_stack, current_function, arg_num
    symbol_action = int(symbol_action)

    if symbol_action == 64:  # pid
        current_input = parser.top_token[1]
        p = getaddr(current_input)
        semantic_stack.append(p)

    elif symbol_action == 65:  # pnum
        current_input = parser.top_token[1]
        semantic_stack.append(f'#{current_input}')

    elif symbol_action == 42:
        pb.append(generate_code("ASSIGN", semantic_stack[-1], semantic_stack[-2], ))
        i += 1
        pop_semantic_stack(1)

    elif symbol_action == 49:  # add
        t = gettemp()
        pb.append(generate_code("ADD", semantic_stack[-1], semantic_stack[-2], t))
        i += 1
        pop_semantic_stack(2)
        semantic_stack.append(t)

    elif symbol_action == 51:  # sub
        t = gettemp()
        pb.append(generate_code("SUB", semantic_stack[-2], semantic_stack[-1], t))
        i += 1
        pop_semantic_stack(2)
        semantic_stack.append(t)

    elif symbol_action == 52:  # mul
        t = gettemp()
        pb.append(generate_code("MULT", semantic_stack[-1], semantic_stack[-2], t))
        i += 1
        pop_semantic_stack(2)
        semantic_stack.append(t)

    elif symbol_action == 54:  # div
        t = gettemp()
        pb.append(generate_code("DIV", semantic_stack[-2], semantic_stack[-1], t))
        i += 1
        pop_semantic_stack(2)
        semantic_stack.append(t)

    elif symbol_action == 70:  # save
        semantic_stack.append(i)
        pb.append('')
        i += 1

    elif symbol_action == 66:  # jpf_save
        pb[semantic_stack[-1]] = generate_code("JPF", semantic_stack[-2], str(i + 1))
        pop_semantic_stack(2)
        semantic_stack.append(i)
        pb.append('')
        i += 1

    elif symbol_action == 67:  # label
        semantic_stack.append(i)

    elif symbol_action == 32:  # jp
        pb[semantic_stack[-1]] = generate_code("JP", i)
        semantic_stack.pop()

    elif symbol_action in [31, 39]:  # jpf
        pb[semantic_stack[-1]] = generate_code("JPF", semantic_stack[-2], str(i))
        pop_semantic_stack(2)

    elif symbol_action == 33:  # while
        pb[semantic_stack[-1]] = generate_code("JPF", semantic_stack[-2], str(i + 1))
        pb.append(generate_code("JP", semantic_stack[-3]))
        pb[break_s[-1]] = generate_code("JP", i + 1)
        i += 1
        break_s.pop()
        pop_semantic_stack(3)

    elif symbol_action == 48:  # equal
        t = gettemp()
        pb.append(generate_code("EQ", semantic_stack[-1], semantic_stack[-2], t))
        i += 1
        pop_semantic_stack(2)
        semantic_stack.append(t)

    elif symbol_action == 46:  # lt
        t = gettemp()
        pb.append(generate_code("LT", semantic_stack[-2], semantic_stack[-1], t))
        i += 1
        pop_semantic_stack(2)
        semantic_stack.append(t)

    elif symbol_action == 45:  # get_value
        t1 = gettemp()
        pb.append(generate_code("MULT", '#4', semantic_stack[-1], t1))
        pop_semantic_stack(1)
        semantic_stack.append(t1)
        t2 = gettemp()
        pb.append(generate_code("ADD", f'#{semantic_stack[-2]}', semantic_stack[-1], t2))
        pop_semantic_stack(2)
        semantic_stack.append(f'@{t2}')
        i += 2

    elif symbol_action in [7, 28]:  # pop
        semantic_stack.pop()

    elif symbol_action == 29:  # break action
        if len(break_s) == 0:
            semantic_errors.append(
                f'#{scanner.number_of_line} : Semantic Error! No \'while\' or \'switch case\' found for \'break\'.')
        else:
            pb.append(generate_code("JP", break_s[-1]))
            i += 1

    elif symbol_action == 69:  # switch_compare
        temp = gettemp()
        pb.append(generate_code('EQ', semantic_stack[-2], semantic_stack[-1], temp))
        i += 1
        pop_semantic_stack(1)
        semantic_stack.append(temp)

    elif symbol_action == 36:  # switch end
        pop_semantic_stack(1)  # pops expression
        pb[break_s[-1]] = generate_code("JP", i)
        break_s.pop()  # pops i

    elif symbol_action == 68:  # jp_forward
        pb.append(generate_code("JP", i + 2))
        i = i + 1

    elif symbol_action == 59:  # call
        function_symbol = scanner.NewSymbolTable.get_row_by_address(semantic_stack[-1])
        if function_symbol is not None and function_symbol.kind == 'func':
            if arg_num != function_symbol.no_of_args:
                semantic_errors.append(
                    f'#{scanner.number_of_line}: semantic error! Mismatch in numbers of arguments of \'{function_symbol.lexeme}\'')
            arg_num = 1
            pb.append(generate_code("ASSIGN", f'#{i + 2}', function_symbol.return_address))
            i += 1
            pb.append(generate_code("JP", function_symbol.start_address))
            i += 1
            pop_semantic_stack(1)
            t = gettemp()
            pb.append(generate_code("ASSIGN", function_symbol.return_value, t))
            i += 1
            semantic_stack.append(t)
        else:
            pb.append(generate_code("PRINT", semantic_stack[-1]))
            i += 1
            pop_semantic_stack(1)


    elif symbol_action == 8:  # int_type
        scanner.NewSymbolTable.add_type_to_last_symbol("int")

    elif symbol_action == 9:  # void_type
        if scanner.NewSymbolTable.symbol_table[-1].kind in ['var', 'arr']:
            semantic_errors.append(
                f'# {scanner.number_of_line} : Semantic Error! Illegal type of void for \'{scanner.NewSymbolTable.symbol_table[-1].lexeme}\'.')
        scanner.NewSymbolTable.add_type_to_last_symbol("void")


    elif symbol_action == 71:  # break_save
        break_s.append(i)
        pb.append('')
        i += 1

    elif symbol_action == 72:  # add_array_type_kind
        scanner.NewSymbolTable.add_size_to_last_symbol_array(int(semantic_stack[-1][1:]))
        scanner.NewSymbolTable.add_kind_to_last_symbol("arr")
        pop_semantic_stack(1)

    elif symbol_action == 6:  # add_var_kind
        scanner.NewSymbolTable.add_kind_to_last_symbol("var")
        pop_semantic_stack(1)

    elif symbol_action == 15:  # add_var_kind_args
        scanner.NewSymbolTable.add_kind_to_last_symbol("var")
        pop_semantic_stack(1)

    elif symbol_action == 73:  # add_func_kind
        scanner.NewSymbolTable.add_kind_to_last_symbol("func")
        scanner.NewSymbolTable.set_return_address_to_last_symbol(gettemp())
        scanner.NewSymbolTable.set_return_value_to_last_symbol(gettemp())
        scanner.NewSymbolTable.set_start_address_to_last_symbol(i)
        current_function = scanner.NewSymbolTable.symbol_table[-1].address
        pop_semantic_stack(1)


    elif symbol_action == 16:  # add_arr_kind_args
        scanner.NewSymbolTable.add_kind_to_last_symbol("arr")
        pop_semantic_stack(1)

    elif symbol_action in [13, 14]:  # add_one_arg
        scanner.NewSymbolTable.add_one_arg()

    elif symbol_action == 74:  # add_scope
        scope_stack.append(len(scanner.NewSymbolTable.symbol_table))
        scope += 1

    elif symbol_action == 10:  # remove_scope
        compiler.create_symbol_table_file()
        # scanner.NewSymbolTable.remove_scope()
        scope_stack.pop()
        compiler.create_symbol_table_file()
        scope -= 1

    elif symbol_action == 35:  # return expression
        function_symbol = scanner.NewSymbolTable.get_row_by_address(current_function)
        pb.append(generate_code("ASSIGN", semantic_stack[-1], function_symbol.return_value))
        i += 1
        pop_semantic_stack(1)
        pb.append(generate_code("JP", f'@{function_symbol.return_address}'))
        i += 1

    elif symbol_action == 34:  # return
        function_symbol = scanner.NewSymbolTable.get_row_by_address(current_function)
        pop_semantic_stack(1)
        pb.append(generate_code("JP", f'@{function_symbol.return_address}'))
        i += 1

    elif symbol_action in [62, 63]:  # arg
        function_symbol = scanner.NewSymbolTable.get_row_by_address(semantic_stack[-2])
        if function_symbol.lexeme != "output":
            pb.append(generate_code("ASSIGN", semantic_stack[-1], function_symbol.address + arg_num * 4))
            arg_num += 1
            i += 1
            pop_semantic_stack(1)

    elif symbol_action == 1:  # arg
        pb[0] = generate_code("JP", scanner.NewSymbolTable.find_main_address())

    elif symbol_action == 75:  # add_to_symbol_table
        lexeme = parser.top_token[1]
        scanner.NewSymbolTable(lexeme, scope)