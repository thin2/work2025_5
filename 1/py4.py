import re

texts = []  
row_index = 0
col_index = 0
copy_txt = ""  
undo_stack = []  
last_option = None  
row_bool = False
col_bool = False
option=['?','.',';','h','j','k','l','^','$','w','b','i','a','x','dw','yy','p','P','dd',
         'o','O','u','r','s','q']


def display_texts():
    HIGHLIGHT_START = '\033[42m'
    HIGHLIGHT_END = '\033[0m'

    def should_skip_line(line: str, bool_cur: bool) -> bool:
        return not line.strip() and not bool_cur
    def get_line_prefix(bool_cur: bool) -> str:
        return '*' if row_bool and bool_cur else ' '
    def apply_cursor_highlight(line: str) -> str:
        if not line:
            return HIGHLIGHT_START + ' ' + HIGHLIGHT_END

        cursor_pos = min(col_index, len(line) - 1)
        return (line[:cursor_pos]
                + HIGHLIGHT_START
                + line[cursor_pos]
                + HIGHLIGHT_END
                + line[cursor_pos + 1:])
    if not texts:
        return
    for idx, line in enumerate(texts):
        bool_cur = (idx == row_index)
        if should_skip_line(line, bool_cur):
            continue
        prefix = get_line_prefix(bool_cur) if row_bool else ''
        if bool_cur and col_bool:
            displayed_line = apply_cursor_highlight(line)
        else:
            displayed_line = line if line.strip() else ''

        print(f"{prefix}{displayed_line}")


def cur_state():
    undo_stack.append((texts.copy(), row_index, col_index, row_bool, col_bool))
def undo():
    global texts, row_index, col_index, row_bool, col_bool
    if undo_stack:
        texts, row_index, col_index, row_bool, col_bool = undo_stack.pop()

def insert_line(text):
    global texts, col_index, row_index
    if not texts:
        texts.append("")
        row_index = 0
        col_index = 0
    line = texts[row_index]
    texts[row_index] = line[:col_index] + text + line[col_index:]
def appent_line(text):
    global texts, col_index, row_index
    if not texts:
        texts.append("")
        row_index = 0
        col_index = 0
    line = texts[row_index]
    texts[row_index] = line[:col_index] + text + line[col_index:]
    col_index += len(text)

def det_char():
    global texts
    line = texts[row_index]
    if line and col_index < len(line):
        texts[row_index] = line[:col_index] + line[col_index + 1:]

def det_word():
    global texts, col_index
    line = texts[row_index]
    if col_index >= len(line):
        col_index =len(line.strip())-1

        return
 
    pattern = re.search(r"\s+", line[row_index:])
    if pattern:
        end = col_index + pattern.end()+1
        texts[row_index] = line[:col_index] + line[end:]
    else:
        texts[row_index] = line[:col_index]

def move_left():
    global col_index
    if col_index > 0:
        col_index -= 1

def move_right():
    global col_index
    if col_index < len(texts[row_index]):
        col_index += 1


def move_to_start():
    global col_index
    col_index = 0

def move_to_end():
    global col_index
    col_index = len(texts[row_index])

def move_word_left():
    global col_index
    line = texts[row_index]
    if col_index == 0:
        return
    i = col_index - 1
    while i > 0 and line[i] == ' ':
        i -= 1
    while i > 0 and line[i - 1] != ' ':
        i -= 1
    col_index = i

def move_word_right():
    global col_index
    line = texts[row_index]
    if col_index >= len(line):
        return
    i = col_index
    while i < len(line) and line[i] != ' ':
        i += 1
    while i < len(line) and line[i] == ' ':
        i += 1
    col_index = i

def copy_line():
    global copy_txt
    if texts:
        copy_txt = texts[row_index]

def paste_below():
    global texts, row_index
    if copy_txt:
        texts.insert(row_index + 1, copy_txt)
        row_index += 1
        col_index = 0

def paste_above():
    global texts, row_index
    if copy_txt:
        texts.insert(row_index, copy_txt)
        col_index = 0


def up():
    global row_index, col_index
    if row_index > 0:
        row_index -= 1
        col_index = min(col_index, len(texts[row_index]))

def down():
    global row_index, col_index
    if row_index < len(texts) - 1:
        row_index += 1
        col_index = min(col_index, len(texts[row_index]))

# 当前行上插入空行
def insert_empty_above():
    global texts, row_index
    texts.insert(row_index, "")

# 当前行下插入空行
def insert_empty_below():
    global texts, row_index
    texts.insert(row_index + 1, "")
    row_index += 1
    col_index = 0


def det_line():
    global texts, row_index, col_index
    texts.pop(row_index)
    if not texts:
        row_index = 0
        col_index = 0
    else:
        row_index = min(row_index, len(texts)-1)
        col_index = min(col_index, len(texts[row_index]))


def show_help():
    text = """Available commands:
    ? – display help
    . – toggle row cursor
    ; – toggle line cursor
    h – move left
    j – move down
    k – move up
    l – move right
    ^ – move to line start
    $ – move to line end
    w – next word
    b – previous word
    i<text> – insert text
    a<text> – append text
    x – delete char
    dw – delete word
    yy – copy line
    dd – delete line
    p – paste below
    P – paste above
    o – insert line below
    O – insert line above
    u – undo
    r – repeat last command
    s – show content
    q – quit"""
    print(text)


def process_option(option):
    global last_option
    global row_bool, col_bool

    if option == ';':
        row_bool = not row_bool
        display_texts()
        return
    elif option == '.':
        col_bool = not col_bool
        display_texts()
        return
    elif option == 'q':
        exit()
    elif option == '?':
        show_help()
        return
    elif option == 'u':
        undo()
        display_texts()
        return
    elif option == 'r':
        if last_option:
            process_option(last_option)
        return
    elif option == 's':
        pass
    else:
        last_option = option

    if option.startswith('i') and len(option) > 1:
        insert_line(option[1:])
        need_state = True
    elif option.startswith('a') and len(option) > 1:
        appent_line(option[1:])
        need_state = True
    elif option == 'h':
        move_left()
        need_state = False
    elif option == 'l':
        move_right()
        need_state = False
    elif option == 'b':
        move_word_left()
        need_state = False
    elif option == 'w':
        move_word_right()
        need_state = False
    elif option == 'x':
        det_char()
        need_state = False
    elif option == 'dw':
        det_word()
        need_state = True
    elif option == '$':
        move_to_end()
        need_state = False
    elif option == '^':
        move_to_start()
        need_state = True
    elif option == 'yy':
        copy_line()
        need_state = False
    elif option == 'p':
        paste_below()
        need_state = True
    elif option == 'P':
        paste_above()
        need_state = True
    elif option == 'O':
        insert_empty_above()
        need_state = True
    elif option == 'o':
        insert_empty_below()
        need_state = True
    elif option == 'dd':
        det_line()
        need_state = True
    elif option == 'j':
        up()
        need_state = False
    elif option == 'k':
        down()
        need_state = False
    else:
        return

    display_texts()
    if 'need_state' in locals() and need_state:
        cur_state()


# 主循环
def main():
    global texts
    texts = []
    while True:
        option = input('>')
        if not option or option[0] == ' '  :
            continue
        process_option(option)


if __name__ == "__main__":
    main()
