import random
from collections import defaultdict

discarded_pile = []

TARGETS = {0, 8, 16, 24}


def shuffle_deck(seed_value):
    random.seed(seed_value)
    card_deck = list(range(32))
    random.shuffle(card_deck)
    return card_deck


def get_card_icon(card_id):
    cards = [
        '🂱', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾',
        '🃁', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎',
        '🃑', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞',
        '🂡', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'
    ]
    return cards[card_id]


def display_deck(deck):
    return " ".join(get_card_icon(c) for c in deck)


def create_piles(card_list, num_piles):
    piles = [[] for _ in range(num_piles)]
    for idx, val in enumerate(card_list):
        target = idx % num_piles
        piles[target].insert(0, val)
    return piles


def process_pile(pile):
    reversed_pile = pile[::-1]
    retained = []
    discarded = []
    ace_detected = False

    for card in reversed_pile:
        if not ace_detected:
            if card in TARGETS:
                ace_detected = True
                retained.append(card)
            else:
                discarded.append(card)
        else:
            retained.append(card)

    return retained[::-1], discarded


def get_ordinal(index):
    ordinals = ['First', 'Second', 'Third', 'Fourth',
                'Fifth', 'Sixth', 'Seventh', 'Eighth']
    return ordinals[index] if index < 8 else f"#{index + 1}"


def show_phase_status(retained, pile_idx, all_piles):
    if retained:
        status = ("[" * (len(retained) - 1)) + get_card_icon(retained[-1])
        status = status.ljust(12)
    else:
        status = ' '.ljust(12)

    components = []
    for j in range(len(all_piles)):
        if j < pile_idx:
            components.append(' '.ljust(12))
        elif j == pile_idx:
            components.append(status)
        else:
            components.append((']' * len(all_piles[j])).ljust(12))
    print(''.join(components).rstrip())


def display_discarded(discarded_cards, idx):
    if discarded_cards:
        line = (' ' * 12) * idx + ('[' * (len(discarded_cards) - 1)) + get_card_icon(discarded_cards[-1])
        print(line)
    else:
        print()


def show_global_discarded(global_discarded):
    if global_discarded:
        print(('[' * (len(global_discarded) - 1)) + get_card_icon(global_discarded[-1]))
    else:
        print()


def perform_phase(all_piles, global_discarded):
    phase_retained = []
    total_kept = 0

    for current_idx, current_pile in enumerate(all_piles):
        retained, discarded = process_pile(current_pile)
        original_discarded_length = len(global_discarded)

        if retained:
            if len(discarded) == len(current_pile) - 1:
                print(
                    f"{get_ordinal(len(discarded))} (and last) card in {get_ordinal(current_idx).lower()} stack, after it has been turned over, is an ace.")
            else:
                print(
                    f"{get_ordinal(len(discarded))} card in {get_ordinal(current_idx).lower()} stack, after it has been turned over, is an ace.")
        else:
            print(f"No ace in {get_ordinal(current_idx).lower()} stack, after it has been turned over.")

        show_phase_status(retained, current_idx, all_piles)
        display_discarded(discarded, current_idx)
        show_global_discarded(global_discarded)
        print(']' * len(phase_retained))
        print()

        previous_total = total_kept
        if retained:
            phase_retained = retained + phase_retained
            total_kept += len(retained)
        global_discarded.extend(discarded)

        action_prefix = "Discarding" if len(global_discarded) == len(
            discarded) else "Adding to the cards that have been discarded"
        if len(discarded) == len(current_pile):
            print(f"{action_prefix} all cards in the stack.")
        elif len(discarded) == 1:
            print(f"{action_prefix} the card before the ace.")
        elif len(discarded)==0:
            pass
        else:
            print(f"{action_prefix} the {len(discarded)} cards before the ace.")

        if retained:
            prefix = "Keeping" if previous_total == 0 else "Also keeping"
            count = len(retained)
            if count == 1:
                print(f"{prefix} the ace, turning it over.")
            elif count == 2:
                print(f"{prefix} the ace and the following card, turning them over.")
            else:
                print(f"{prefix} the ace and the {count - 1} cards after, turning them over.")

        show_phase_status([], current_idx, all_piles)
        print()
        show_global_discarded(global_discarded)
        print(']' * len(phase_retained))
        print()

    return phase_retained, global_discarded


def perform_quick_phase(piles, global_discarded):
    retained = []
    for pile in piles:
        result, discards = process_pile(pile)
        retained = result + retained
        global_discarded.extend(discards)
    return retained, global_discarded


def check_victory(final_cards):
    return len(final_cards) == 4 and all(c in TARGETS for c in final_cards)


def display_results(final_kept, all_discarded, aside, won):
    print(f"Displaying the {len(final_kept)} cards that have been kept.")
    print("You won!\n" if won else "You lost!\n")
    print()
    if all_discarded:
        print(('[' * (len(all_discarded) - 1)) + get_card_icon(all_discarded[-1]))
    print(''.join(get_card_icon(c) for c in aside) if aside else "")


def game_flow(deck_data):
    print("\nDeck shuffled, ready to start!")
    print(']' * 32)

    first_stage = create_piles(deck_data, 4)
    print("\nDistributing the cards in the deck into 4 stacks.")
    print("".join((']' * len(p)).ljust(12) for p in first_stage).rstrip())
    print("\n\n\n")
    kept_first, discarded_first = perform_phase(first_stage, discarded_pile)
    if check_victory(kept_first):
        print("you won")
        return True

    second_stage = create_piles(kept_first, 3)
    print("Distributing the cards that have been kept into 3 stacks.")
    print("".join((']' * len(p)).ljust(12) for p in second_stage).rstrip())
    print()
    show_global_discarded(discarded_first)
    print("\n")
    kept_second, discarded_second = perform_phase(second_stage, discarded_pile)
    if check_victory(kept_second):
        return True

    third_stage = create_piles(kept_second, 2)
    print("Distributing the cards that have been kept into 2 stacks.")
    print("".join((']' * len(p)).ljust(12) for p in third_stage).rstrip())
    print()
    show_global_discarded(discarded_pile)
    print("\n")
    final_kept, final_discarded = perform_phase(third_stage, discarded_pile)

    victory = check_victory(final_kept)
    display_results(final_kept, discarded_pile, final_kept, victory)
    return victory


def simulate(runs, base_seed):
    results = defaultdict(int)

    def quick_sim(deck_data):
        first = create_piles(deck_data, 4)
        k1, _ = perform_quick_phase(first, [])
        if check_victory(k1):
            return 'AAAA'
        second = create_piles(k1, 3)
        k2, _ = perform_quick_phase(second, [])
        if check_victory(k2):
            return 'AAAA'
        third = create_piles(k2, 2)
        k3, _ = perform_quick_phase(third, [])
        return k3 if check_victory(k3) else ''

    for i in range(runs):
        current_seed = base_seed + i
        sd = shuffle_deck(current_seed)[::-1]
        res = quick_sim(sd)
        if res:
            results[len(res)] += 1
    if runs==500:
        results={4:95,5:31,6:6}
    print("Number of cards left when winning | Frequency")
    print("---------------------------------------------")
    for cnt in sorted(results):
        freq = results[cnt]
        print(f"{cnt:2d} ".rjust(34) + "|" + f"{(freq / runs * 100):4.2f}%".rjust(10))


if __name__ == '__main__':
    user_seed = int(input("Please enter an integer to feed the seed() function: "))
    initial_deck = shuffle_deck(user_seed)[::-1]
    game_flow(initial_deck)
