import random
from collections import defaultdict
phase_removed = []
def shuffle_deck(seed_value):
    random.seed(seed_value)
    deck = [i for i in range(32)]
    random.shuffle(deck)
    return deck


target = [0, 8, 16, 24]

def card_to_unicode(card):
    cards = [
        '🂱', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾',  # Hearts
        '🃁', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎',  # Diamonds
        '🃑', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞',  # Clubs
        '🂡', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'  # Spades
    ]
    return cards[card]


def display(deck):
    return " ".join(card_to_unicode(card) for card in deck)


def simulate_game(deck_values):
    print("\nDeck shuffled, ready to start!")
    print()
    print(']'*32)

    phase1_piles = split_phase(deck_values, 4)
    print("\nDistributing the cards in the desk into 4 stacks.")
    str_1=[]
    for i, pile in enumerate(phase1_piles, 1):
        str_1.append(("]"*len(pile)).ljust(12))
    print(("".join(str_1)).rstrip())
    print()
    print()
    print()
    print()
    phase1_remaining, phase1_removed = process_phase(phase1_piles,phase_removed)
    victory = check_victory(phase1_removed)
    if victory:
        print("you won")
        return True


    phase2_piles = split_phase(phase1_remaining, 3)
    print("Distributing the cards that have been kept into 3 stacks.")
    str_1=[]
    for i, pile in enumerate(phase2_piles, 1):
        str_1.append(("]"*len(pile)).ljust(12))
    print(("".join(str_1)).rstrip())
    print()

    print('['*(len(phase1_removed)-1)+card_to_unicode(phase1_removed[-1]))
    print()
    print()
    phase2_remaining, phase2_removed = process_phase(phase2_piles,phase_removed)
    victory = check_victory(phase2_remaining)
    if victory:
        return True


    phase3_piles = split_phase(phase2_remaining, 2)
    print("Distributing the cards that have been kept into 2 stacks.")
    str_1=[]
    for i, pile in enumerate(phase3_piles, 1):
        str_1.append(("]"*len(pile)).ljust(12))
    print(("".join(str_1)).rstrip())
    print()
    print('['*(len(phase_removed)-1)+card_to_unicode(phase_removed[-1]))
    print()
    print()
    phase3_remaining, phase3_removed = process_phase(phase3_piles,phase_removed)

    victory = check_victory(phase3_remaining)
    all_discarded = phase3_removed
    all_put_aside = phase3_remaining

    final_output(phase3_remaining, all_discarded, all_put_aside, victory)

    return victory

def final_output(final_kept, final_discarded, final_put_aside, victory):

    print(f"Displaying the {len(final_kept)} cards that have been kept.")

    if victory:
        print("You won!")
    else:
        print("You lost!")

    print()
    print()

    if final_discarded:

        discarded_str = '[' * (len(final_discarded)-1) + card_to_unicode(final_discarded[-1])
        print(discarded_str)
    else:
        print()

    if final_put_aside:
        put_aside_str = ''.join(card_to_unicode(card) for card in final_put_aside)
        print(put_aside_str)
    else:
        print()
def split_phase(deck, num_piles):
    if num_piles == 4:
        piles = [[] for _ in range(num_piles)]
        for i, card in enumerate(deck):
            piles[i % 4].append(card)
        for pile in piles:
            pile.reverse()
        return piles
    elif num_piles == 3:
        piles = [[] for _ in range(num_piles)]
        for i, card in enumerate(deck):
            piles[i % 3].append(card)
        for pile in piles:
            pile.reverse()
        return piles
    elif num_piles == 2:
        piles = [[] for _ in range(num_piles)]
        for i, card in enumerate(deck):
            piles[i % 2].append(card)
        for pile in piles:
            pile.reverse()
        return piles


def process_pile(pile):
    flipped = pile[::-1]
    remaining = []
    removed = []
    found = False
    for card in flipped:
        if not found:
            if card in target:
                found = True
                remaining.append(card)
            else:
                removed.append(card)
        else:
            remaining.append(card)
    return remaining[::-1], removed
def get_order(n):
    order=['First', 'Second', 'Third','Fourth','Fifth', 'Sixth','Seventh', 'Eighth']
    return order[n]
def func(processed,i,pile):
    if processed==[]:
        str_1=f' '.ljust(12)
    else:
        str_1=("["*(len(processed)-1)+card_to_unicode(processed[-1])).ljust(12)
    if len(pile)==4:
        if i==0:
            print((str_1+(']'*len(pile[1])).ljust(12)+(']'*len(pile[2])).ljust(12)+(']'*len(pile[3])).ljust(12)).rstrip())
        elif i==1:
            print((f''.ljust(12)*i+str_1+(']'*len(pile[2])).ljust(12)+(']'*len(pile[3])).ljust(12)).rstrip())
        elif i==2:
            print((f''.ljust(12)*i+str_1+((']'*len(pile[3])).ljust(12))).rstrip())
        elif i==3:
            print((f''.ljust(12)*i+str_1).rstrip())
    if len(pile)==3:
        if i==0:
            print((f''.ljust(12)*0+str_1+(']'*len(pile[1])).ljust(12)+(']'*len(pile[2])).ljust(12)).rstrip())
        elif i==1:
            print((f''.ljust(12)*i+str_1+(']'*len(pile[2])).ljust(12).rstrip()))
        elif i==2:
            print((f''.ljust(12)*i+str_1).rstrip())
    if len(pile)==2:
        if i==0:
            print((f''.ljust(12)*0+str_1+(']'*len(pile[1])).ljust(12)).rstrip())
        elif i==1:
            print((f''.ljust(12)*i+str_1).rstrip())
def func_1(removed,i):
    if removed:
        print(f''.ljust(12)*i+'['*(len(removed)-1)+card_to_unicode(removed[-1]))
    else:
        print()
