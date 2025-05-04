import re

# Global variables
content = []  
line_cursor = 0  
row_cursor = 0  
undo_stack = []  
last_command = None  
copied_line = None  
show_line_cursor = False  
show_row_cursor = False  

def main():
    global content, line_cursor, row_cursor, show_line_cursor, show_row_cursor
    content = [""]
    line_cursor = 0
    row_cursor = 0
    show_line_cursor = False
    show_row_cursor = False

    while True:
        try:
            cmd = input(">")
        except EOFError:
            break

        if cmd == "q":
            break

        action, text = parse_command(cmd)
        if action is None:
            continue

        # Save state before executing command (except for ?, s, u, r)
        if action not in ["?", "s", "u", "r"]:
            update_undo_stack()

        handle_command(action, text)

        # Update last_command for repeat (excluding u, r)
        if action not in ["?", "s", "u", "r"]:
            last_command = (action, text)

        # Display content after command (except for ?, s)
        if action not in ["?", "s"]:
            display_content()

    return

def parse_command(cmd):
    if not cmd:
        return None, None

    # Single character commands
    single_commands = {"?", ".", ";", "h", "j", "k", "l", "^", "$", "x", "u", "r", "s", "o", "O", "q"}
    if cmd in single_commands:
        return cmd, None

    # Two character commands
    two_commands = {"dw", "yy", "dd"}
    if len(cmd) >= 2 and cmd[:2] in two_commands:
        return cmd[:2], cmd[2:].strip()

    # Commands with text: i, a
    text_commands = {"i", "a"}
    if len(cmd) >= 1 and cmd[0] in text_commands:
        return cmd[0], cmd[1:]

    # Line paste commands
    if cmd in ["p", "P"]:
        return cmd, None

    # Invalid command
    return None, None

def handle_command(action, text):
    global content, line_cursor, row_cursor, show_line_cursor, show_row_cursor, copied_line

    if action == "?":
        print_help()
    elif action == ".":
        show_row_cursor = not show_row_cursor
    elif action == ";":
        show_line_cursor = not show_line_cursor
    elif action == "h":
        move_left()
    elif action == "l":
        move_right()
    elif action == "j":
        move_up()
    elif action == "k":
        move_down()
    elif action == "^":
        move_line_start()
    elif action == "$":
        move_line_end()
    elif action == "w":
        move_next_word()
    elif action == "b":
        move_prev_word()
    elif action == "i":
        insert_text(text)
    elif action == "a":
        append_text(text)
    elif action == "x":
        delete_char()
    elif action == "dw":
        delete_word()
    elif action == "yy":
        copy_line()
    elif action == "dd":
        delete_line()
    elif action == "p":
        paste_line(below=True)
    elif action == "P":
        paste_line(below=False)
    elif action == "o":
        insert_empty_line(below=True)
    elif action == "O":
        insert_empty_line(below=False)
    elif action == "u":
        undo()
    elif action == "r":
        repeat_last_command()

    adjust_cursor()

def adjust_cursor():
    global line_cursor, row_cursor, content
    line_cursor = max(0, min(len(content)-1, line_cursor))
    current_line = content[line_cursor]
    row_cursor = max(0, min(len(current_line), row_cursor))

def move_left():
    global row_cursor
    row_cursor = max(0, row_cursor - 1)

def move_right():
    global row_cursor, line_cursor
    current_line = content[line_cursor]
    row_cursor = min(len(current_line), row_cursor + 1)

def move_up():
    global line_cursor, row_cursor
    if line_cursor > 0:
        line_cursor -= 1
        current_line = content[line_cursor]
        row_cursor = min(row_cursor, len(current_line))

def move_down():
    global line_cursor, row_cursor
    if line_cursor < len(content) - 1:
        line_cursor += 1
        current_line = content[line_cursor]
        row_cursor = min(row_cursor, len(current_line))

def move_line_start():
    global row_cursor
    row_cursor = 0

def move_line_end():
    global row_cursor, line_cursor
    row_cursor = len(content[line_cursor])


def move_next_word():
    global row_cursor, line_cursor
    line = content[line_cursor]
    if row_cursor >= len(line):
        return

    match = re.search(r'\S', line[row_cursor + 1:])
    if match:
        row_cursor += match.start() + 1
    else:
        row_cursor = len(line)


def move_prev_word():
    global row_cursor
    line = content[line_cursor]
    if row_cursor == 0:
        return

    # 找到row_cursor前的所有非空格块
    matches = list(re.finditer(r'\S+', line[:row_cursor]))
    if matches:
        row_cursor = matches[-1].start()
    else:
        row_cursor = 0


def insert_text(text):
    global content, line_cursor, row_cursor
    if not text:
        return

    current_line = content[line_cursor]
    new_line = current_line[:row_cursor] + text + current_line[row_cursor:]
    content[line_cursor] = new_line

def append_text(text):
    global content, line_cursor, row_cursor
    if not text:
        return

    current_line = content[line_cursor]
    new_line = current_line[:row_cursor + 1] + text + current_line[row_cursor + 1:]
    content[line_cursor] = new_line
    row_cursor += len(text)  # 移动到插入文本末尾

def delete_char():
    global content, line_cursor, row_cursor
    current_line = content[line_cursor]
    if row_cursor < len(current_line):
        new_line = current_line[:row_cursor] + current_line[row_cursor+1:]
        content[line_cursor] = new_line

def delete_word():
    global content, line_cursor, row_cursor
    current_line = content[line_cursor]
    if row_cursor >= len(current_line):
        return

    remaining = current_line[row_cursor:]
    match = re.search(r'^\S*\s*', remaining)
    if match:
        end = row_cursor + match.end()
        content[line_cursor] = current_line[:row_cursor] + current_line[end:]

def copy_line():
    global copied_line, line_cursor
    if content:
        copied_line = content[line_cursor]

def delete_line():
    global content, line_cursor
    if len(content) == 1:
        content = [""]
    else:
        del content[line_cursor]
        line_cursor = max(0, min(line_cursor, len(content)-1))

def paste_line(below):
    global content, line_cursor, copied_line
    if copied_line is None:
        return

    target = line_cursor + 1 if below else line_cursor
    content.insert(target, copied_line)
    line_cursor = target

def insert_empty_line(below):
    global content, line_cursor
    target = line_cursor + 1 if below else line_cursor
    content.insert(target, "")
    line_cursor = target

def undo():
    global content, line_cursor, row_cursor, undo_stack
    if not undo_stack:
        return

    prev_state = undo_stack.pop()
    content = prev_state["content"]
    line_cursor = prev_state["line"]
    row_cursor = prev_state["row"]

def repeat_last_command():
    if last_command:
        action, text = last_command
        handle_command(action, text)

def update_undo_stack():
    undo_stack.append({
        "content": list(content),
        "line": line_cursor,
        "row": row_cursor
    })

def display_content():
    for i, line in enumerate(content):
        prefix = "*" if show_line_cursor and i == line_cursor else " "
        line_str = f"{prefix}{line}"

        if i == line_cursor and show_row_cursor and len(line) > 0:
            if row_cursor <= len(line):
                before = line[:row_cursor]
                after = line[row_cursor:]
                line_str = f"{prefix}{before}\033[42m{after[0] if after else ' '}\033[0m{after[1:]}"
            else:
                line_str = f"{prefix}{line}\033[42m \033[0m"

        print(line_str)

def print_help():
    help_text = """Available commands:
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
    print(help_text)

if __name__ == "__main__":
    main()