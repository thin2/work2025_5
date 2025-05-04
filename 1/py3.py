import re
text = []  
row = 0
col = 0
copys = ""
undo_stack = []
lv_choice = None  
bool_row = False
bool_col = False
choice=['?','.',';','h','j','k','l','^','$','w','b','i','a','x','dw','yy','p','P','dd',
         'o','O','u','r','s','q']


def display():
    if not text :
        return
    for idx, line in enumerate(text):
        bool_curr_row = (idx == row)
        line_is_empty = not line.strip()
        if line_is_empty and not bool_curr_row:
            continue
        prefix = '*' if bool_row and bool_curr_row else ' ' if bool_row else ''
        print(prefix, end='')
        if bool_curr_row and bool_col and line:
            index_green = min(col, len(line) - 1)
            before = line[:index_green]
            green = '\033[42m' + line[index_green] + '\033[0m'
            after = line[index_green + 1:]
            print(before + green + after)
        else:
            print(line if not line_is_empty else "")




def save():
    undo_stack.append((text.copy(), row, col, bool_row, bool_col))

def undo():
    global text, row, col, bool_row, bool_col
    if undo_stack:
        text, row, col, bool_row, bool_col = undo_stack.pop()

def text_insert(txt):
    global text, col, row

    if not text:
        text.append("")
        row = 0
        col = 0

    line = text[row]
    text[row] = line[:col] + txt + line[col:]

def text_append(txt):
    global text, col, row
    if not text:
        text.append("")
        row = 0
        col = 0
    line = text[row]
    text[row] = line[:col] + txt + line[col:]
    col += len(txt)


def delete_c():
    global text
    line = text[row]
    if line and col < len(line):
        text[row] = line[:col] + line[col + 1:]
def delete_w():
    global text, col
    line = text[row]
    if col >= len(line):
        col =len(line.strip())-1
        return
    match = re.search(r"\s+", line[row:])
    if match:
        end = col + match.end()+1
        text[row] = line[:col] + line[end:]
    else:
        text[row] = line[:col]
def left():
    global col
    if col > 0:
        col -= 1

def right():
    global col
    if col < len(text[row]):
        col += 1

def move_to_start():
    global col
    col = 0

def move_to_end():
    global col
    col = len(text[row])

def move_word_left():
    global col
    line = text[row]
    if col == 0:
        return

    i = col - 1

    while i > 0 and line[i] == ' ':
        i -= 1

    while i > 0 and line[i - 1] != ' ':
        i -= 1

    col = i

def move_word_right():
    global col
    line = text[row]
    length = len(line)
    if col >= length:
        return
    i = col
    while i < length and line[i] != ' ':
        i += 1
    while i < length and line[i] == ' ':
        i += 1

    col = i


def copy_line():
    global copys
    if text:
        copys = text[row]

def paste_below():
    global text, row
    if copys:
        text.insert(row + 1, copys)
        row += 1
        col = 0

def paste_above():
    global text, row
    if copys:
        text.insert(row, copys)
        col = 0

def move_up():
    global row, col
    if row > 0:
        row -= 1
        col = min(col, len(text[row]))

def move_down():
    global row, col
    if row < len(text) - 1:
        row += 1
        col = min(col, len(text[row]))

def insert_empty_above():
    global text, row
    text.insert(row, "")

def insert_empty_below():
    global text, row
    text.insert(row + 1, "")
    row += 1
    col = 0


def delete_l():
    global text, row, col
    text.pop(row)
    if not text:
        row = 0
        col = 0
    else:
        row = min(row, len(text)-1)
        col = min(col, len(text[row]))

def show_help():
    for cmd in choice:
        print(cmd, end=' ')

def process_choice(cho):
    global lv_choice, bool_row, bool_col

    toggle_cmds = {
        ';': lambda: switch('row'),
        '.': lambda: switch('col')
    }
    if cho in toggle_cmds:
        toggle_cmds[cho]()
        display()
        return

    # 特殊命令
    if cho == 'q':
        exit()
    elif cho == '?':
        show_help()
        return
    elif cho == 'u':
        undo()
        display()
        return
    elif cho == 'r':
        if lv_choice:
            process_choice(lv_choice)
        return
    elif cho == 's':
        return
    else:
        lv_choice = cho

    # 插入/追加操作
    if cho.startswith('i') and len(cho) > 1:
        text_insert(cho[1:])
        return end_edit()
    elif cho.startswith('a') and len(cho) > 1:
        text_append(cho[1:])
        return end_edit()

    # 命令操作映射
    actions = {
        'h': left,
        'l': right,
        'b': move_word_left,
        'w': move_word_right,
        'x': delete_c,
        'dw': lambda: (delete_w(), save()),
        '$': move_to_end,
        '^': lambda: (move_to_start(), save()),
        'yy': copy_line,
        'p': lambda: (paste_below(), save()),
        'P': lambda: (paste_above(), save()),
        'O': lambda: (insert_empty_above(), save()),
        'o': lambda: (insert_empty_below(), save()),
        'dd': lambda: (delete_l(), save()),
        'j': move_up,
        'k': move_down
    }

    action = actions.get(cho)
    if action:
        action() if callable(action) else None
        display()

def switch(attr):
    global bool_row, bool_col
    if attr == 'row':
        bool_row = not bool_row
    elif attr == 'col':
        bool_col = not bool_col

def end_edit():
    display()
    save()


def main():
    global text
    text = []
    while True:
        cho = input('>')
        if not cho or cho[0] == ' '  :
            continue
        process_choice(cho)


if __name__ == "__main__":
    main()