def func_2(removed):
    if removed:
        print('['*(len(removed)-1)+card_to_unicode(removed[-1]))
    else:
        print()

def simulate(n, i):
    def check_victory(final_pile):
        if len(final_pile) == 4:
            return True
        list_copy = final_pile.copy()
        for i, card in enumerate(list_copy):
            if card in target:
                list_copy[i] = 'A'
            else:
                list_copy[i] = 'X'
        return "AAAA" in ''.join(list_copy)
    def shuffle_deck(seed_value):
        random.seed(seed_value)
        deck = [i for i in range(32)]
        random.shuffle(deck)
        return deck
    def simulate_game(deck_values):

        phase1_piles = split_phase(deck_values, 4)

        phase1_remaining, phase1_removed = process_phase(phase1_piles)

        if check_victory(phase1_remaining):
            return 'AAAA'
        phase2_piles = split_phase(phase1_remaining, 3)

        phase2_remaining, phase2_removed = process_phase(phase2_piles)

        if check_victory(phase2_remaining):
            return 'AAAA'
        phase3_piles = split_phase(phase2_remaining, 2)

        phase3_remaining, phase3_removed = process_phase(phase3_piles)
        if check_victory(phase3_remaining):
            return phase3_remaining
        else:
            return ''

    def split_phase(deck, num_piles):
        if num_piles == 4:
            piles = [[] for _ in range(num_piles)]
            for i, card in enumerate(deck):
                piles[i % 4].append(card)
            for pile in piles:
                pile.reverse()
            return piles
        elif num_piles == 3:
            piles = [[] for _ in range(num_piles)]
            for i, card in enumerate(deck):
                piles[i % 3].append(card)
            for pile in piles:
                pile.reverse()
            return piles
        elif num_piles == 2:
            piles = [[] for _ in range(num_piles)]
            for i, card in enumerate(deck):
                piles[i % 2].append(card)
            for pile in piles:
                pile.reverse()
            return piles

    def process_phase(piles):
        phase_remaining = []
        phase_removed = []
        for i, pile in enumerate(piles, 1):
            processed, removed = process_pile(pile)

            if processed:
                phase_remaining = processed + phase_remaining
            phase_removed.extend(removed)
        return phase_remaining, phase_removed
    def process_pile(pile):
        flipped = pile[::-1]
        remaining = []
        removed = []
        found = False
        for card in flipped:
            if not found:
                if card in target:
                    found = True
                    remaining.append(card)
                else:
                    removed.append(card)
            else:
                remaining.append(card)
        return remaining[::-1], removed
    results = defaultdict(int)

    for game_num in range(n):
        seed_value = i + game_num
        deck = shuffle_deck(seed_value)
        deck_values = [card for card in deck[::-1]]
        remaining_cards = simulate_game(deck[::-1])

        if remaining_cards is not None:
            results[len(remaining_cards)] += 1

    print("Number of cards left when winning | Frequency")
    print("---------------------------------------------")
    sorted_results = sorted(results.items())
    for remaining, count in sorted_results:
        if remaining == 0:
            continue
        probability = (count / n) * 100
        if probability < 0.005:
            prob_str = "0.00"
        else:
            prob_str = f"{probability:4.2f}"
        print(f"{remaining:2d} ".rjust(34)+"|"+f"{prob_str}%".rjust(10))
def process_phase(piles,phase_removed):
    phase_remaining = []

    global_kept = 0
    for i, pile in enumerate(piles):
        processed, removed = process_pile(pile)
        if processed:
            if len(removed)==len(pile)-1:
                print(f'{get_order(len(removed))} (and last) card in {get_order(i).lower()} stack, after it has been turned over, is an ace.')
            else:
                print(f'{get_order(len(removed))} card in {get_order(i).lower()} stack, after it has been turned over, is an ace.')

        else:
            print(f"No ace in {get_order(i).lower()} stack, after it has been turned over.")

        func(processed, i, piles)
        func_1(removed, i)
        func_2(phase_removed)
        print(']' * len(phase_remaining))
        print()

        prev_kept = global_kept
        if processed:
            phase_remaining = processed + phase_remaining
            global_kept += len(processed)
        phase_removed.extend(removed)
        if len(phase_removed) - len(removed) == 0:
            prefix = "Discarding"
        else:
            prefix = "Adding to the cards that have been discarded"
        if len(removed) == len(pile):
            print(f"{prefix} all cards in the stack.")
        elif len(removed) == 1:
            print(f"{prefix} the card before the ace.")
        elif len(removed) >= 2:
            print(f"{prefix} the {len(removed)} cards before the ace.")
        else:
            pass

        if processed:
            if prev_kept == 0:
                prefix2 = "Keeping"
            else:
                prefix2 = "Also keeping"
            if len(processed) == 1:
                print(f"{prefix2} the ace, turning it over.")
            elif len(processed) == 2:
                print(f"{prefix2} the ace and the card after, turning them over.")
            elif len(processed) >= 3:
                print(f"{prefix2} the ace and the {len(processed) - 1} cards after, turning them over.")

        func([], i, piles)
        print()
        func_2(phase_removed)
        print(']' * len(phase_remaining))
        print()
    return phase_remaining, phase_removed

def check_victory(final_pile):
    if len(final_pile)==4:
        return True
    list_copy=final_pile.copy()
    for i, card in enumerate(list_copy):
        if card in target:
            list_copy[i]='A'
        else:
            list_copy[i] = 'X'
    return "AAAA" in ''.join(list_copy)


if __name__ == '__main__':
    seed_value = int(input("Please enter an integer to feed the seed() function: "))
    deck = shuffle_deck(seed_value)

    deck_values = [card for card in deck[::-1]]

    simulate_game(deck_values)

