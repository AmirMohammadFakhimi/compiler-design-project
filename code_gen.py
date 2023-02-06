ss = []
current_input = None  # TODO
pb = []
i = 0


def generate_code(op, first_op, second_op="", third_op=""):
    return f'({op},{first_op},{second_op},{third_op})'


def pop_ss(num):
    global ss
    for _ in range(num):
        ss.pop()


def getaddr(input):
    pass  # TODO


def gettemp():
    pass  # TODO


def action_routine(symbol_action):
    global current_input, i
    if symbol_action == "pid":
        p = getaddr(current_input)
        ss.append(p)
    elif symbol_action == "pnum":
        ss.append(current_input)
    elif symbol_action == "assign":
        pb[i] = generate_code("ASSIGN", ss[-1], ss[-2], )
        i += 1
        pop_ss(1)
    elif symbol_action == "add":
        t = gettemp()
        pb[i] = generate_code("ADD", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)
    elif symbol_action == "minus":
        t = gettemp()
        pb[i] = generate_code("SUB", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)
    elif symbol_action == "mul":
        t = gettemp()
        pb[i] = generate_code("MULT", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)
    elif symbol_action == "div":
        t = gettemp()
        pb[i] = generate_code("DIV", ss[-2], ss[-1], t)
        i += 1
        pop_ss(2)
        ss.append(t)
    elif symbol_action == "save":
        ss.append(i)
        i += 1
    elif symbol_action == "jpf_save":
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i + 1))
        pop_ss(2)
        ss.append(i)
        i += 1
    elif symbol_action == "label":
        ss.append(i)
    elif symbol_action == "jp":
        pb[ss[-1]] = generate_code("JP", i)
        ss.pop()
    elif symbol_action == "jpf":
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i))
        pop_ss(2)
    elif symbol_action == "while":
        pb[ss[-1]] = generate_code("JPF", ss[-2], str(i + 1))
        pb[i] = generate_code("JP", ss[-3])
        i += 1
        pop_ss(3)
    elif symbol_action == "equal":
        t = gettemp()
        pb[i] = generate_code("EQ", ss[-1], ss[-2], t)
        i += 1
        pop_ss(2)
        ss.append(t)
    elif symbol_action == "lt":
        t = gettemp()
        pb[i] = generate_code("LT", ss[-2], ss[-1], t)
        i += 1
        pop_ss(2)
        ss.append(t)
    elif symbol_action == "get_value":
        addr = ss[-2] + ss[-1]
        ss.append(addr)
