def word_on_board(word, board):
    row_count = len(board)
    column_count = len(board[0])

    direction_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for row in range(row_count):
        for column in range(column_count):
            if board[row][column] == word[0]:
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
                                and (board[final_row][final_column]
                                     == word[len(path)])
                        ):
                            path.append((final_row, final_column))
                            break
                    if len(path) == path_len:
                        break

                if len(path) == len(word):
                    return path
    return None

