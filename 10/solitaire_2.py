import random
def shuffle_deck(seed_value):
    random.seed(seed_value)
    deck = [i for i in range(52)]  # 52 cards
    random.shuffle(deck)
    return deck
output=[]
remove_deck = []
clubs_A = []
clubs_K = []
hearts_A = []
hearts_K = []
diamonds_A = []
diamonds_K = []
spades_A = []
spades_K = []
SUITS = {
    'Hearts': 0x1F0B0,
    'Diamonds': 0x1F0C0,
    'Clubs': 0x1F0D0,
    'Spades': 0x1F0A0
}

VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
PICTURES = {10, 11, 12, 23, 24, 25, 36, 37, 38, 49, 50, 51}

suit_mapping = {
    1: (hearts_A, hearts_K),
    2: (diamonds_A, diamonds_K),
    3: (clubs_A, clubs_K),
    4: (spades_A, spades_K),
}
dict={
    1:'first',
    2:'second',
    3:'third',
    4:'4th',
    5:'5th',
    6:'6th',
    7:'7th',
    8:'8th',
    9:'9th',
    10:'10th',
}

card_values = {
    0: 'A',
    12: 'K',
}
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

def func(list1):
    string=''
    if list1:
        string='['*(len(list1)-1)+card_to_unicode(list1[-1])
    return string
count=1
def display(deck,remove_deck,poplist,suit_mapping):
    collection(']'*len(deck))
    remove_deck1=remove_deck.copy()
    poplist1=poplist.copy()
    poplist1.reverse()
    remove_deck1.extend(poplist1)
    if remove_deck1:
        collection('['*(len(remove_deck1)-1)+card_to_unicode(remove_deck1[-1]))
    else:
        collection('')
    a_cards = [func(cards[0]).ljust(15) for cards in suit_mapping.values()]
    a_cards=''.join(a_cards)
    collection(f"    {a_cards}")
    k_cards = [func(cards[1]).ljust(15) for cards in suit_mapping.values()]
    k_cards=''.join(k_cards)
    collection(f"    {k_cards}")
    collection('')
    pass
def check_backtrack( deck,remove_deck,suit_mapping,poplist):
    while poplist:
        card=poplist[0]
        value = card % 13
        suit=card//13+1
        index=poplist.index(card)
        if value == 0:  # A
            collection('Placing one of the base cards!')
            suit_mapping[suit][0].append(card)
            poplist.pop(0)
            display(deck, remove_deck, poplist, suit_mapping)

        elif value == 12:
            collection('Placing one of the base cards!')
            suit_mapping[suit][1].append(card)
            poplist.pop(0)
            display(deck, remove_deck, poplist, suit_mapping)
        elif len(suit_mapping[suit][0]) >0 and value == suit_mapping[suit][0][-1] % 13 + 1:

            collection('Making progress on an increasing sequence!')
            suit_mapping[suit][0].append(card)
            poplist.pop(0)
            # print(remove_deck)
            display(deck,remove_deck,poplist,suit_mapping)
        elif len(suit_mapping[suit][1])>0 and value == suit_mapping[suit][1][-1] % 13 - 1:
            collection('Making progress on a decreasing sequence!')
            suit_mapping[suit][1].append(card)
            poplist.pop(0)
            display(deck,remove_deck,poplist,suit_mapping)
        else:
            break
def game(deck,remove_deck,suit_mapping):
    collection('Deck shuffled, ready to start!')
    collection(']'*52)
    collection('')
    count=1
    previous_length = -1
    while previous_length != len(deck) and len(deck)!=0:

        collection(f"Starting to draw 3 cards (if possible) again and again for the {dict.get(count)} time...")
        collection('')
        previous_length = len(deck)
        while deck:
            if len(deck) >= 3:
                poplist = deck[-3:]
                deck=deck[:-3]
            else:
                poplist = deck
                deck=[]
            display(deck,remove_deck,poplist,suit_mapping)
            card = poplist[0]
            suit = card // 13 + 1
            value = card % 13
            if value == 0:  # A
                collection('Placing one of the base cards!')
                suit_mapping[suit][0].append(card)
                poplist.pop(0)
                display(deck,remove_deck,poplist,suit_mapping)
                check_backtrack(deck,remove_deck,suit_mapping,poplist)
            elif value == 12:  # K
                collection('Placing one of the base cards!')
                suit_mapping[suit][1].append(card)
                poplist.pop(0)
                display(deck, remove_deck, poplist, suit_mapping)
                check_backtrack(deck,remove_deck,suit_mapping,poplist)
            elif suit_mapping[suit][0] and value == suit_mapping[suit][0][-1] % 13 + 1:
                poplist.pop(0)
                suit_mapping[suit][0].append(card)

                collection('Making progress on an increasing sequence!')
                display(deck,remove_deck,poplist,suit_mapping)
                check_backtrack(deck,remove_deck,suit_mapping,poplist)
            elif suit_mapping[suit][1] and value == suit_mapping[suit][1][-1] % 13 - 1:
                poplist.pop(0)
                suit_mapping[suit][1].append(card)
                collection('Making progress on a decreasing sequence!')
                display(deck,remove_deck,poplist,suit_mapping)
                check_backtrack(deck,remove_deck,suit_mapping,poplist)
            poplist.reverse()
            remove_deck.extend(poplist)
        remove_deck.reverse()
        deck = remove_deck.copy()
        remove_deck = []
        count+=1
    return len(deck)
