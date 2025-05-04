import random

base = [[None for _ in range(4)] for _ in range(13)]
suit_map = {0: 3, 1: 0, 2: 1, 3: 2}
reverse_map = {3: 0, 0: 1, 2: 3, 1: 2}
log = []


def card_value(c):
    return (c % 13) + 1


def card_suit(c):
    return c // 13


def make_deck(s):
    random.seed(s)
    d = list(set(range(52)) - {6, 19, 32, 45})
    random.shuffle(d)
    return d


def record(msg=""):
    log.append(msg.rstrip() if msg else "")


def card_pic(c):
    icons = [
        '🂱', '🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾',
        '🃁', '🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎',
        '🃑', '🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞',
        '🂡', '🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'
    ]
    return icons[c]


def init_base():
    for sc in [6, 19, 32, 45]:
        s = card_suit(sc)
        base[6][suit_map[s]] = 7


def show_base():
    for r in base:
        line = []
        for c in range(4):
            if r[c] is None:
                line.append("")
            else:
                suit = reverse_map[c]
                num = r[c] - 1
                line.append(card_pic(num + suit * 13))
        record('\t' + '\t'.join(line))
    record()


def can_put(card):
    v = card_value(card)
    s = card_suit(card)
    col = suit_map[s]

    if v == 7:
        return False, None, None

    if v > 7:
        target_r = 6 - (v - 7)
        if target_r < 0 or target_r > 5:
            return False, None, None
        if base[target_r][col] is not None:
            return False, None, None
        if v == 8:
            return (base[6][col] == 7), target_r, col
        else:
            return (base[target_r + 1][col] == v - 1), target_r, col
    else:
        target_r = 6 + (7 - v)
        if target_r < 7 or target_r > 12:
            return False, None, None
        if base[target_r][col] is not None:
            return False, None, None
        if v == 6:
            return (base[6][col] == 7), target_r, col
        else:
            return (base[target_r - 1][col] == v + 1), target_r, col


def attempt_place(card, src):
    ok, r, c = can_put(card)
    if ok:
        base[r][c] = card_value(card)
        msg = "left" if src == 1 else "put aside"
        record(f"Placing card from top of stack of cards {msg} 😊")
        return True
    else:
        msgs = {
            1: "Cannot place card from top of stack of cards left ☹️",
            2: "Cannot place card from top of stack of cards put aside ☹️"
        }
        record(msgs[src])
        if src == 2:
            record('')
    return False


def process_discards(main, discard):
    changed = True
    while changed and discard:
        changed = False
        top = discard[-1]
        if attempt_place(top, 2):
            discard.pop()
            record("]" * len(main))
            record(("[" * (len(discard) - 1) + card_pic(discard[-1])) if discard else "")
            show_base()
            changed = True


def phase_num(n):
    return ['first', 'second', 'third', 'fourth'][n]


def play_phase(main, discard):
    while main:
        current = main.pop(0)
        if attempt_place(current, 1):
            record("]" * len(main))
            record(("[" * (len(discard) - 1) + card_pic(discard[-1])) if discard else "")
            show_base()
            process_discards(main, discard)
        else:
            discard.append(current)
            record("]" * len(main))
            record("[" * (len(discard) - 1) + card_pic(discard[-1]))
            record()
    return main, discard


def run_game(seed):
    global base
    base = [[None] * 4 for _ in range(13)]
    init_base()
    record("All 7s removed and placed, rest of deck shuffled, ready to start!")

    main = make_deck(seed)[::-1]
    record(']' * len(main))
    record()
    show_base()
    discard = []

    for phase in range(3):
        if phase == 0:
            record(f"Starting {phase_num(phase)} round...")
        else:
            record()
            record(f"Starting {phase_num(phase)} round...")
        record()
        main, discard = play_phase(main, discard)

        complete = True
        for c in range(4):
            cnt = sum(1 for r in base if r[c] is not None)
            if cnt != 13:
                complete = False
                break
        if complete:
            record("You placed all cards, you won 👍")
            return 0
        if phase < 2:
            main = discard
            discard = []

    remain = len(main) + len(discard)
    record(f"You could not place {remain} cards, you lost 👎")
    return remain


def simulate(n, s):
    stats = {}
    for i in range(n):
        res = run_game(s + i)
        stats[res] = stats.get(res, 0) + 1

    print('Number of cards left | Frequency')
    print('--------------------------------')
    for k in sorted(stats, reverse=True):
        pct = stats[k] / n * 100
        print(f"{k} |   {pct:6.2f}%".rjust(32))


if __name__ == '__main__':
    s = int(input("Please enter an integer to feed the seed() function: "))
    run_game(s)
    print(f'\nThere are {len(log)} lines of output; what do you want me to do?\n')

    while True:
        print('Enter: q to quit')
        print(f'       a last line number (between 1 and {len(log)})')
        print(f'       a first line number (between -1 and -{len(log)})')
        print(f'       a range of line numbers (of the form m--n with 1 <= m <= n <= {len(log)})')

        cmd = input('       ').strip()
        if cmd == 'q':
            break
        elif cmd.isdigit():
            n = int(cmd)
            if 1 <= n <= len(log):
                print('\n' + '\n'.join(log[:n]))
        elif cmd.startswith('-') and cmd[1:].isdigit():
            n = int(cmd)
            if -len(log) <= n < 0:
                print('\n' + '\n'.join(log[n:]))
        elif '--' in cmd:
            try:
                m, n = map(int, cmd.split('--'))
                if 1 <= m <= n <= len(log):
                    print('\n' + '\n'.join(log[m - 1:n]))
            except:
                pass
        print()
