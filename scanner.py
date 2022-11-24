buffer = ""
begin_pointer = 0
forward_pointer = 0
states = []
start_state = None
number_of_line = 1

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
whitespace = "\n\f\r\v\t" + chr(32)
symbols = ";:,[](){}+-*=</"


class State:
    _destination_states = dict()

    def __init__(self, number):
        self.number = number

    def add_dest_state(self, input_letters, destination_state):
        for letter in input_letters:
            self._destination_states[letter] = destination_state

    def move(self, input_letter):
        return self._destination_states[input_letter]


def initial_input_file():
    global buffer
    file = open("input.txt", 'r')
    buffer = file.read()


def initial_DFA():
    global states, start_state
    start_state = State(0)
    start_state.add_dest_state("")


def get_next_token():
    pass
