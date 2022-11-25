import token

buffer = ""
buffer_size = 0
begin_pointer = 0
forward_pointer = 0
number_of_line = 1

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digit = "0123456789"
whitespace = "\n\f\r\v\t "
p_symbols = ";:,[](){}+-<"
domain = letters + digit + whitespace + p_symbols + "*=/"

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
    ERROR = "ERROR"


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
            not_split_keys = ["other", "EOF"]
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
        super(ErrorState, self).__init__(False, Token.ERROR)
        self.message = message


def initial_input_file():
    initial_DFA()
    global buffer, forward_pointer, buffer_size
    input_file = open("input.txt", 'r')
    # token_file = open("tokens.txt", 'w')
    # lexeme_error_file = open("lexical_errors.txt", 'w')
    # symbol_table_file = open("symbol_table.txt", 'w')
    buffer = input_file.read()
    buffer_size = len(buffer)
    while forward_pointer < buffer_size:
        get_next_token()


def initial_DFA():
    start_state = State()

    # error states
    invalid_input_error = ErrorState("Invalid input")
    unclosed_comment_error = ErrorState("Unclosed comment")
    unmatched_comment_error = ErrorState("Unmatched comment")
    invalid_number_error = ErrorState("Invalid number")

    # digit
    digit_state1 = State()
    digit_state2 = State(True, Token.NUMBER)
    digit_state1.add_all_states({digit: digit_state1, letters: invalid_number_error, other: digit_state2})

    # letter (id & keyword)
    letter_state1 = State()
    letter_state2 = State(True, Token.LETTER)
    letter_state1.add_all_states({letters: letter_state1, other: letter_state2})

    # symbol, p-symbols = {all except ==, =, /, *}
    symbol_state1 = State(False, Token.SYMBOL)
    symbol_state2 = State()  # =
    symbol_state3 = State(False, Token.SYMBOL)  # return ==
    symbol_state4 = State(True, Token.SYMBOL)  # return =
    symbol_state2.add_all_states({"=": symbol_state3, other: symbol_state4})

    symbol_state5 = State()  # *
    symbol_state6 = State(True, Token.SYMBOL)
    symbol_state5.add_all_states({"/": unmatched_comment_error, other: symbol_state6})

    # whitespace
    whitespace1 = State()
    whitespace2 = State(True, Token.WHITE_SPACE)
    whitespace1.add_all_states({whitespace: whitespace1, other: whitespace2})

    # comment
    comment_state1 = State()  # /
    comment_state2 = State(True, Token.SYMBOL)  # / divide
    comment_state3 = State()  # /*
    comment_state4 = State()  # /* *
    comment_state5 = State(False, Token.COMMENT)
    comment_state6 = State()  # //

    comment_state1.add_all_states({"/": comment_state6, "*": comment_state3, other: comment_state2})

    comment_state3.add_all_states({"*": comment_state4, "EOF": unclosed_comment_error, other: comment_state3})
    comment_state4.add_all_states(
        {"*": comment_state4, "/": comment_state5, "EOF": unclosed_comment_error, other: comment_state3})

    comment_state6.add_all_states({"\n": comment_state5, "EOF": comment_state5, other: comment_state6})

    # initial start state
    start_state.add_all_states(
        {
            whitespace: whitespace1,
            digit: digit_state1,
            "/": comment_state1,
            letters: letter_state1,
            p_symbols: symbol_state1,
            "=": symbol_state2,
            "*": symbol_state5,
            other: invalid_input_error
        }
    )


def reset_pointers():
    global forward_pointer, begin_pointer
    forward_pointer = forward_pointer + 1
    begin_pointer = forward_pointer


def get_next_token():
    global forward_pointer, begin_pointer, number_of_line,domain
    current_state = State.start_state

    while not current_state.is_final():
        if forward_pointer == len(buffer):
            char = "EOF"
        else:
            char = buffer[forward_pointer]
            if char not in domain:
                # TODO invalid input state error
                pass


        if char == "\n":
            number_of_line += 1
            print()
            print(str(number_of_line) + " : ", end=" ")
        current_state = current_state.move(char)
        forward_pointer += 1
    forward_pointer -= 1

    if current_state.should_back:
        forward_pointer -= 1

    lexeme = buffer[begin_pointer:forward_pointer + 1]
    reset_pointers()
    if current_state.token == Token.ERROR:
        if len(lexeme) > 7:
            lexeme = lexeme[:7] + "..."
        print("(Error " + current_state.message + " : " + lexeme + ")", end=" ")
        get_next_token()
    elif current_state.token != Token.WHITE_SPACE and current_state.token != Token.COMMENT:
        current_token = current_state.token
        if current_token == Token.LETTER:
            current_token = get_letter_token(lexeme)
        return current_token, lexeme


def get_letter_token(lexeme):
    if lexeme in keywords:
        return Token.KEYWORD
    else:
        return Token.ID

def panic():
    reset_pointers()