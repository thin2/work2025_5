def create_letter_count(board):
    """
    Create a dictionary that counts the number of times
    each letter (and blank) appears on the board.
    Blanks are represented by '_'.
    """
    all_elements_list = []
    # Extract all letters from the board into a list
    for row in board:
        for letter in row:
            all_elements_list.append(letter)

    # Create a dictionary with the numbers of each letter
    all_elements_dict = {}
    for letter in all_elements_list:
        if letter in all_elements_dict:
            all_elements_dict[letter] += 1
        else:
            all_elements_dict[letter] = 1

    # Check if there are any blanks ('_') on the board
    universal_letter_count = all_elements_dict.get('_', 0)

    return all_elements_dict, universal_letter_count


def count_word_letters(word):
    """
    Count how many times each letter appears in a given word.
    """
    letter_count = {}
    for letter in word:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1
    return letter_count



def is_word_valid(word, all_elements_dict, universal_letter_count):
    """
    Check if a word can be formed using the letters on the board.
    A word is valid if the number of required letters is less than or equal to
    the available letters plus the universal letters (blanks).
    """
    letter_count = count_word_letters(word)
    needed_universal_letter = 0

    for letter, needed_letter in letter_count.items():
        available_letter = all_elements_dict.get(letter, 0)

        if needed_letter > available_letter:
            needed_universal_letter += needed_letter - available_letter

    return needed_universal_letter <= universal_letter_count


def words_on_board(words, board):
    """
    Check which words in the list can be formed
    using the available letters and blanks on the board.
    """
    # Step 1: Get the letter counts from the board
    all_elements_dict, universal_letter_count = create_letter_count(board)

    # Step 2: For each word, check if it's valid
    output_list = []
    for word in words:
        if is_word_valid(word, all_elements_dict, universal_letter_count):
            output_list.append(word)

    return output_list