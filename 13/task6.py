# 1. 全局分值映射
letter_dict = {
    ' ': 0, 'EAIONRTLSU': 1, 'DG': 2,
    'BCMP': 3, 'FHVWY': 4, 'K': 5,
    'JX': 8, 'QZ': 10
}
point_dict = {}
for letters, pts in letter_dict.items():
    for ch in letters:
        point_dict[ch] = pts


def word_on_board(word, board):
    # DFS 判断能否拼出 word，并返回路径；支持 '_' 通配符
    if not word or not board or not board[0]:
        return None
    R, C = len(board), len(board[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    def dfs(r, c, i, seen, path):
        if i == len(word):
            return True
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if (0 <= nr < R and 0 <= nc < C
                and (nr,nc) not in seen
                and (board[nr][nc] == word[i] or board[nr][nc] == '_')):
                seen.add((nr,nc)); path.append((nr,nc))
                if dfs(nr, nc, i+1, seen, path):
                    return True
                path.pop(); seen.remove((nr,nc))
        return False

    for i in range(R):
        for j in range(C):
            if board[i][j] == word[0] or board[i][j] == '_':
                seen = {(i,j)}; path = [(i,j)]
                if dfs(i, j, 1, seen, path):
                    return path
    return None


def clean_and_slide_columns(board):
    R, C = len(board), len(board[0])
    newb = [['']*C for _ in range(R)]
    for c in range(C):
        col = [board[r][c] for r in range(R) if board[r][c] != '']
        blanks = [''] * (R - len(col))
        for r in range(R):
            newb[r][c] = blanks[r] if r < len(blanks) else col[r - len(blanks)]
    return newb


def textoggle_move(board, path, spare):
    b = [row[:] for row in board]
    # 删除路径上的字母
    for r, c in path:
        b[r][c] = ''
    # 下落
    b = clean_and_slide_columns(b)
    # 用 spare 填充 '' 或 '_'
    idx = 0; R, C = len(b), len(b[0])
    for c in range(C):
        for r in range(R-1, -1, -1):
            if b[r][c] == '' or b[r][c] == '_':
                if idx < len(spare):
                    b[r][c] = spare[idx]
                else:
                    b[r][c] = '#'
                idx += 1
    return b


def play_best_game(board, spare_letters):
    # 读取词典
    with open('words_alpha.txt') as f:
        words = [w.strip().upper() for w in f if w.strip()]

    total = 0
    idx = 0
    b = [row[:] for row in board]

    while True:
        candidates = []
        for w in words:
            path = word_on_board(w, b)
            if path:
                # 计算本轮基础分：只给非 '_' 格子计分
                base = 0
                for (r, c), ch in zip(path, w):
                    if board[r][c] != '_':  # 注意用原 board 或用 b？应当用拼出时的 b
                        base += point_dict.get(ch, 0)
                # 回合得分 = 基础分 × 单词长度
                round_score = base * len(w)
                candidates.append((round_score, w, path))

        if not candidates:
            break

        # 选最高分，平局选更长单词，再字母序
        candidates.sort(key=lambda x: (-x[0], -len(x[1]), x[1]))
        score, w, path = candidates[0]
        total += score

        # 用 spare_letters 更新棋盘
        need = len(path)
        new = spare_letters[idx: idx+need]
        idx += need
        b = textoggle_move(b, path, new)

    return total


if __name__ == "__main__":
    print(play_best_game(
        [['R','U','N'],['R','E','N'],['X','X','X']],
        ['T','R','T','A','T','N','T']
    ))  # 52
    print(play_best_game(
        [['R','_','N'],['R','E','N'],['X','X','X']],
        ['T','R','T','A','T','N','T']
    ))  # 85
