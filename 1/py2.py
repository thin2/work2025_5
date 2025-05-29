import re

lines = []
current1 = 0
current2 = 0
copy_text = ""
UndoStack = []
last_opt = None
row_enable = False
col_enable = False
opts = ['?', '.', ';', 'h', 'j', 'k', 'l', '^', '$', 'w', 'b', 'i', 'a', 'x', 'dw', 'yy', 'p', 'P', 'dd',
        'o', 'O', 'u', 'r', 's', 'q']

def display_lines():
    # if not lines :
    #     return
    for idx, line in enumerate(lines):
        is_current_row = ((idx+1) == current1)
        is_line_empty = not line.strip()
        if is_line_empty and not is_current_row:
            continue
        prefix = ''
        if row_enable:
            prefix = '*' if is_current_row else ' '
        print(prefix, end='')
        if is_current_row and col_enable and line:
            cursor_index = min(current2, len(line) - 1)
            highlighted_line = (
                    line[:cursor_index]
                    + '\033[42m' + line[cursor_index] + '\033[0m'
                    + line[cursor_index + 1:]
            )
            print(highlighted_line)
        elif not is_line_empty:
            print(line)
        elif is_current_row:
            print()

def save_state():
    UndoStack.append((lines.copy(), current1, current2, row_enable, col_enable,last_opt,copy_text))
def undo():
    global lines, current1, current2, row_enable, col_enable
    if UndoStack:
        lines, current1, current2, row_enable, col_enable, last_opt, copy_text = UndoStack.pop()
def insert_text(text):
    global lines, current2, current1
    if not lines:
        lines.append("")
        current1 = 1
        current2 = 0
    current11=max(0,current1-1)
    line = lines[current11]
    lines[current11] = line[:current2] + text + line[current2:]
def append_text(text):
    global lines, current2, current1
    if not lines:
        lines.append("")
        current1 = 1
        current2 = 0
    current11=max(0,current1-1)
    line = lines[current11]
    lines[current11] = line[:current2+1] + text + line[current2+1:]
    if current2==0:
        current2 += len(text)-1
    else:
        current2 += len(text)



def det_c():
    global lines
    if  not lines:
        return
    current11=max(0,current1-1)
    line = lines[current11]
    if line and current2 < len(line):
        lines[current11] = line[:current2] + line[current2 + 1:]


def det_w():
    global lines, current2
    if  not lines:
        return
    current11=max(0,current1-1)
    line = lines[current11]

    if current2 >= len(line):
        current2 = len(line.strip()) - 1
        return
    match = re.search(r"\s+", line[current2:])
    if match:
        end = current2 + match.end() + 1
        lines[current11] = line[:current2] + line[end:]
    else:
        lines[current11] = line[:current2]


def move_left():
    global current2
    if current2 > 0:
        current2 -= 1


def move_right():
    global current2
    if current2 < len(lines[current1]):
        current2 += 1


def move_to_start():
    global current2
    current2 = 0


def move_to_end():
    global current2
    current2 = len(lines[current1])


def move_word_left():
    global current2
    line = lines[current1]
    if current2 == 0:
        return
    i = current2 - 1
    while i > 0 and line[i] == ' ':
        i -= 1
    while i > 0 and line[i - 1] != ' ':
        i -= 1
    current2 = i


def move_word_right():
    global current2
    line = lines[current1]
    if current2 >= len(line):
        return
    i = current2
    while i < len(line) and line[i] != ' ':
        i += 1
    while i < len(line) and line[i] == ' ':
        i += 1
    current2 = i


def copy_line():
    global copy_text
    if lines:
        copy_text = lines[current1]


def paste_below():
    global lines, current1
    if copy_text:
        lines.insert(current1 + 1, copy_text)
        current1 += 1
        current2 = 0


def paste_above():
    global lines, current1
    if copy_text:
        lines.insert(current1, copy_text)
        current2 = 0

def move_up():
    global current1, current2
    if current1 > 0:
        current1 -= 1
        current2 = min(current2, len(lines[current1]))


