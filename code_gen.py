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
    current_input = parser.get_top_input(parser.top_token)
    symbol_action = int(symbol_action)
    if symbol_action == 66: #pid
        p = getaddr(current_input)
        ss.append(p)

    elif symbol_action == 67: #pnum
        ss.append(current_input)
    elif symbol_action == "assign":
        pb[i] = generate_code("ASSIGN", ss[-1], ss[-2], )
        i += 1
        pop_ss(1)

    elif symbol_action == 50: #add
        t = gettemp()
        pb[i] = generate_code("ADD", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 52: #sub
        t = gettemp()
        pb[i] = generate_code("SUB", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 53: #mul
        t = gettemp()
        pb[i] = generate_code("MULT", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 55: #div
        t = gettemp()
        pb[i] = generate_code("DIV", ss[-2], ss[-1], t)
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 72: #save
        ss.append(i)
        i += 1

    elif symbol_action == 68: #jpf_save
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i + 1))
        pop_ss(2)
        ss.append(i)
        i += 1

    elif symbol_action == 69: #label
        ss.append(i)

    elif symbol_action == 33: #jp
        pb[ss[-1]] = generate_code("JP", i)
        ss.pop()

    elif symbol_action == 32: #jpf
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i))
        pop_ss(2)

    elif symbol_action == 34: #while
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i + 1))
        pb[i] = generate_code("JP", ss[-3])
        i += 1
        pop_ss(4)

    elif symbol_action == 49: #equal
        t = gettemp()
        pb[i] = generate_code("EQ", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 47: # lt
        t = gettemp()
        pb[i] = generate_code("LT", ss[-2], ss[-1], t)
        i += 1
        pop_ss(2)
        ss.append(t)

    elif symbol_action == 46: # get_value
        addr = ss[-2] + ss[-1]
        ss.append(addr)
    
    elif symbol_action == 29: # pop
        ss.pop()

    elif symbol_action == 30: # break action
        pb[i] = generate_code("JP",ss[-4])
        i += 1
    
    elif symbol_action == 71: #switch_compare
        temp = gettemp()
        pb[i] = generate_code('EQ', ss[-2], ss[-1], temp)
        i += 1
        pop_ss(1)
        ss.append(temp)

    elif symbol_action == 37:
        pop_ss(1) # pops expression
        pb[ss[-1]] = generate_code("JP",i)
        pop_ss(1) # pops i

    elif symbol_action == 70: #jp_forward
        pb[i] = generate_code("JP",i+1)
        i=i+1
    
    elif symbol_action == 65:
        pb[i] = generate_code("PRINT",ss[-1])
        i=i+1