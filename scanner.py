buffer = ""
begin_pointer = 0
forward_pointer = 0
start_state = None
number_of_line = 1

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digit = "0123456789"
whitespace = "\n\f\r\v\t" + chr(32)
symbols = ";:,[](){}+-*=</"
other = "other"


class State:
    states = []
    _number = 0
    _destination_states = dict()

    def __init__(self, should_back=False, token=None):
        self.number = State._number
        self.should_back = should_back
        self.token = token
        State.states.append(self)
        State._number += 1

    def is_final(self):
        return self.token != None

    def add_all_states(self, states: dict, not_split_keys=None):
        if not_split_keys is None:
            not_split_keys = ["other"]
        for key, value in states:
            self.add_dest_state(key, value, key not in not_split_keys)

    def add_dest_state(self, input_letters, destination_state, should_split=True):
        if should_split:
            for letter in input_letters:
                self._destination_states[letter] = destination_state
        else:
            self._destination_states[input_letters] = destination_state

    def move(self, input_letter):
        if input_letter not in self._destination_states.keys():
            return self._destination_states["other"]
        return self._destination_states[input_letter]


def initial_input_file():
    global buffer
    file = open("input.txt", 'r')
    buffer = file.read()


def initial_DFA():
    global start_state
    start_state = State()

    # digit
    digit_state1 = State()
    digit_state2 = State(True, "NUMBER")
    digit_state1.add_all_states({digit: digit_state1, other: digit_state2})

    # letter
    digit_state1 = State()
    digit_state2 = State(True, "NUMBER")
    digit_state1.add_all_states({digit: digit_state1, other: digit_state2})


    # comment
    comment_state1 = State()
    comment_state2 = State(True, "SYMBOL")
    comment_state3 = State()
    comment_state4 = State()
    comment_state5 = State()
    comment_state6 = State(True, "COMMENT")
    # TODO add all start state


def get_next_token():
    pass