def move_down():
    global current1, current2
    if current1 < len(lines) - 1:
        current1 += 1
        current2 = min(current2, len(lines[current1]))


def insert_empty_above():
    global lines, current1
    lines.insert(current1, "")


def insert_empty_below():
    global lines, current1
    lines.insert(current1 + 1, "")
    current1 += 1
    current2 = 0


def det_l():
    global lines, current1, current2
    lines.pop(current1)
    if not lines:
        current1 = 0
        current2 = 0
    else:
        current1 = min(current1, len(lines) - 1)
        current2 = min(current2, len(lines[current1]))


def show_help():
    help_menu = """? - display this help info
    ; - toggle row cursor on and off
    . - toggle line cursor on and off
    h - move cursor left
    j - move cursor up
    k - move cursor down
    l - move cursor right
    ^ - move cursor to beginning of the line
    $ - move cursor to end of the line
    w - move cursor to beginning of next word
    b - move cursor to beginning of previous word
    i - insert <text> before cursor
    a - append <text> after cursor
    x - delete character at cursor
    dw - delete word and trailing spaces at cursor
    yy - copy current line to memory
    p - paste copied line(s) below line cursor
    P - paste copied line(s) above line cursor
    dd - delete line
    o - insert empty line below
    O - insert empty line above
    u - undo previous command
    r - repeat last command
    s - show content
    q - quit program
    """
    print(help_menu)


def opts_process(opt):
    global last_opt, row_enable, col_enable

    def toggle(var_name):
        global row_enable, col_enable
        if var_name == 'row':
            row_enable = not row_enable
        elif var_name == 'col':
            col_enable = not col_enable
        display_lines()

    def repeat_last():
        if last_opt:
            opts_process(last_opt)

    def simple_action(action, save=False):
        action()
        display_lines()
        if save:
            save_state()

    def insert_or_append_text(mode, text):
        if mode == 'i':
            insert_text(text)
        elif mode == 'a':
            append_text(text)
        display_lines()
        save_state()

    if opt == ';':
        toggle('row')
    elif opt == '.':
        toggle('col')
    elif opt == 'q':
        exit()
    elif opt == '?':
        show_help()
    elif opt == 'u':
        simple_action(undo)
    elif opt == 'r':
        repeat_last()
    elif opt.startswith(('i', 'a')) and len(opt) > 1:
        insert_or_append_text(opt[0], opt[1:])
        last_opt = opt
    elif opt == 'h':
        simple_action(move_left)
        last_opt = opt
    elif opt == 'l':
        simple_action(move_right)
        last_opt = opt
    elif opt == 'b':
        simple_action(move_word_left)
        last_opt = opt
    elif opt == 'w':
        simple_action(move_word_right)
        last_opt = opt
    elif opt == 'x':
        simple_action(det_c)
        last_opt = opt
    elif opt == 'dw':
        simple_action(det_w, save=True)
        last_opt = opt
    elif opt == '$':
        simple_action(move_to_end)
        last_opt = opt
    elif opt == '^':
        simple_action(move_to_start, save=True)
        last_opt = opt
    elif opt == 'yy':
        simple_action(copy_line)
        last_opt = opt
    elif opt == 'p':
        simple_action(paste_below, save=True)
        last_opt = opt
    elif opt == 'P':
        simple_action(paste_above, save=True)
        last_opt = opt
    elif opt == 'O':
        simple_action(insert_empty_above, save=True)
        last_opt = opt
    elif opt == 'o':
        simple_action(insert_empty_below, save=True)
        last_opt = opt
    elif opt == 'dd':
        simple_action(det_l, save=True)
        last_opt = opt
    elif opt == 'j':
        simple_action(move_up)
        last_opt = opt
    elif opt == 'k':
        simple_action(move_down)
        last_opt = opt
    elif opt == 's':
        pass
    else:
        last_opt = opt

def main():
    global lines
    lines = []
    while True:
        opt = input('>')
        if not opt or opt[0] == ' ':
            continue
        opts_process(opt)


if __name__ == "__main__":
    main()
