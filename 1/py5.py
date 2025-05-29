import re

lines = []
current1= 0
current2 = 0
copy_text = ''
UndoStack = []
last_opt = None
row_enable = False
col_enable = False
opts=['?','.',';','h','j','k','l','^','$','w','b','i','a','x','dw','yy','p','P','dd',
         'o','O','u','r','s','q']


def display():
    for idx, line in enumerate(lines):
        is_current = ((idx+1) == current1)

        is_empty = not line.strip()
        if row_enable and is_current:
            prefix = '*'
        elif row_enable:
            prefix = ' '
        else:
            prefix = ''
        print(prefix, end='')
        if is_current and col_enable and line:
            cursor_index = min(current2, len(line) - 1)
            print(line[:cursor_index] + '\033[42m' + line[cursor_index] + '\033[0m' + line[cursor_index + 1:])
        elif not is_empty:
            print(line)
        elif is_current:
            print()
        else:
            print()


def save_state():
    print(last_opt)
    UndoStack.append((lines.copy(), current1, current2, row_enable, col_enable, copy_text, last_opt))

def undo():
    global lines, current1, current2, row_enable, col_enable, copy_text,last_opt
    if UndoStack:
        lines, current1, current2, row_enable, col_enable, copy_text,last_opt = UndoStack.pop()


def insert_text(text):
    global lines, current2, current1
    if not lines:
        lines.append("")
        current1= 1
        current2 = 0
    current11=max(0,current1-1)
    line = lines[current11]
    lines[current11] = line[:current2] + text + line[current2:]
    # current2 += len(text)

def append_text(text):
    global lines, current2, current1
    if not lines:
        lines.append("")
        current1= 1
        current2 = 0
    current11=max(0,current1-1)
    line = lines[current11]
    lines[current11] = line[:current2+1] + text + line[current2+1:]
    if current2==0:
        current2 += len(text)-1
    else:
        current2 += len(text)

def delete_char():
    global lines
    if not lines:
        return
    current11=max(0,current1-1)
    line = lines[current11]
    if line and current2 < len(line):
        lines[current11] = line[:current2] + line[current2 + 1:]

def delete_word():
    global lines, current2
    current11=max(0,current1-1)
    if not lines:
        return
    line = lines[current11]
    if current2 >= len(line):
        current2 =len(line.strip())-1
        return
    match = re.search(r'\s*(\S+\s*)', line[current2:])
    if match:
        end = current2 + match.end()

        lines[current11] = line[:current2] + line[end:]
    else:
        lines[current11] = line[:current2]

def move_left():
    global current2
    if current2 > 0:
        current2 -= 1

def move_right():
    global current2,  current1
    current11=max(0,current1-1)
    if  not lines:
        current2 = 0
        return
    line = lines[current11]
    if not line:
        current2 = 0
        return
    if current2 < len(lines[current11]):
        current2 += 1

def move_to_start():
    global current2
    current2 = 0

def move_to_end():
    global current2
    current11=max(0,current1-1)
    current2 = len(lines[current11])

def move_word_left():
    global current2
    current11=max(0,current1-1)
    if not lines:
        current2 = 0
        return
    line = lines[current11]
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
    current11=max(0,current1-1)
    if not lines:
        current2 = 0
        return
    line = lines[current11]
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
    current11=max(0,current1-1)
    if lines:
        copy_text = lines[current11]
def paste_below():
    global lines, current1
    if copy_text:
        lines.insert(current1+ 1, copy_text)
        current1+= 1
def paste_above():
    global lines, current1
    if copy_text:
        lines.insert(current1, copy_text)
def move_up():
    global current1, current2
    current11=max(0,current1-1)
    if current1> 1:
        current1-= 1
        current2 = min(current2, len(lines[current1]))

def move_down():
    global current1, current2
    if current1< len(lines) :
        current1+= 1
        current2 = min(current2, len(lines[current1]))

def insert_empty_above():
    global lines, current1
    current11=max(0,current1-1)
    lines.insert(current11, "")

def insert_empty_below():
    global lines, current1
    lines.insert(current1+ 1, "")
    current1+= 1
    # current2 = 0

def delete_line():
    global lines, current1, current2
    lines.pop(current1)
    if not lines:
        current1= 0
        current2 = 0
    else:
        current1= min(current1, len(lines)-1)
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
u - undo previous opts
r - repeat last opts
s - show lines
q - quit program
"""
    print(help_menu)

def process_opts(opt):
    global last_opt
    global row_enable, col_enable
    if opt == ';':
        if row_enable:
            row_enable = False
        else:
            row_enable = True
        display()
        return
    elif opt == '.':
        if col_enable:
            col_enable = False
        else:
            col_enable = True
        display()
        return

    if opt == 'q':
        exit()
    if opt == '?':
        show_help()
        return
    if opt == 'u':
        undo()
        display()
        return
    if opt == 'r':
        if last_opt:
            process_opts(last_opt)
        return

    if opt.startswith('i') and len(opt) > 1:
        save_state()
        insert_text(opt[1:])
        display()
        last_opt = opt
    elif opt.startswith('a') and len(opt) > 1:
        save_state()
        append_text(opt[1:])
        display()
        last_opt = opt
    elif opt == 'h':
        move_left()
        display()
    elif opt == 'l':
        move_right()
        display()
    elif opt == 'b':
        move_word_left()
        display()
    elif opt == 'w':
        move_word_right()
        display()
    elif opt == 'x':
        delete_char()
        display()
        last_opt = opt
    elif opt == 'dw':
        save_state()
        delete_word()
        display()
        last_opt = opt
    elif opt == '$':
        move_to_end()
        display()
    elif opt == '^':
        save_state()
        move_to_start()
        display()
        last_opt = opt

    elif opt == 'yy':
        save_state()
        copy_line()
        display()
        last_opt = opt
    elif opt == 'p':
        save_state()
        paste_below()
        display()
        last_opt = opt
    elif opt == 'P':
        save_state()
        paste_above()
        display()
        last_opt = opt

    elif opt == 'O':
        save_state()
        insert_empty_above()
        display()
        last_opt = opt

    elif opt == 'o':
        save_state()
        insert_empty_below()
        display()
        last_opt = opt

    elif opt == 'dd':
        save_state()
        delete_line()
        display()
        last_opt = opt

    elif opt == 'j':
        save_state()
        move_up()
        display()
        last_opt = opt
    elif opt == 'k':
        move_down()
        display()
    elif opt=='s':
        display()

def main():
    global lines
    lines = []
    while True:
        opt = input('>')
        if not opt or opt[0] == ' '  :
            continue
        process_opts(opt)


if __name__ == "__main__":
    main()
