import json
import scanner
from custom_token import Token
import anytree

terminals: list[str]
non_terminals: list[str]
first: dict[str, list[str]]
follow: dict[str, list[str]]
grammar: dict[str, list[str]]
parse_table: dict[str, dict[str, str]]
stack = ["0"]
node_stack = []
root = None
errors = []
tokens = {}


def initial_parser(file_name="grammar/table.json"):
    global parse_table, grammar, follow, non_terminals, terminals, first

    input_file = open(file_name, 'r')
    data = json.loads(input_file.read())
    terminals = data["terminals"]
    non_terminals = data["non_terminals"]
    first = data["first"]
    follow = data["follow"]
    grammar = data["grammar"]
    parse_table = data["parse_table"]


def get_top_input(top_token):
    if top_token[0] == Token.KEYWORD or top_token[0] == Token.SYMBOL:
        return top_token[1]
    else:
        return top_token[0]


def get_parse_tree():
    result = ""
    for pre, _, node in anytree.RenderTree(root):
        result += pre + node.name + '\n'
    return result


def run_parser(file_name="grammar/table.json"):
    global parse_table, grammar, node_stack, stack, follow, root, non_terminals
    initial_parser(file_name)
    top_token = scanner.get_next_token()

    while True:
        top_stack = stack[-1]

        top_input = get_top_input(top_token)
        tokens[top_input] = top_token[0]

        if top_input in parse_table[top_stack].keys():
            action = parse_table[top_stack][top_input].split('_')
        else:
            action = ["error"]
        if action[0] == "shift":
            stack.append(top_input)
            stack.append(action[1])
            if top_token == '$':
                node_stack.append(anytree.Node(top_token))
            else:
                node_stack.append(anytree.Node('(' + str(top_token[0]) + ', ' + str(top_token[1]) + ')'))
            top_token = scanner.get_next_token()
        elif action[0] == "reduce":

            action_grammar = grammar[action[1]]
            number_of_rhs = (len(action_grammar) - action_grammar.count('epsilon') - 2)
            for _ in range(number_of_rhs * 2):
                stack.pop()
            children = []
            for _ in range(number_of_rhs):
                children.append(node_stack.pop())
            children.reverse()
            if action_grammar.count('epsilon') > 0:
                children.append(anytree.Node('epsilon'))
            stack.append(action_grammar[0])
            next_state = parse_table[stack[-2]][stack[-1]].split('_')[1]
            stack.append(next_state)
            node_stack.append(anytree.Node(action_grammar[0], children=children))
        elif action[0] == "accept":
            node = node_stack.pop()
            root = node_stack.pop()
            children = list(root.children)
            children.append(node)
            root = anytree.Node(root.name, children=children)
            break

        elif action[0] == "error":
            errors.append(f'#{scanner.number_of_line} : syntax error , illegal {top_input}')

            while True:
                stack_item_state = stack[-1]
                stack_item_row = parse_table[stack_item_state]
                goto_keys = []

                for stack_item_input in stack_item_row.keys():
                    if stack_item_row[stack_item_input].startswith('goto'):
                        goto_keys.append(stack_item_input)

                goto_keys.sort()
                if len(goto_keys) > 0:
                    top_token = scanner.get_next_token()
                    top_input = get_top_input(top_token)
                    tokens[top_input] = top_token[0]

                    if top_input == "$":
                        errors.append(f'syntax error, Unexpected EOF')
                        return

                    is_break = False
                    for i in range(len(goto_keys)):
                        if top_input in follow[goto_keys[i]]:
                            stack.append(goto_keys[i])
                            errors.append(f'#{scanner.number_of_line} : syntax error , missing {goto_keys[i]}')
                            next_grammar_number = stack_item_row[goto_keys[i]].split('_')[1]
                            stack.append(next_grammar_number)
                            is_break = True
                            break

                    if is_break:
                        break
                    else:
                        errors.append(f'#{scanner.number_of_line} : syntax error , discarded {top_input} from input')





                    # stack.append(goto_keys[0])
                    # errors.append(f'#{scanner.number_of_line} : syntax error , missing {goto_keys[0]}')
                    # next_grammar_number = stack_item_row[goto_keys[0]].split('_')[1]
                    # stack.append(next_grammar_number)
                    #
                    # # iterate over input until find a follow of the desired non-terminal
                    # top_token = scanner.get_next_token()
                    # top_input = get_top_input(top_token)
                    # tokens[top_input] = top_token[0]
                    # while top_input not in follow[goto_keys[0]]:
                    #     if top_input == "$":
                    #         errors.append(f'syntax error, Unexpected EOF')
                    #         return
                    #
                    #     top_token = scanner.get_next_token()
                    #     top_input = get_top_input(top_token)
                    #     tokens[top_input] = top_token[0]
                    #     errors.append(f'#{scanner.number_of_line} : syntax error , discarded {top_input} from input')
                    #
                    # break
                else:
                    stack.pop()
                    stack_pop = stack.pop()
                    if stack_pop in non_terminals:
                        errors.append(f'syntax error , discarded {stack_pop} from stack')
                    else:
                        errors.append(f'syntax error , discarded ({stack_pop}, {stack_pop}) from stack')