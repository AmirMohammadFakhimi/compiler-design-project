buffer = ""
buffer_size = 0
begin_pointer = 0
forward_pointer = 0
number_of_line = 1

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digit = "0123456789"
whitespace = "\n\f\r\v\t "
p_symbols = ";:,[](){}+-*<"
other = "other"
keywords = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "endif"]


class Token:
    LETTER = "LETTER"
    NUMBER = "NUMBER"
    SYMBOL = "SYMBOL"
    ID = "ID"
    KEYWORD = "KEYWORD"
    COMMENT = "COMMENT"
    WHITE_SPACE = "WHITESPACE"


class State:
    start_state = None
    states = []
    _number = 0

    def __init__(self, should_back=False, token=None):
        self.number = State._number
        self.should_back = should_back
        self.token = token
        self._destination_states = dict()
        State.states.append(self)
        if State._number == 0:
            State.start_state = self
        State._number += 1

    def is_final(self):
        return self.token is not None

    def add_all_states(self, states: dict, not_split_keys=None):
        if not_split_keys is None:
            not_split_keys = ["other"]
        for key in states:
            self._add_dest_state(key, states[key], key not in not_split_keys)

    def _add_dest_state(self, input_letters, destination_state, should_split=True):
        if should_split:
            for letter in input_letters:
                self._destination_states[letter] = destination_state
        else:
            self._destination_states[input_letters] = destination_state

    def move(self, input_letter):
        if input_letter not in self._destination_states.keys():
            if other in self._destination_states.keys():
                return self._destination_states["other"]
            else:
                reset_pointers()
                return State.start_state
        return self._destination_states[input_letter]


class ErrorState(State):
    def __init__(self, message):
        super(State, self).__init__()
        self.message = message


def initial_input_file():
    initial_DFA()
    global buffer, forward_pointer, buffer_size
    input_file = open("input.txt", 'r')
    token_file = open("tokens.txt", 'w')
    lexeme_error_file = open("lexical_errors.txt", 'w')
    symbol_table_file = open("symbol_table.txt", 'w')
    buffer = input_file.read()
    buffer_size = len(buffer)
    while forward_pointer < buffer_size:
        get_next_token()


def initial_DFA():
    start_state = State()

    # digit
    digit_state1 = State()
    digit_state2 = State(True, Token.NUMBER)
    digit_state1.add_all_states({digit: digit_state1, other: digit_state2})

    # letter (id & keyword)
    letter_state1 = State()
    letter_state2 = State(True, Token.LETTER)
    letter_state1.add_all_states({letters: letter_state1, other: letter_state2})

    # symbol, p-symbols = {all except ==, =, /}
    symbol_state1 = State(False, Token.SYMBOL)
    symbol_state2 = State()
    symbol_state3 = State(False, Token.SYMBOL)
    symbol_state4 = State(True, Token.SYMBOL)
    symbol_state2.add_all_states({"=": symbol_state3, other: symbol_state4})

    # whitespace
    whitespace1 = State()
    whitespace2 = State(True, Token.WHITE_SPACE)
    whitespace1.add_all_states({whitespace: whitespace1, other: whitespace2})

    # comment
    comment_state1 = State()
    comment_state2 = State(False, Token.SYMBOL)
    comment_state3 = State()
    comment_state4 = State()
    comment_state5 = State()
    comment_state6 = State(True, Token.COMMENT)

    comment_state1.add_all_states({"/": comment_state6, "*": comment_state3, other: comment_state2})
    comment_state6.add_all_states({"\n": comment_state5, "EOF": comment_state5, other: comment_state6})
    comment_state3.add_all_states({"*": comment_state4, other: comment_state3})
    comment_state4.add_all_states({"*": comment_state4, "/": comment_state5, other: comment_state3})

    # initial start state
    start_state.add_all_states(
        {
            whitespace: whitespace1,
            digit: digit_state1,
            "/": comment_state1,
            letters: letter_state1,
            p_symbols: symbol_state1,
            "=": symbol_state2,
        }
    )


def reset_pointers():
    global forward_pointer, begin_pointer
    forward_pointer = forward_pointer + 1
    begin_pointer = forward_pointer


def get_next_token():
    global forward_pointer, begin_pointer, number_of_line
    temp_state = State.start_state

    while not temp_state.is_final():
        if forward_pointer == len(buffer):
            char = "EOF"
        else:
            char = buffer[forward_pointer]

        if char == "\n":
            number_of_line += 1
        temp_state = temp_state.move(char)
        forward_pointer += 1
    forward_pointer -= 1

    if temp_state.should_back:
        forward_pointer -= 1

    lexeme = buffer[begin_pointer:forward_pointer + 1]
    reset_pointers()
    print(lexeme + ":" + temp_state.token)


def get_letter_token(lexeme):
    if lexeme in keywords:
        return Token.KEYWORD
    else:
        return Token.ID


def save_token(lexeme, token):
    if token != token.WHITE_SPACE and token != token.COMMENT:
        pass
