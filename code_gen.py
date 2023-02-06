import parser
import scanner

ss = []
current_input = None
pb = []
i = 0
temp_addr = 500


def generate_code(op, first_op, second_op="", third_op=""):
    return f'({op}, {first_op}, {second_op}, {third_op})'


def pop_ss(num):
    global ss
    for _ in range(num):
        ss.pop()


def getaddr(inpt):
    table = scanner.symbol_table
    for i in range(len(table)):
        if table[i] == inpt:
            return (i - 12) * 4 + 100
    return -1


def gettemp():
    global temp_addr
    temp_addr += 4
    return temp_addr - 4


def action_routine(symbol_action):
    global i
    current_input = parser.top_token[1]
    symbol_action = int(symbol_action)
    if symbol_action == 64:  # pid
        p = getaddr(current_input)
        ss.append(p)

    elif symbol_action == 65:  # pnum
        ss.append(f'#{current_input}')

    elif symbol_action == 42:
        pb.append(generate_code("ASSIGN", ss[-1], ss[-2], ))
        i += 1
        pop_ss(1)

    elif symbol_action == 49:  # add
        t = gettemp()
        pb.append(generate_code("ADD", ss[-1], ss[-2], t))
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 51:  # sub
        t = gettemp()
        pb.append(generate_code("SUB", ss[-1], ss[-2], t))
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 52:  # mul
        t = gettemp()
        pb.append(generate_code("MULT", ss[-1], ss[-2], t))
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 54:  # div
        t = gettemp()
        pb.append(generate_code("DIV", ss[-2], ss[-1], t))
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 70:  # save
        ss.append(i)
        pb.append('')
        i += 1

    elif symbol_action == 66:  # jpf_save
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i + 1))
        pop_ss(2)
        ss.append(i)
        pb.append('')
        i += 1

    elif symbol_action == 67:  # label
        ss.append(i)

    elif symbol_action == 32:  # jp
        pb[ss[-1]] = generate_code("JP", i)
        ss.pop()

    elif symbol_action == 31:  # jpf
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i))
        pop_ss(2)

    elif symbol_action == 33:  # while
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i + 1))
        pb.append(generate_code("JP", ss[-3]))
        i += 1
        pop_ss(4)

    elif symbol_action == 48:  # equal
        t = gettemp()
        pb.append(generate_code("EQ", ss[-1], ss[-2], t))
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 46:  # lt
        t = gettemp()
        pb.append(generate_code("LT", ss[-2], ss[-1], t))
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 45:  # get_value
        addr = ss[-2] + ss[-1]
        ss.append(addr)

    elif symbol_action == 28:  # pop
        ss.pop()

    elif symbol_action == 29:  # break action
        pb.append(generate_code("JP", ss[-4]))
        i += 1

    elif symbol_action == 69:  # switch_compare
        temp = gettemp()
        pb.append(generate_code('EQ', ss[-2], ss[-1], temp))
        i += 1
        pop_ss(1)
        ss.append(temp)

    elif symbol_action == 36: # switch end
        pop_ss(1)  # pops expression
        pb[ss[-1]] = generate_code("JP", i)
        pop_ss(1)  # pops i

    elif symbol_action == 68:  # jp_forward
        pb.append(generate_code("JP", i + 1))
        i = i + 1

    elif symbol_action == 59: # output
        pb.append(generate_code("PRINT", ss[-1]))
        i = i + 1
