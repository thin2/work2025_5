def clean_and_slide_columns(board):
    """

    """
    # Make a copy of the board to avoid modify the original board
    new_board = []
    for row in board:
        new_board.append(row)

    rows = len(board)
    columns = len(board[0])

    for column in range(columns):
        for row in range(rows):
            column_chars = [board[row][column] for row in range(rows)]
        non_blank = []
        for char in column_chars:
            if char not in ['', ' ']:
                non_blank.append(char)

        padded = [''] * (rows - len(non_blank)) + non_blank
        for row in range(rows):
            new_board[row][column] = padded[row]
    return new_board


def textoggle_move(board, word_sequence, spare_letters):
    """
    """
    # Make a copy of the board to avoid modify the original board
    new_board = []
    for row in board:
        new_board.append(row)
    for row, column in word_sequence:
        new_board[row][column] = ''
    letter_index = 0
    board_slide = clean_and_slide_columns(new_board)
    for column in range(len(board)):
        # Start from the bottom of each column and upward
        for row in range(len(board[0]) - 1, -1, -1):
            if board_slide[row][column] == '':
                if letter_index < len(spare_letters):
                    # Fill the empty space with a spare letter
                    board_slide[row][column] = spare_letters[letter_index]
                    letter_index += 1
                else:
                    # If there are not enough spare letters avaliable,
                    # the character '#' should be used to indicate
                    # an empty position on the board
                    board_slide[row][column] = '#'
    return board_slide