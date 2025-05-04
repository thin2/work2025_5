import re

editor_buffer = []
line_cursor = 0
char_cursor = 0
copy_buffer = ''
history_stack = []
last_command = None
line_highlight = False
char_highlight = False
valid_commands = ['?', '.', ';', 'h', 'j', 'k', 'l', '^', '$', 'w', 'b', 'i', 'a', 'x', 'dw', 'yy', 'p', 'P', 'dd',
                  'o', 'O', 'u', 'r', 's', 'q']

def show_editor():
    if not editor_buffer:
        return
    for idx, line in enumerate(editor_buffer):
        is_active = (idx == line_cursor)
        if not line.strip() and not is_active:
            continue
        print(get_line_prefix(is_active), end='')
        if is_active and char_highlight and line:
            print(highlight_char(line, char_cursor))
        else:
            print(line)

def get_line_prefix(is_active):
    if not line_highlight:
        return ''
    return '*' if is_active else ' '

def highlight_char(text, cursor_pos):
    if not text:
        return ''
    pos = min(cursor_pos, len(text) - 1)
    return f"{text[:pos]}\033[42m{text[pos]}\033[0m{text[pos+1:]}"

def backup_state():
    history_stack.append((editor_buffer.copy(), line_cursor, char_cursor, line_highlight, char_highlight, copy_buffer))

def restore_state():
    global editor_buffer, line_cursor, char_cursor, line_highlight, char_highlight, copy_buffer
    if history_stack:
        editor_buffer, line_cursor, char_cursor, line_highlight, char_highlight, copy_buffer = history_stack.pop()

def insert_at_cursor(text):
    global editor_buffer, char_cursor, line_cursor
    if not editor_buffer:
        editor_buffer.append("")
        line_cursor = 0
        char_cursor = 0

    line = editor_buffer[line_cursor]
    editor_buffer[line_cursor] = line[:char_cursor] + text + line[char_cursor:]

def append_at_cursor(text):
    global editor_buffer, char_cursor, line_cursor
    if not editor_buffer:
        editor_buffer.append("")
        line_cursor = 0
        char_cursor = 0
    line = editor_buffer[line_cursor]
    editor_buffer[line_cursor] = line[:char_cursor] + text + line[char_cursor:]
    char_cursor += len(text)

def delete_character():
    global editor_buffer
    line = editor_buffer[line_cursor]
    if line and char_cursor < len(line):
        editor_buffer[line_cursor] = line[:char_cursor] + line[char_cursor + 1:]

import re

def delete_next_word():
    global editor_buffer, char_cursor

    line = editor_buffer[line_cursor]
    if char_cursor >= len(line):
        char_cursor = len(line.strip())-1
        return
    remainder = line[char_cursor:]
    match = re.match(r'\s*(\S+\s*)', remainder)
    if match:
        end = char_cursor + match.end()
        editor_buffer[line_cursor] = line[:char_cursor] + line[end:]
    else:

        editor_buffer[line_cursor] = line[:char_cursor]


def cursor_left():
    global char_cursor
    if char_cursor > 0:
        char_cursor -= 1

def cursor_right():
    global char_cursor
    if char_cursor < len(editor_buffer[line_cursor]):
        char_cursor += 1

def move_line_start():
    global char_cursor
    char_cursor = 0

def move_line_end():
    global char_cursor
    char_cursor = len(editor_buffer[line_cursor])

def move_word_back():
    global char_cursor
    line = editor_buffer[line_cursor]
    if char_cursor == 0:
        return
    i = char_cursor - 1
    while i > 0 and line[i] == ' ':
        i -= 1
    while i > 0 and line[i - 1] != ' ':
        i -= 1
    char_cursor = i

def move_word_forward():
    global char_cursor
    line = editor_buffer[line_cursor]
    if char_cursor >= len(line):
        return
    i = char_cursor
    while i < len(line) and line[i] != ' ':
        i += 1
    while i < len(line) and line[i] == ' ':
        i += 1
    char_cursor = i

def copy_current_line():
    global copy_buffer
    if editor_buffer:
        copy_buffer = editor_buffer[line_cursor]

def paste_line_below():
    global editor_buffer, line_cursor
    if copy_buffer:
        editor_buffer.insert(line_cursor + 1, copy_buffer)
        line_cursor += 1

def paste_line_above():
    global editor_buffer, line_cursor
    if copy_buffer:
        editor_buffer.insert(line_cursor, copy_buffer)

def move_line_up():
    global line_cursor, char_cursor
    if line_cursor > 0:
        line_cursor -= 1
        char_cursor = min(char_cursor, len(editor_buffer[line_cursor]))

