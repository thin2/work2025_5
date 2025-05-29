import re

content = []
cursor_row = 0
cursor_col = 0
clipboard = ''
undo_stack = []
last_valid_command = None
row_cursor_enabled = False
col_cursor_enabled = False
command=['?','.',';','h','j','k','l','^','$','w','b','i','a','x','dw','yy','p','P','dd',
         'o','O','u','r','s','q']

# 输出编辑器内容
def display_content():
    # if content == [] :
    #     return
    # print(content)

    for idx, line in enumerate(content):
        is_current = ((idx+1) == cursor_row)
        # print(idx,cursor_row)
        is_empty = not line.strip()
        # if is_empty and not is_current:
        #     continue
        if row_cursor_enabled and is_current:
            prefix = '*'
        elif row_cursor_enabled:
            prefix = ' '
        else:
            prefix = ''

        print(prefix, end='')

        if is_current and col_cursor_enabled and line:
            cursor_index = min(cursor_col, len(line) - 1)
            print(line[:cursor_index] + '\033[42m' + line[cursor_index] + '\033[0m' + line[cursor_index + 1:])
        elif not is_empty:
            print(line)
        elif is_current:
            print()
        else:
            print()


def save_state():
    print(last_valid_command)
    undo_stack.append((content.copy(), cursor_row, cursor_col, row_cursor_enabled, col_cursor_enabled, clipboard, last_valid_command))

def undo():
    global content, cursor_row, cursor_col, row_cursor_enabled, col_cursor_enabled, clipboard,last_valid_command
    if undo_stack:
        content, cursor_row, cursor_col, row_cursor_enabled, col_cursor_enabled, clipboard,last_valid_command = undo_stack.pop()


def insert_text(text):
    global content, cursor_col, cursor_row
    if not content:
        content.append("")
        cursor_row = 1
        cursor_col = 0
    cursor_row1=max(0,cursor_row-1)
    line = content[cursor_row1]
    content[cursor_row1] = line[:cursor_col] + text + line[cursor_col:]
    # cursor_col += len(text)

def append_text(text):
    global content, cursor_col, cursor_row
    if not content:
        content.append("")
        cursor_row = 1
        cursor_col = 0
    cursor_row1=max(0,cursor_row-1)
    line = content[cursor_row1]
    content[cursor_row1] = line[:cursor_col+1] + text + line[cursor_col+1:]
    if cursor_col==0:
        cursor_col += len(text)-1
    else:
        cursor_col += len(text)

def delete_char():
    global content
    if not content:
        return
    cursor_row1=max(0,cursor_row-1)
    line = content[cursor_row1]
    if line and cursor_col < len(line):
        content[cursor_row1] = line[:cursor_col] + line[cursor_col + 1:]

def delete_word():
    global content, cursor_col
    cursor_row1=max(0,cursor_row-1)
    if not content:
        return
    line = content[cursor_row1]
    if cursor_col >= len(line):
        cursor_col =len(line.strip())-1
        return
    match = re.search(r'\s*(\S+\s*)', line[cursor_col:])
    if match:
        end = cursor_col + match.end()

        content[cursor_row1] = line[:cursor_col] + line[end:]
    else:
        content[cursor_row1] = line[:cursor_col]


# 移动光标左/右
def move_left():
    global cursor_col
    if cursor_col > 0:
        cursor_col -= 1

def move_right():
    global cursor_col,  cursor_row
    cursor_row1=max(0,cursor_row-1)
    if  not content:
        cursor_col = 0
        return
    line = content[cursor_row1]
    if not line:
        cursor_col = 0
        return
    if cursor_col < len(content[cursor_row1]):
        cursor_col += 1

# 移动到行首/行尾
def move_to_start():
    global cursor_col
    cursor_col = 0

def move_to_end():
    global cursor_col
    cursor_row1=max(0,cursor_row-1)
    cursor_col = len(content[cursor_row1])

def move_word_left():
    global cursor_col
    cursor_row1=max(0,cursor_row-1)
    if not content:
        cursor_col = 0
        return
    line = content[cursor_row1]
    if cursor_col == 0:
        return
    i = cursor_col - 1
    while i > 0 and line[i] == ' ':
        i -= 1
    while i > 0 and line[i - 1] != ' ':
        i -= 1
    cursor_col = i

def move_word_right():
    global cursor_col
    cursor_row1=max(0,cursor_row-1)
    if not content:
        cursor_col = 0
        return
    line = content[cursor_row1]
    if cursor_col >= len(line):
        return
    i = cursor_col
    while i < len(line) and line[i] != ' ':
        i += 1
    while i < len(line) and line[i] == ' ':
        i += 1
    cursor_col = i

