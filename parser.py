import json

terminals: list[str]
non_terminals: list[str]
first: dict[str, list[str]]
follow: dict[str, list[str]]
grammar: dict[str, list[str]]
parse_table: dict[str, dict[str, str]] = dict()

def initial_parser(file_name="grammar/table.json"):
    input_file = open(file_name, 'r')
    data = json.loads(input_file.read())

    terminals = data["terminals"]
    non_terminals = data["non_terminals"]
    terminals = data["terminals"]

    print(data["terminals"])