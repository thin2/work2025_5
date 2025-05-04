def calculate_value(board):
    """
    Calculates the total points value of all letters on the given board.
    """

    # Create a dictionary to store the letter and
    # their corresponding point value.
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

    # Create a dictionary to store the point value for each letter.
    point_dict = {}
    for letters, points in letter_dict.items():
        for letter in letters:
            point_dict[letter] = points

    # Initialize the total point
    total_point = 0

    # Iterates through each row of the given board
    for row in board:
        # Iterates through each letter in the current row
        for letter in row:
            # Check if the letter in point_dict
            # and add all points into the total points
            if letter in point_dict:
                total_point += point_dict[letter]
    return total_point
# print(calculate_value([['A', 'A', 'A'], ['B', 'B', 'B'], ['C', 'C', 'C']]))