# 复制当前行
def copy_line():
    global clipboard
    cursor_row1=max(0,cursor_row-1)
    if content:
        clipboard = content[cursor_row1]

# 粘贴行到当前行下方
def paste_below():
    global content, cursor_row
    if clipboard:
        content.insert(cursor_row + 1, clipboard)
        cursor_row += 1


# 粘贴行到当前行上方
def paste_above():
    global content, cursor_row
    if clipboard:
        content.insert(cursor_row, clipboard)


# 上移一行
def move_up():
    global cursor_row, cursor_col
    cursor_row1=max(0,cursor_row-1)
    if cursor_row > 1:
        cursor_row -= 1
        cursor_col = min(cursor_col, len(content[cursor_row]))

# 下移一行
def move_down():
    global cursor_row, cursor_col
    if cursor_row < len(content) :
        cursor_row += 1
        cursor_col = min(cursor_col, len(content[cursor_row]))

# 当前行上插入空行
def insert_empty_above():
    global content, cursor_row
    cursor_row1=max(0,cursor_row-1)
    content.insert(cursor_row1, "")

# 当前行下插入空行
def insert_empty_below():
    global content, cursor_row
    content.insert(cursor_row + 1, "")
    cursor_row += 1
    # cursor_col = 0

# 删除当前行
def delete_line():
    global content, cursor_row, cursor_col
    content.pop(cursor_row)
    if not content:
        cursor_row = 0
        cursor_col = 0
    else:
        cursor_row = min(cursor_row, len(content)-1)
        cursor_col = min(cursor_col, len(content[cursor_row]))

# 显示帮助菜单
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

# 解析并执行命令
def process_command(cmd):
    global last_valid_command
    global row_cursor_enabled, col_cursor_enabled
    if cmd == ';':
        if row_cursor_enabled:
            row_cursor_enabled = False
        else:
            row_cursor_enabled = True
        display_content()
        return
    elif cmd == '.':
        if col_cursor_enabled:
            col_cursor_enabled = False
        else:
            col_cursor_enabled = True
        display_content()
        return

    if cmd == 'q':
        exit()
    if cmd == '?':
        show_help()
        return
    if cmd == 'u':
        undo()
        display_content()
        return
    if cmd == 'r':

        if last_valid_command:
            process_command(last_valid_command)
        return


    # if cmd == ';':
    #     if row_cursor_enabled:
    #         row_cursor_enabled = False
    #     else:
    #         row_cursor_enabled = True
    #     display_content()
    #     return
    # elif cmd == '.':
    #     if col_cursor_enabled:
    #         col_cursor_enabled = False
    #     else:
    #         col_cursor_enabled = True
    #     display_content()
    #     return
    if cmd.startswith('i') and len(cmd) > 1:
        save_state()
        insert_text(cmd[1:])
        display_content()
        last_valid_command = cmd
    elif cmd.startswith('a') and len(cmd) > 1:
        save_state()
        append_text(cmd[1:])
        display_content()
        last_valid_command = cmd
    elif cmd == 'h':

        move_left()
        display_content()
    elif cmd == 'l':
        move_right()
        display_content()
    elif cmd == 'b':
        move_word_left()
        display_content()
    elif cmd == 'w':
        move_word_right()
        display_content()
    elif cmd == 'x':
        delete_char()
        display_content()
        last_valid_command = cmd
    elif cmd == 'dw':
        save_state()
        delete_word()
        display_content()
        last_valid_command = cmd
    elif cmd == '$':
        move_to_end()
        display_content()
    elif cmd == '^':
        save_state()
        move_to_start()
        display_content()
        last_valid_command = cmd

    elif cmd == 'yy':
        save_state()
        copy_line()
        display_content()
        last_valid_command = cmd
    elif cmd == 'p':
        save_state()
        paste_below()
        display_content()
        last_valid_command = cmd
    elif cmd == 'P':
        save_state()
        paste_above()
        display_content()
        last_valid_command = cmd

    elif cmd == 'O':
        save_state()
        insert_empty_above()
        display_content()
        last_valid_command = cmd

    elif cmd == 'o':
        save_state()
        insert_empty_below()
        display_content()
        last_valid_command = cmd

    elif cmd == 'dd':
        save_state()
        delete_line()
        display_content()
        last_valid_command = cmd

    elif cmd == 'j':
        save_state()
        move_up()
        display_content()
        last_valid_command = cmd
    elif cmd == 'k':
        move_down()
        display_content()
    elif cmd=='s':
        display_content()

# 主循环
def main():
    global content
    content = []
    while True:
        cmd = input('>')
        if not cmd or cmd[0] == ' '  :
            continue
        process_command(cmd)


if __name__ == "__main__":
    main()
