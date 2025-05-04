import random

foundation = [[None for _ in range(4)] for _ in range(13)]
output_lines = []

suit_to_column = {0: 3, 1: 0, 2: 1, 3: 2}
column_to_return = {3: 0, 0: 1, 2: 3, 1: 2}

def record_output(text):
    output_lines.append(text.rstrip() if text else "")
def card_value(card):

    return (card % 13) + 1

def card_suit(card):

    return card // 13

def unicode_for_card(card):

    card_unicode = [
        '🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾',  # 红桃
        '🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎',  # 方块
        '🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞',  # 梅花
        '🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'   # 黑桃
    ]
    return card_unicode[card]

def create_shuffled_deck(seed_val):

    random.seed(seed_val)
    deck = list(set(range(52)) - {6, 19, 32, 45})
    random.shuffle(deck)
    return deck

def initialize_foundation():
    for card in [6, 32, 45, 19]:
        col = suit_to_column[card_suit(card)]
        foundation[6][col] = 7

def show_foundation():

    for row in range(13):
        row_disp = []
        for col in range(4):
            if foundation[row][col] is None:
                row_disp.append("")
            else:

                orig_card = foundation[row][col] + column_to_return.get(col) * 13 - 1
                row_disp.append(f"{unicode_for_card(orig_card)}")
        record_output('\t' + '\t'.join(row_disp))
    record_output('')

def check_placement(card):

    value = card_value(card)
    suit = card_suit(card)
    col = suit_to_column[suit]

    if value > 7:
        target_row = 6 - (value - 7)
        if not (0 <= target_row <= 5):
            return False, None, None
        if foundation[target_row][col] is not None:
            return False, None, None
        if value == 8:
            if foundation[6][col] == 7:
                return True, target_row, col
        else:
            if foundation[target_row + 1][col] == value - 1:
                return True, target_row, col
        return False, None, None

    elif value < 7:
        target_row = 6 + (7 - value)
        if not (7 <= target_row <= 12):
            return False, None, None
        if foundation[target_row][col] is not None:
            return False, None, None
        if value == 6:
            if foundation[6][col] == 7:
                return True, target_row, col
        else:
            if foundation[target_row - 1][col] == value + 1:
                return True, target_row, col
        return False, None, None

    else:
        return False, None, None

def place_card_on_foundation(card, source_class):
    valid, target_row, target_col = check_placement(card)
    if valid:
        foundation[target_row][target_col] = card_value(card)
        if source_class == 1:
            record_output("Placing card from top of stack of cards left 😊")
        elif source_class == 2:
            record_output("Placing card from top of stack of cards put aside 😊")
        return True
    else:
        if source_class == 1:
            record_output("Cannot place card from top of stack of cards left ☹️")
        elif source_class == 2:
            record_output("Cannot place card from top of stack of cards put aside ☹️")
    return False

def process_waste_pile(stock, waste):

    for _ in range(1000):
        if not waste:
            break
        modified = False
        top_waste = waste[-1]
        if place_card_on_foundation(top_waste, 2):
            waste.pop()
            record_output("]" * len(stock))
            if waste:
                record_output("[" * (len(waste) - 1) + unicode_for_card(waste[-1]))
            else:
                record_output('')
            show_foundation()
            modified = True
        else:
            record_output('')
        if not modified:
            break

def round_order(n):
    orders = ['first', 'second', 'third', 'fourth']
    return orders[n]

def play_round(stock, waste):
    while stock:
        current_card = stock.pop(0)
        if place_card_on_foundation(current_card, 1):
            record_output("]" * len(stock))
            if waste:
                record_output("[" * (len(waste) - 1) + unicode_for_card(waste[-1]))
            else:
                record_output('')
            show_foundation()
            process_waste_pile(stock, waste)
        else:
            waste.append(current_card)
            record_output("]" * len(stock))
            record_output("[" * (len(waste) - 1) + unicode_for_card(waste[-1]))
            record_output('')
    return stock, waste

def play_game(seed_val):
    global foundation
    foundation = [[None for _ in range(4)] for _ in range(13)]
    initialize_foundation()
    record_output("All 7s removed and placed, rest of deck shuffled, ready to start!")
    stock = create_shuffled_deck(seed_val)[::-1]
    record_output(']' * len(stock))
    record_output('')
    show_foundation()
    waste = []
    for phase in range(3):
        if phase == 0:
            record_output(f"Starting {round_order(phase)} round...")
        else:
            record_output('')
            record_output(f"Starting {round_order(phase)} round...")
        record_output('')
        stock, waste = play_round(stock, waste)
        complete = True
        for col in range(4):
            if sum(1 for row in range(13) if foundation[row][col] is not None) != 13:
                complete = False
                break
        if complete:
            record_output("You placed all cards, you won 👍")
            return 0
        if phase < 2:
            stock = waste
            waste = []
    record_output(f"You could not place {len(stock) + len(waste)} cards, you lost 👎")
    return len(stock) + len(waste)

def simulate(n, i):

    outcomes = {}
    for j in range(n):
        leftover = play_game(i + j)
        outcomes[leftover] = outcomes.get(leftover, 0) + 1
    results = []
    for leftover, count in outcomes.items():
        prob = (count / n) * 100
        results.append((leftover, prob))
    results.sort(key=lambda x: x[0], reverse=True)
    print('Number of cards left | Frequency')
    print('--------------------------------')
    for leftover, prob in results:
        if prob < 0.005:
            prob = 0.00
        line = f"{leftover} |   {prob :>6.2f}%".rjust(32)
        print(line.ljust(32))

if __name__ == '__main__':
    seed_input = int(input("Please enter an integer to feed the seed() function: "))
    play_game(seed_input)
    print()
    print(f'There are {len(output_lines)} lines of output; what do you want me to do?')
    print()
    total_lines = len(output_lines)
    while True:
        print('Enter: q to quit')
        print(f'       a last line number (between 1 and {total_lines})')
        print(f'       a first line number (between -1 and -{total_lines})')
        print("       a range of line numbers (of the form m--n with 1 <= m <= n <= {})".format(total_lines))
        user_cmd = input('       ').strip()
        if user_cmd == 'q':
            break
        elif user_cmd.isdigit():
            print()
            num = int(user_cmd)
            if 1 <= num <= total_lines:
                for line in output_lines[:num]:
                    print(line)
            print()
        elif user_cmd.startswith('-') and user_cmd[1:].isdigit():
            num = int(user_cmd)
            print()
            if -total_lines <= num <= -1:
                for line in output_lines[num:]:
                    print(line)
            print()
        elif '--' in user_cmd:
            print()
            try:
                m_str, n_str = user_cmd.split('--')
                m, n = int(m_str.strip()), int(n_str.strip())
                if 1 <= m <= n <= total_lines:
                    for line in output_lines[m - 1:n]:
                        print(line)
                    print()
            except ValueError:
                print()
                continue
        else:
            print()
            continue