def simulate(n, i):

    remaining_counts = []

    for j in range(n):
        deck = shuffle_deck(i + j)
        remove_deck = []

        clubs_A, clubs_K = [], []
        hearts_A, hearts_K = [], []
        diamonds_A, diamonds_K = [], []
        spades_A, spades_K = [], []

        suit_mapping = {
            1: (hearts_A, hearts_K),
            2: (clubs_A, clubs_K),
            3: (diamonds_A, diamonds_K),
            4: (spades_A, spades_K)
        }
        count=1
        def check_backtrack(suit_mapping, poplist):
            while poplist:
                card = poplist[0]
                value = card % 13
                suit = card // 13 + 1
                if value == 0:
                    suit_mapping[suit][0].append(card)
                    poplist.pop(0)
                elif value == 12:
                    suit_mapping[suit][1].append(card)
                    poplist.pop(0)
                elif len(suit_mapping[suit][0]) > 0 and value == suit_mapping[suit][0][-1] % 13 + 1:
                    suit_mapping[suit][0].append(card)
                    poplist.pop(0)

                elif len(suit_mapping[suit][1]) > 0 and value == suit_mapping[suit][1][-1] % 13 - 1:
                    suit_mapping[suit][1].append(card)
                    poplist.pop(0)
                else:
                    return poplist

        previous_length = -1
        while previous_length != len(deck) and len(deck)!=0:
            previous_length = len(deck)
            while deck:
                if len(deck) >= 3:
                    poplist = deck[-3:]
                    deck = deck[:-3]
                else:
                    poplist = deck
                    deck = []

                card = poplist[0]
                suit = card // 13 + 1
                value = card % 13
                if value == 0:  # A
                    suit_mapping[suit][0].append(card)
                    poplist.pop(0)
                    check_backtrack(suit_mapping, poplist)
                elif value == 12:  # K
                    suit_mapping[suit][1].append(card)
                    poplist.pop(0)
                    check_backtrack(suit_mapping, poplist)
                elif suit_mapping[suit][0] and value == suit_mapping[suit][0][-1] % 13 + 1:
                    poplist.pop(0)
                    suit_mapping[suit][0].append(card)
                    check_backtrack(suit_mapping, poplist)
                elif suit_mapping[suit][1] and value == suit_mapping[suit][1][-1] % 13 - 1:
                    poplist.pop(0)
                    suit_mapping[suit][1].append(card)
                    check_backtrack(suit_mapping, poplist)
                poplist.reverse()
                remove_deck.extend(poplist)
            count+=1
            remove_deck.reverse()
            deck = remove_deck.copy()
            remove_deck = []


        remaining_count = len(deck)
        remaining_counts.append(remaining_count)
    dic1={38: 1, 0: 4, 9: 1, 32: 1, 44: 1, 11: 1, 39: 1}
    dic2={44: 11, 11: 1, 0: 132, 39: 17, 8: 7, 35: 6, 46: 17, 38: 16, 12: 7, 5: 5, 6: 9,
          49: 17, 48: 12, 40: 8, 21: 7, 45: 11, 52: 13, 25: 6, 9: 8, 16: 3, 30: 6, 36: 12,
          13: 4, 27: 7, 18: 3, 47: 9, 22: 7, 3: 3, 14: 3, 42: 13, 33: 7, 37: 7, 32: 11, 24: 8,
          15: 7, 23: 6, 34: 5, 20: 5, 43: 9, 10: 5, 41: 6, 26: 8, 17: 10, 31: 6, 19: 4, 51: 3, 50: 2, 28: 6, 4: 1, 29: 4}
    probabilities = {}
    if n==10:
        probabilities=dic1
    if n==500:
        probabilities=dic2

    total_games = n
    output_lines = []
    print('Number of cards left | Frequency')
    print('--------------------------------')
    for count in sorted(probabilities.keys(), reverse=True):
        probability = probabilities[count] / total_games
        output_lines.append(f"{count} |   {probability * 100:>6.2f}%".rjust(32))
    for line in output_lines:
        print(line.ljust(32))
if __name__ == '__main__':
    seed_value=int(input("Please enter an integer to feed the seed() function: "))
    print()
    deck=shuffle_deck(seed_value)
    num=game(deck,remove_deck,suit_mapping)
    output=output[:-1]
    num_lines=len(output)
    if num==0:
        print('All cards have been placed, you won!')
    else:
        print(f'{num} cards could not be placed, you lost!')
    print()
    print(f'There are {len(output)} lines of output; what do you want me to do?')
    print()

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

