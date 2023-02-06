from custom_token import Token

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

symbol_table_set = {"if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "endif"}
symbol_table = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "endif"]
tokens: dict[int, list[(str, str)]] = dict()
errors: dict[int, list[(str, str)]] = dict()

class NewSymbolTable:
    symbol_table = []
    empty_address = 100

    def __init__(self, lexeme):
        self.lexeme = lexeme
        self.address = NewSymbolTable.empty_address
        self.type = None
        self.size = 4
        NewSymbolTable.empty_address += self.size

        NewSymbolTable.symbol_table.append(self)

    @staticmethod
    def add_type_to_last_symbol(type):
        NewSymbolTable.symbol_table[-1].type = type

    @staticmethod
    def add_size_to_last_symbol_array(length):
        size = 4 * length
        NewSymbolTable.symbol_table[-1].size = size
        NewSymbolTable.empty_address += size - 4


class State:
    start_state = None
    states = []
    _number = 0

    def __init__(self, name, should_back=False, token=None):
        self.number = State._number
        self.name = name
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
    invalid_input_error = None

    def __init__(self, name, message):
        super(ErrorState, self).__init__(name, False, Token.ERROR)
        self.message = message
        if name == "invalid_input_error":
            ErrorState.invalid_input_error = self


def run_scanner(file_name="input.txt"):
    initial_scanner(file_name)
    while True:
        next_token = get_next_token()
        if next_token == "$":
            break
        else:
            (current_token, lexeme) = next_token
            handle_output_token(current_token, lexeme)


def initial_scanner(file_name="input.txt"):
    initial_DFA()
    global buffer, forward_pointer, buffer_size
    input_file = open(file_name, 'r')
    buffer = input_file.read()
    buffer_size = len(buffer)


def initial_DFA():
    start_state = State("start_state")

    # error states
    unclosed_comment_error = ErrorState("unclosed_comment_error", "Unclosed comment")
    unmatched_comment_error = ErrorState("unmatched_comment_error", "Unmatched comment")
    invalid_number_error = ErrorState("invalid_number_error", "Invalid number")
    ErrorState("invalid_input_error", "Invalid input")

    # digit
    digit_state1 = State("digit_state1")
    digit_state2 = State("digit_state2", True, Token.NUMBER)
    digit_state1.add_all_states({digit: digit_state1, letters: invalid_number_error, other: digit_state2})

    # letter (id & keyword)
    letter_state1 = State("letter_state1")
    letter_state2 = State("letter_state2", True, Token.LETTER)
    letter_state1.add_all_states({letters: letter_state1, digit: letter_state1, other: letter_state2})

    # symbol, p-symbols = {all except ==, =, /, *}
    symbol_state1 = State("symbol_state1", False, Token.SYMBOL)
    symbol_state2 = State("symbol_state2")  # =
    symbol_state3 = State("symbol_state3", False, Token.SYMBOL)  # return ==
    symbol_state4 = State("symbol_state4", True, Token.SYMBOL)  # return =
    symbol_state2.add_all_states({"=": symbol_state3, other: symbol_state4})

    symbol_state5 = State("symbol_state5")  # *
    symbol_state6 = State("symbol_state6", True, Token.SYMBOL)
    symbol_state5.add_all_states({"/": unmatched_comment_error, other: symbol_state6})

    # whitespace
    whitespace1 = State("whitespace1")
    whitespace2 = State("whitespace2", True, Token.WHITE_SPACE)
    whitespace3 = State("whitespace3", False, Token.WHITE_SPACE)
    whitespace1.add_all_states({whitespace: whitespace1, "EOF": whitespace3, other: whitespace2})

    # comment
    comment_state1 = State("comment_state1")  # /
    comment_state2 = State("comment_state2", True, Token.SYMBOL)  # / divide
    comment_state3 = State("comment_state3")  # /*
    comment_state4 = State("comment_state4")  # /* *
    comment_state5 = State("comment_state5", False, Token.COMMENT)  # /* */
    comment_state6 = State("comment_state6")  # //
    comment_state7 = State("comment_state7", True, Token.COMMENT)  # // (\n | EOF)

    comment_state1.add_all_states({"/": comment_state6, "*": comment_state3, other: comment_state2})

    comment_state3.add_all_states({"*": comment_state4, "EOF": unclosed_comment_error, other: comment_state3})
    comment_state4.add_all_states(
        {"*": comment_state4, "/": comment_state5, "EOF": unclosed_comment_error, other: comment_state3})

    comment_state6.add_all_states({"\n": comment_state7, "EOF": comment_state7, other: comment_state6})

    # initial start state
    start_state.add_all_states(
        {
            whitespace: whitespace1,
            digit: digit_state1,
            "/": comment_state1,
            letters: letter_state1,
            p_symbols: symbol_state1,
            "=": symbol_state2,
            "*": symbol_state5
        }
    )


def reset_pointers():
    global forward_pointer, begin_pointer
    forward_pointer = forward_pointer + 1
    begin_pointer = forward_pointer


def get_next_token():
    global forward_pointer, begin_pointer, number_of_line
    if forward_pointer >= buffer_size:
        return "$"
    current_state = State.start_state

    while not current_state.is_final():
        if forward_pointer == len(buffer):
            char = "EOF"
        else:
            char = buffer[forward_pointer]

        if char not in domain and char != "EOF":

            if current_state.name != "comment_state3" and current_state.name != "comment_state4" and current_state.name != "comment_state6":
                current_state = ErrorState.invalid_input_error
        else:
            current_state = current_state.move(char)

        forward_pointer += 1
    forward_pointer -= 1

    if current_state.should_back:
        forward_pointer -= 1

    lexeme = buffer[begin_pointer:forward_pointer + 1]
    number_of_line += lexeme.count("\n")
    reset_pointers()
    if current_state.token == Token.ERROR:
        if current_state.name == "unclosed_comment_error":
            error_line = number_of_line - lexeme.count("\n")
            lexeme = lexeme.strip()
            if len(lexeme) > 7:
                lexeme = lexeme[:7] + "..."
            add_to_error_dict(error_line, lexeme, current_state.message)
        else:
            if current_state.name == "invalid_input_error":
                lexeme = lexeme.strip()
            add_to_error_dict(number_of_line, lexeme, current_state.message)

        return get_next_token()
    elif current_state.token == Token.WHITE_SPACE or current_state.token == Token.COMMENT:
        return get_next_token()
    else:
        current_token: str = current_state.token
        if current_token == Token.LETTER:
            current_token = get_letter_token(lexeme)
        handle_output_token(current_token, lexeme)
        return current_token, lexeme


def get_letter_token(lexeme):
    if lexeme in keywords:
        return Token.KEYWORD
    else:
        return Token.ID


def handle_output_token(current_token, lexeme):
    add_to_dict(tokens, current_token, lexeme)

    if current_token == Token.ID or current_token == Token.KEYWORD:
        add_to_symbol_table(lexeme)


def add_to_symbol_table(lexeme):
    global symbol_table_set, symbol_table
    if lexeme not in symbol_table_set:
        symbol_table.append(lexeme)
        symbol_table_set.add(lexeme)
        NewSymbolTable(lexeme)


def add_to_dict(dictionary, key, value):
    global number_of_line
    if number_of_line not in dictionary:
        dictionary[number_of_line] = []

    dictionary[number_of_line].append((key, value))


def add_to_error_dict(number_line, key, value):
    global errors
    if number_line not in errors:
        errors[number_line] = []

    errors[number_line].append((key, value))
