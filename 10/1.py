import random
from collections import defaultdict
discarded_cards = []

TARGET_CARDS = [0, 8, 16, 24]


def randomize_deck(seed_val):

    random.seed(seed_val)
    deck = [i for i in range(32)]
    random.shuffle(deck)
    return deck


def card_unicode(card):


    icons = [
        '🂱', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾',  # Hearts
        '🃁', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎',  # Diamonds
        '🃑', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞',  # Clubs
        '🂡', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'  # Spades
    ]
    return icons[card]


def show_deck(deck):

    return " ".join(card_unicode(card) for card in deck)


def distribute_cards(deck, num):

    stacks = [[] for _ in range(num)]
    for idx, card in enumerate(deck):
        stacks[idx % num].append(card)
    for stack in stacks:
        stack.reverse()
    return stacks



def evaluate_stack(stack):
    rev_stack = stack[::-1]
    kept = []
    removed = []
    found_target = False
    i = 0
    while i < len(rev_stack):
        card = rev_stack[i]
        if not found_target:
            if card in TARGET_CARDS:
                found_target = True
                kept.append(card)
            else:
                removed.append(card)
        else:
            kept.append(card)
        i += 1

    return kept[::-1], removed


def order_label(n):
    orders = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth']
    return orders[n] if n < len(orders) else f"#{n + 1}"


def print_phase_info(kept, idx, stacks):
    if kept:
        info = ("[" * (len(kept) - 1)) + card_unicode(kept[-1])
        info = info.ljust(12)
    else:
        info = ' '.ljust(12)

    segments = []
    for j in range(len(stacks)):
        if j < idx:
            segments.append(' '.ljust(12))
        elif j == idx:
            segments.append(info)
        else:
            segments.append((']' * len(stacks[j])).ljust(12))
    line = "".join(segments)
    print(line.rstrip())


def print_removed_info(removed, idx):
    if removed:
        line = (' '.ljust(12)) * idx + ('[' * (len(removed) - 1)) + card_unicode(removed[-1])
        print(line)
    else:
        print()


def print_global_removed(global_removed):
    if global_removed:
        print(('[' * (len(global_removed) - 1)) + card_unicode(global_removed[-1]))
    else:
        print()

def execute_phase_1(stacks, global_removed):
    phase_kept = []
    global_kept = 0

    for idx, stack in enumerate(stacks):
        kept, removed = evaluate_stack(stack)

        prev_kept = global_kept
        if kept:
            phase_kept = kept + phase_kept
            global_kept += len(kept)
        global_removed.extend(removed)

    return phase_kept, global_removed

def execute_phase(stacks, global_removed):
    phase_kept = []
    global_kept = 0
    for idx, stack in enumerate(stacks):
        kept, removed = evaluate_stack(stack)

        if kept:
            if len(removed) == len(stack) - 1:
                print(
                    f'{order_label(len(removed))} (and last) card in {order_label(idx).lower()} stack, after it has been turned over, is an ace.')
            else:
                print(
                    f'{order_label(len(removed))} card in {order_label(idx).lower()} stack, after it has been turned over, is an ace.')
        else:
            print(f"No ace in {order_label(idx).lower()} stack, after it has been turned over.")

        print_phase_info(kept, idx, stacks)
        print_removed_info(removed, idx)
        print_global_removed(global_removed)
        print(']' * len(phase_kept))
        print()

        prev_kept = global_kept
        if kept:
            phase_kept = kept + phase_kept
            global_kept += len(kept)
        global_removed.extend(removed)
        str_pre = "Discarding" if (len(global_removed) - len(
            removed)) == 0 else "Adding to the cards that have been discarded"
        if len(removed) == len(stack):
            print(f"{str_pre} all cards in the stack.")
        elif len(removed) == 1:
            print(f"{str_pre} the card before the ace.")
        elif len(removed) >= 2:
            print(f"{str_pre} the {len(removed)} cards before the ace.")
        if kept:
            str_pre2 = "Keeping" if prev_kept == 0 else "Also keeping"
            if len(kept) == 1:
                print(f"{str_pre2} the ace, turning it over.")
            elif len(kept) == 2:
                print(f"{str_pre2} the ace and the following card, turning them over.")
            elif len(kept) >= 3:
                print(f"{str_pre2} the ace and the {len(kept) - 1} cards after, turning them over.")

        print_phase_info([], idx, stacks)
        print()
        print_global_removed(global_removed)
        print(']' * len(phase_kept))
        print()
    return phase_kept, global_removed


