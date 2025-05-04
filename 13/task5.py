def calculate_value(board):
    """
    Calculates the total points value of all letters on the given board.
    """
    letter_dict = {
        ' ': 0,
        'EAIONRTLSU': 1,
        'DG': 2,
        'BCMP': 3,
        'FHVWY': 4,
        'K': 5,
        'JX': 8,
        'QZ': 10
    }

    point_dict = {}
    for letters, points in letter_dict.items():
        for letter in letters:
            point_dict[letter] = points

    total_point = 0

    for row in board:
        for letter in row:
            if letter in point_dict:
                total_point += point_dict[letter]

    return total_point


letter_dict = {
    ' ': 0, 'EAIONRTLSU': 1, 'DG': 2,
    'BCMP': 3, 'FHVWY': 4, 'K': 5,
    'JX': 8, 'QZ': 10
}
point_dict = {}
for letters, pts in letter_dict.items():
    for ch in letters:
        point_dict[ch] = pts



def word_on_board(word, board):
    """
    Check if a given word can be formed on the board by sequentially selecting adjacent letters.
    """
    if not word:
        return None
    row_count = len(board)
    if row_count == 0:
        return None
    column_count = len(board[0])
    if column_count == 0:
        return None

    direction_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for row in range(row_count):
        for column in range(column_count):
            if board[row][column] == word[0] or board[row][column] == '_':
                path = [(row, column)]
                while len(path) < len(word):
                    row, column = path[-1]
                    path_len = len(path)

                    for change_row, change_column in direction_list:
                        final_row = row + change_row
                        final_column = column + change_column
                        if (0 <= final_row < row_count
                                and 0 <= final_column < column_count
                                and (final_row, final_column) not in path
                                and (board[final_row][final_column] == word[len(path)]
                                     or board[final_row][final_column] == '_')):
                            path.append((final_row, final_column))
                            break
                    if len(path) == path_len:
                        break
                if len(path) == len(word):
                    return path
    return None


def clean_and_slide_columns(board):
    """
    Slide down the columns and fill empty spots with blank or '#'.
    """
    new_board = [row[:] for row in board]
    rows = len(board)
    columns = len(board[0])

    for column in range(columns):
        column_chars = [board[row][column] for row in range(rows)]
        non_blank = [char for char in column_chars if char not in ['', ' ']]
        padded = [''] * (rows - len(non_blank)) + non_blank
        for row in range(rows):
            new_board[row][column] = padded[row]

    return new_board


def textoggle_move(board, word_sequence, spare_letters):
    """
    Make the best move on the board, removing the word and sliding the letters.
    """
    new_board = [row[:] for row in board]
    for row, column in word_sequence:
        new_board[row][column] = ''

    letter_index = 0
    board_slide = clean_and_slide_columns(new_board)

    for column in range(len(board[0])):
        for row in range(len(board) - 1, -1, -1):
            if board_slide[row][column] == '':
                if letter_index < len(spare_letters):
                    board_slide[row][column] = spare_letters[letter_index]
                    letter_index += 1
                else:
                    board_slide[row][column] = '#'
            elif board_slide[row][column] == '_':
                if letter_index < len(spare_letters):
                    board_slide[row][column] = spare_letters[letter_index]
                    letter_index += 1

    return board_slide


def create_letter_count(board):
    """
    Create a dictionary that counts the number of times each letter appears on the board.
    """
    all_elements_list = []
    for row in board:
        for letter in row:
            all_elements_list.append(letter)

    all_elements_dict = {}
    for letter in all_elements_list:
        if letter in all_elements_dict:
            all_elements_dict[letter] += 1
        else:
            all_elements_dict[letter] = 1

    universal_letter_count = all_elements_dict.get('_', 0)

    return all_elements_dict, universal_letter_count


def count_word_letters(word):
    """
    Count how many times each letter appears in a word.
    """
    letter_count = {}
    for letter in word:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1
    return letter_count


def is_word_valid(word, all_elements_dict, universal_letter_count, allow_blank_for_first_letter=False):
    """
    Check if a word can be formed using the letters on the board.
    """
    letter_count = count_word_letters(word)
    needed_universal_letter = 0

    if word[0] == '_':  # Check if first letter is '_'
        allow_blank_for_first_letter = True

    for letter, needed_letter in letter_count.items():
        available_letter = all_elements_dict.get(letter, 0)

        if needed_letter > available_letter:
            needed_universal_letter += needed_letter - available_letter

    if allow_blank_for_first_letter:
        needed_universal_letter -= letter_count.get('_', 0)  # Deduct the first letter '_'

    return needed_universal_letter <= universal_letter_count


def words_on_board(words, board):
    """
    Check which words in the list can be formed using the available letters and blanks.
    """
    all_elements_dict, universal_letter_count = create_letter_count(board)

    output_list = []
    for word in words:
        allow_blank_for_first_letter = word[0] == '_'
        if is_word_valid(word, all_elements_dict, universal_letter_count, allow_blank_for_first_letter):

            output_list.append(word)

    return output_list


def play_best_game(board, spare_letters):
    """
    Play the best game by choosing the highest-scoring word and updating the board.
    """
    with open('words_alpha.txt') as f:
        word_list = [line.strip().upper() for line in f if line.strip()]

    total_score = 0
    spare_index = 0
    round_num = 1
    current_board = [row[:] for row in board]

    while True:
        found = []
        for word in word_list:
            seq = word_on_board(word, current_board)
            if seq is not None:
                base = 0
                for (r, c), ch in zip(seq, word):
                    if current_board[r][c] != '_':
                        base += point_dict.get(ch, 0)
                round_score = base * len(word)
                found.append((round_score, word, seq))
        if not found:
            break

        found.sort(key=lambda x: (-x[0], -len(x[1]), x[1]))
        best_score, best_word, best_path = found[0]
        total_score += best_score

        needed = len(best_path)
        new_letters = spare_letters[spare_index:spare_index + needed]
        spare_index += needed
        current_board = textoggle_move(current_board, best_path, new_letters)
        round_num += 1

    return total_score



print(play_best_game([['R', 'U', 'N'], ['R', 'E', 'N'], ['X', 'X', 'X']], ['T','R','T','A','T','N','T'])
)
print(play_best_game([['R', '_', 'N'], ['R', 'E', 'N'], ['X', 'X', 'X']], ['T','R','T','A','T','N','T']))



