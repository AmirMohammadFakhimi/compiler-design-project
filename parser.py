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


def initial_parser(file_name="grammar/table.json"):
    global parse_table, grammar,follow

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


def run_parser(file_name="grammar/table.json"):
    global parse_table, grammar, node_stack, stack,follow,root
    initial_parser(file_name)
    top_token = scanner.get_next_token()

    while (True):
        top_stack = stack[-1]

        top_input = get_top_input(top_token)

        if top_input in parse_table[top_stack].keys():
            action = parse_table[top_stack][top_input].split('_')
        else:
            action = ["error"]
        print(action)
        if action[0] == "shift":
            stack.append(top_input)
            stack.append(action[1])
            node_stack.append(anytree.Node(top_token))
            top_token = scanner.get_next_token()
        elif action[0] == "reduce":
            action_grammar = grammar[action[1]]
            number_of_remove_from_stack = (len(action_grammar) - action_grammar.count('epsilon') - 2) * 2
            for _ in range(number_of_remove_from_stack):
                stack.pop()

            stack.append(action_grammar[0])
            next_state = parse_table[stack[-2]][stack[-1]].split('_')[1]
            children = node_stack[-number_of_remove_from_stack:]
            node_stack = node_stack[:-number_of_remove_from_stack]
            node_stack.append(anytree.Node(action_grammar[0], children=children))
            stack.append(next_state)
        elif action[0] == "accept":
            root = anytree.Node('program', children=node_stack)
            break
        elif action[0] == "error":
            errors.append(f'#{scanner.number_of_line} : syntax error , illegal {top_input}')

            while True:
                stack_item_state = stack[-1]
                stack_item_row = parse_table[stack_item_state]
                gotos_key = []

                for stack_item_input in stack_item_row.keys():
                    if stack_item_row[stack_item_input].startswith('goto'):
                        gotos_key.append(stack_item_input)

                gotos_key.sort()
                if len(gotos_key) > 0:
                    stack.append(gotos_key[0])
                    next_grammar_number = stack_item_row[gotos_key[0]].split('_')[1]
                    stack.append(next_grammar_number)

                    # iterate over input until find a follow of the desired non terminal
                    while top_input not in follow[grammar[next_grammar_number][0]]:
                        if top_input == "$":
                            return

                        top_input = get_top_input(top_token)

                    break
                else:
                    stack.pop()
                    stack.pop()
