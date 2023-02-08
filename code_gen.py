import compiler
import parser
import scanner

break_s = []
semantic_stack = []
semantic_errors = []
pb = []
i = 0
temp_addr = 500

scope_stack = [0]
scope = 0

def reset_code_gen():
    global break_s, semantic_stack, pb, i, temp_addr
    break_s = []
    semantic_stack = []
    pb = []
    i = 0
    temp_addr = 500


def generate_code(op, first_op, second_op="", third_op=""):
    return f'({op}, {first_op}, {second_op}, {third_op})'


def pop_semantic_stack(num):
    global semantic_stack
    for _ in range(num):
        semantic_stack.pop()


def getaddr(inpt):
    return scanner.NewSymbolTable.get_address(inpt)


def gettemp():
    global temp_addr
    temp_addr += 4
    return temp_addr - 4


def action_routine(symbol_action):
    global i, scope, scope_stack
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

    elif symbol_action == 28:  # pop
        semantic_stack.pop()

    elif symbol_action == 29:  # break action
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

    elif symbol_action == 59:  # output
        pb.append(generate_code("PRINT", semantic_stack[-1]))
        pop_semantic_stack(1)
        i = i + 1

    elif symbol_action == 8:  # int_type
        scanner.NewSymbolTable.add_type_to_last_symbol("int")

    elif symbol_action == 9:  # void_type
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

    elif symbol_action == 15:  # add_var_kind_args
        scanner.NewSymbolTable.add_kind_to_last_symbol("var")
        scanner.NewSymbolTable.set_temp_reg_to_last_symbol(gettemp())

    elif symbol_action == 73:  # add_func_kind
        scanner.NewSymbolTable.add_kind_to_last_symbol("func")
        scanner.NewSymbolTable.set_return_value_address_to_last_symbol(gettemp())
        scanner.NewSymbolTable.set_start_address_to_last_symbol(i)

    elif symbol_action == 16:  # add_arr_kind_args
        scanner.NewSymbolTable.add_kind_to_last_symbol("arr")
        scanner.NewSymbolTable.set_temp_reg_to_last_symbol(gettemp())

    elif symbol_action in [13, 14]:  # add_one_arg
        scanner.NewSymbolTable.add_one_arg()

    elif symbol_action == 74:  # add_scope
        compiler.create_symbol_table_file()
        scope += 1
        scope_stack.append(scope)

    elif symbol_action == 10:  # remove_scope
        scanner.NewSymbolTable.remove_scope()
        scope -= 1
        scope_stack.pop()
