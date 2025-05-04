import random

foundation = [[None for _ in range(4)] for _ in range(13)]

suit_to_col = {0: 3, 1: 0, 2: 1, 3: 2}
return_to_col = {3:0,0:1,2:3,1:2}
output=[]
def get_value(card):

    return (card % 13) + 1

def get_suit(card):

    return card // 13

def shuffle_deck(seed_value):

    random.seed(seed_value)
    deck = list(set(range(52)) - {6, 19, 32, 45})
    random.shuffle(deck)
    return deck
def collection(output_str):
    if not output_str:
        output_str=""
    else:
        output_str = output_str.rstrip()
    output.append(output_str)
def card_to_unicode(card):
    cards = [
    '🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾',  # Hearts
    '🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎',  # Diamonds
    '🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞',  # Clubs
    '🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'   # Spades
    ]

    return cards[card]

def init_foundation():
    foundation[6][suit_to_col[get_suit(6)]] = 7

    foundation[6][suit_to_col[get_suit(32)]] = 7

    foundation[6][suit_to_col[get_suit(45)]] = 7

    foundation[6][suit_to_col[get_suit(19)]] = 7


def display_foundation():

    for row in range(13):
        row_disp = []
        for col in range(4):
            if foundation[row][col] is None:
                row_disp.append("")
            else:
                row_disp.append(f"{card_to_unicode(foundation[row][col]+return_to_col.get(col)*13-1)}")
                # row_disp.append(f"{foundation[row][col]+return_to_col.get(col)*13-1}")
        collection('\t'+"\t".join(row_disp))
    collection('')

def can_place(card):

    value = get_value(card)
    suit = get_suit(card)
    col = suit_to_col[suit]

    if value > 7:
        row_target = 6 - (value - 7)
        if row_target < 0 or row_target > 5:
            return False, None, None
        if foundation[row_target][col] is not None:
            return False, None, None
        if value == 8:
            if foundation[6][col] == 7:
                return True, row_target, col
        else:
            if foundation[row_target + 1][col] == value - 1:
                return True, row_target, col
        return False, None, None
    elif value < 7:
        row_target = 6 + (7 - value)
        if row_target < 7 or row_target > 12:
            return False, None, None
        if foundation[row_target][col] is not None:
            return False, None, None
        if value == 6:
            if foundation[6][col] == 7:
                return True, row_target, col
        else:
            if foundation[row_target - 1][col] == value + 1:
                return True, row_target, col
        return False, None, None
    else:

        return False, None, None

def place_card(card,classify):

    can, row, col = can_place(card)
    if can:
        foundation[row][col] = get_value(card)
        if classify==1:
            collection(f"Placing card from top of stack of cards left 😊")
        elif classify==2:
            collection(f"Placing card from top of stack of cards put aside 😊")
        return True
    else:
        if classify==1:
            collection(f"Cannot place card from top of stack of cards left ☹️")
        elif classify==2:
            # collection('')
            collection(f"Cannot place card from top of stack of cards put aside ☹️")

    return False

def process_waste(stock,waste):

    changed = True
    while changed and waste:
        changed = False
        top_card = waste[-1]
        if place_card(top_card,2):
            waste.pop()
            collection("]" * len(stock))
            if  waste:
                collection("[" * (len(waste) - 1) + card_to_unicode(waste[-1]))
            else:
                collection('')
            display_foundation()
            changed = True
        else:
            collection('')
def get_order(n):
    order=['first', 'second', 'third','fourth']
    return order[n]
def play_phase(stock, waste):

    while stock:
        card = stock.pop(0)
        if place_card(card,1):
            collection("]"*len(stock))
            if  waste:
                collection("["*(len(waste)-1)+card_to_unicode(waste[-1]))
            else:
                collection('')
            display_foundation()
            process_waste(stock,waste)
        else:
            waste.append(card)
            collection("]" * len(stock))
            collection("[" * (len(waste) - 1) + card_to_unicode(waste[-1]))
            collection('')
    return stock, waste

def game(seed_value):

    global foundation
    foundation = [[None for _ in range(4)] for _ in range(13)]
    init_foundation()
    collection("All 7s removed and placed, rest of deck shuffled, ready to start!")

    stock = shuffle_deck(seed_value)[::-1]
    collection(']'*len(stock))
    collection('')
    display_foundation()
    waste = []

    for phase in range(0, 3):
        if phase==0:
            collection(f"\nStarting {get_order(phase)} round...")
        else:
            collection('')
            collection(f"Starting {get_order(phase)} round...")
        collection('')
        stock, waste = play_phase(stock, waste)
        complete = True
        for col in range(4):
            count = sum(1 for row in range(13) if foundation[row][col] is not None)
            if count != 13:
                complete = False
                break
        if complete:
            collection("You placed all cards, you won 👍")
            return 0
        if phase < 3:
            stock = waste
            waste = []
    collection(f"You could not place {len(stock) + len(waste)} cards, you lost 👎")
    return len(stock) + len(waste)
def simulate(n, i):
    outcomes = {}
    for j in range(n):
        leftover = game(i + j)
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
    seed_value = int(input("Please enter an integer to feed the seed() function: "))
    game(seed_value)
    print()
    print(f'There are {len(output)} lines of output; what do you want me to do?')
    print()
    num_lines = len(output)
    while True:
        print('Enter: q to quit')
        print(f'       a last line number (between 1 and {len(output)})')
        print(f'       a first line number (between -1 and -{len(output)})')
        print("       a range of line numbers (of the form m--n with 1 <= m <= n <= {})".format(len(output)))

        user_input = input('       ').strip()
        if user_input == 'q':
            break
        elif user_input.isdigit():
            print()
            n = int(user_input)
            if 1 <= n <= num_lines:
                for line in output[:n]:
                    print(line)
            print()
        elif user_input.startswith('-') and user_input[1:].isdigit():
            n = int(user_input)
            print()
            if -num_lines <= n <= -1:
                for line in output[n:]:
                    print(line)
            print()
        elif '--' in user_input:
            print()
            try:
                m, n = user_input.split('--')
                m, n = int(m.strip()), int(n.strip())
                if 1 <= m <= n <= num_lines:
                    for line in output[m - 1:n]:
                        print(line)
                    print()
            except ValueError:
                print()
                continue
        else:
            print()
            continue