def move_line_down():
    global line_cursor, char_cursor
    if line_cursor < len(editor_buffer) - 1:
        line_cursor += 1
        char_cursor = min(char_cursor, len(editor_buffer[line_cursor]))

def insert_blank_above():
    global editor_buffer, line_cursor
    editor_buffer.insert(line_cursor, "")

def insert_blank_below():
    global editor_buffer, line_cursor
    editor_buffer.insert(line_cursor + 1, "")
    line_cursor += 1


def delete_current_line():
    global editor_buffer, line_cursor, char_cursor
    editor_buffer.pop(line_cursor)
    if not editor_buffer:
        line_cursor = 0
        char_cursor = 0
    else:
        line_cursor = min(line_cursor, len(editor_buffer)-1)
        char_cursor = min(char_cursor, len(editor_buffer[line_cursor]))

def print_help_menu():
    print("Available Commands:")
    print("  i<text> : Insert <text> at cursor")
    print("  a<text> : Append <text> after cursor")
    print("  h       : Move cursor left")
    print("  l       : Move cursor right")
    print("  j       : Move cursor up")
    print("  k       : Move cursor down")
    print("  b       : Move cursor to beginning of previous word")
    print("  w       : Move cursor to beginning of next word")
    print("  ^       : Move cursor to beginning of the line")
    print("  $       : Move cursor to end of the line")
    print("  x       : Delete character under cursor")
    print("  dw      : Delete word starting at cursor")
    print("  dd      : Delete current line")
    print("  yy      : Yank (copy) current line")
    print("  p       : Put (paste) yanked line below current line")
    print("  P       : Put (paste) yanked line above current line")
    print("  o       : Open (insert) blank line below and move cursor to it")
    print("  O       : Open (insert) blank line above and move cursor to it")
    print("  u       : Undo last change")
    print("  r       : Redo/Repeat last command (if supported)")  # Clarified 'r'
    print("  ;       : switch row cursor visibility (*)")
    print("  .       : switch column cursor visibility (highlight)")
    print("  ?       : Show this help message")
    print("  q       : Quit the editor")

def handle_command(command_input):
    global last_command, line_highlight, char_highlight

    if not command_input:
        return

    def handle_switch_command(cmd):
        global line_highlight, char_highlight
        if cmd == ';':
            line_highlight = not line_highlight
        elif cmd == '.':
            char_highlight = not char_highlight
        show_editor()

    def handle_text_command(cmd):
        op, text = cmd[0], cmd[1:]
        if not text:
            return
        if op == 'i':
            insert_at_cursor(text)
        elif op == 'a':
            append_at_cursor(text)
        show_editor()
        backup_state()

    def handle_action_command(cmd):
        global last_command
        command_actions = {
            'q': lambda: exit(),
            '?': print_help_menu,
            'u': lambda: (restore_state(), show_editor()),
            'r': lambda: handle_command(last_command) if last_command else None,
            'h': lambda: (cursor_left(), show_editor()),
            'l': lambda: (cursor_right(), show_editor()),
            'b': lambda: (move_word_back(), show_editor()),
            'w': lambda: (move_word_forward(), show_editor()),
            'x': lambda: (delete_character(), show_editor()),
            'dw': lambda: (delete_next_word(), show_editor(), backup_state()),
            '$': lambda: (move_line_end(), show_editor()),
            '^': lambda: (move_line_start(), show_editor(), backup_state()),
            'yy': lambda: (backup_state(), copy_current_line(), show_editor()),
            'p': lambda: (paste_line_below(), show_editor(), backup_state()),
            'P': lambda: (paste_line_above(), show_editor(), backup_state()),
            'O': lambda: (insert_blank_above(), show_editor(), backup_state()),
            'o': lambda: (insert_blank_below(), show_editor(), backup_state()),
            'dd': lambda: (delete_current_line(), show_editor(), backup_state()),
            'j': lambda: (move_line_up(), show_editor()),
            'k': lambda: (move_line_down(), show_editor())
        }

        action = command_actions.get(cmd)
        if action:
            action()

    if command_input in (';', '.'):
        handle_switch_command(command_input)
    elif command_input.startswith(('i', 'a')):
        handle_text_command(command_input)
        last_command = command_input
    else:
        handle_action_command(command_input)
        if command_input  not in ('u', 'r'):
            last_command = command_input

def launch_editor():
    global editor_buffer
    editor_buffer = []
    while True:
        command_input = input('>').strip()
        if command_input == 'q':
            break
        if command_input:
            handle_command(command_input)


if __name__ == "__main__":
    launch_editor()
