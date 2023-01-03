import json
import scanner
from token import Token

terminals: list[str]
non_terminals: list[str]
first: dict[str, list[str]]
follow: dict[str, list[str]]
grammar: dict[str, list[str]]
parse_table: dict[str, dict[str, str]]
stack = ["0"]

errors = []

def initial_parser(file_name="grammar/table.json"):
    global parse_table, grammar

    input_file = open(file_name, 'r')
    data = json.loads(input_file.read())
    terminals = data["terminals"]
    non_terminals = data["non_terminals"]
    first = data["first"]
    follow = data["follow"]
    grammar = data["grammar"]
    parse_table = data["parse_table"]
    
def run_parser():
    global parse_table, grammar

    while (True):
        top_stack = stack[-1]
        top_token = scanner.get_next_token()
        top_input = None
        if top_token == Token.KEYWORD or top_token == Token.SYMBOL:
            top_input = top_token[1]
        else:
            top_input = top_token[0]

        print(top_stack, )
        if top_input in parse_table[top_stack].keys():
            action = parse_table[top_stack][top_input].split('_')
        else:
            action = ["error"]
        
        if action[0] == "shift":
            stack.append(top_input)
            stack.append(action[1])
        elif action[0] == "reduce":
            action_grammer = grammar[action[1]]
            number_of_remove_from_stack = (len(action_grammer) - 2) * 2
            for _ in range(number_of_remove_from_stack):
                stack.pop()
            
            stack.push(action_grammer[0])
            next_state = parse_table[stack[-2]][stack[-1]].split('_')[1]
            stack.push(next_state)
        elif action[0] == "accept":
            break
        elif action[0] == "error":
            pass
    
    
    if len(errors) == 0:
        errors.append("There is no syntax error.")