def show_final_results(kept_final, discarded_final, aside_final, victory):
    print(f"Displaying the {len(kept_final)} cards that have been kept.")

    print("You won!\n" if victory else "You lost!\n")
    print()

    print('[' * (len(discarded_final) - 1) + card_unicode(discarded_final[-1]) if discarded_final else "")

    print(''.join(card_unicode(card) for card in aside_final) if aside_final else "")



def check_win(final_pile):
    if len(final_pile) == 4:
        return True
    temp = final_pile.copy()
    for idx, card in enumerate(temp):
        temp[idx] = 'A' if card in TARGET_CARDS else 'X'
    return "AAAA" in ''.join(temp)


def play_simulation(deck_values):
    print("\nDeck shuffled, ready to start!")
    print(']' * 32)

    phase1 = distribute_cards(deck_values, 4)
    print("\nDistributing the cards in the deck into 4 stacks.")
    line_parts = []
    for pile in phase1:
        line_parts.append((']' * len(pile)).ljust(12))
    print("".join(line_parts).rstrip())
    print("\n\n\n")
    phase1_remaining, phase1_removed = execute_phase(phase1, discarded_cards)
    if check_win(phase1_remaining):
        print("you won")
        return True

    phase2 = distribute_cards(phase1_remaining, 3)
    print("Distributing the cards that have been kept into 3 stacks.")
    line_parts = []
    for pile in phase2:
        line_parts.append((']' * len(pile)).ljust(12))
    print("".join(line_parts).rstrip())
    print()
    print('[' * (len(phase1_removed) - 1) + card_unicode(phase1_removed[-1]))
    print("\n")
    phase2_remaining, phase2_removed = execute_phase(phase2, discarded_cards)
    if check_win(phase2_remaining):
        return True

    phase3 = distribute_cards(phase2_remaining, 2)
    print("Distributing the cards that have been kept into 2 stacks.")
    line_parts = []
    for pile in phase3:
        line_parts.append((']' * len(pile)).ljust(12))
    print("".join(line_parts).rstrip())
    print()
    print('[' * (len(discarded_cards) - 1) + card_unicode(discarded_cards[-1]))
    print("\n")
    phase3_remaining, phase3_removed = execute_phase(phase3, discarded_cards)

    win_flag = check_win(phase3_remaining)
    all_discarded = phase3_removed
    all_aside = phase3_remaining
    show_final_results(phase3_remaining, all_discarded, all_aside, win_flag)
    return win_flag


def simulate(n, start_seed):

    outcomes = defaultdict(int)

    
    def sim_game_local(deck_vals):
        stacks1 = distribute_cards(deck_vals, 4)
        rem1, remv1 = execute_phase_1(stacks1, [])
        if check_win(rem1):
            return 'AAAA'
        stacks2 = distribute_cards(rem1, 3)
        rem2, remv2 = execute_phase_1(stacks2, [])
        if check_win(rem2):
            return 'AAAA'
        stacks3 = distribute_cards(rem2, 2)
        rem3, remv3 = execute_phase_1(stacks3, [])
        if check_win(rem3):
            return rem3
        else:
            return ''

    for game_no in range(n):
        seed_val = start_seed + game_no
        deck = randomize_deck(seed_val)
        deck_vals = deck[::-1]
        result = sim_game_local(deck_vals)
        if result is not None:
            outcomes[len(result)] += 1

    print("Number of cards left when winning | Frequency")
    print("---------------------------------------------")
    for rem_count, count in sorted(outcomes.items()):
        if rem_count == 0:
            continue
        prob = (count / n) * 100
        prob_str = "0.00" if prob < 0.005 else f"{prob:4.2f}"
        print(f"{rem_count:2d} ".rjust(34) + "|" + f"{prob_str}%".rjust(10))


if __name__ == '__main__':
    seed_input = int(input("Please enter an integer to feed the seed() function: "))
    deck = randomize_deck(seed_input)
    deck_vals = deck[::-1]
    play_simulation(deck_vals)
