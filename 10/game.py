import pygame
import sys
import random
import json
import os
from datetime import datetime

# 初始化Pygame
pygame.init()

# 音效加载（需要以下音效文件）
SOUND_FILES = {
    "move": "move.wav",
    "merge": "merge.wav",
    "win": "win.wav",
    "gameover": "gameover.wav"
}
sounds = {}
try:
    pygame.mixer.init()
    for key, file in SOUND_FILES.items():
        if os.path.exists(file):
            sounds[key] = pygame.mixer.Sound(file)
except Exception as e:
    print("音效加载失败:", str(e))

# 窗口尺寸和标题
WIDTH = 500
HEIGHT = 600  # 增加高度以适应扩展菜单
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')

# 默认颜色配置
DEFAULT_COLORS = {
    "background": [187, 173, 160],
    "text": [119, 110, 101],
    "tiles": {
        "0": [205, 193, 180],
        "2": [238, 228, 218],
        "4": [237, 224, 200],
        "8": [242, 177, 121],
        "16": [245, 149, 99],
        "32": [246, 124, 95],
        "64": [246, 94, 59],
        "128": [237, 207, 114],
        "256": [237, 204, 97],
        "512": [237, 200, 80],
        "1024": [237, 197, 63],
        "2048": [237, 194, 46]
    }
}

# 加载用户设置
try:
    with open('settings.json', 'r') as f:
        user_colors = json.load(f)
except:
    user_colors = DEFAULT_COLORS.copy()
    with open('settings.json', 'w') as f:
        json.dump(user_colors, f, indent=4)

# 字体设置
FONT = pygame.font.SysFont('Arial', 24, bold=True)
SCORE_FONT = pygame.font.SysFont('Arial', 20)
MENU_FONT = pygame.font.SysFont('Arial', 22, bold=True)
COLOR_FONT = pygame.font.SysFont('Arial', 18)
GAMEOVER_FONT = pygame.font.SysFont('Arial', 40, bold=True)


class SettingsMenu:
    def __init__(self):
        self.active = False
        self.color_presets = [
            ((187, 173, 160), "默认背景"),
            ((255, 255, 255), "纯白背景"),
            ((100, 100, 100), "深灰背景"),
            ((135, 206, 235), "天蓝背景")
        ]
        self.tile_presets = {
            "2": [
                ((238, 228, 218), "浅黄"),
                ((255, 182, 193), "粉红")
            ],
            "4": [
                ((237, 224, 200), "米色"),
                ((173, 216, 230), "浅蓝")
            ],
            "8": [
                ((242, 177, 121), "橙色"),
                ((144, 238, 144), "浅绿")
            ]
        }

    def draw(self, screen):
        if not self.active:
            return

        # 半透明遮罩
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # 菜单主体
        menu_rect = pygame.Rect(50, 50, 400, 500)
        pygame.draw.rect(screen, (240, 240, 240), menu_rect, border_radius=10)

        # 标题
        title = MENU_FONT.render("游戏设置", True, (0, 0, 0))
        screen.blit(title, (menu_rect.x + 150, menu_rect.y + 15))

        # 背景颜色设置
        self.draw_section(screen, "背景颜色", self.color_presets,
                          menu_rect.x + 20, menu_rect.y + 60,
                          user_colors["background"])

        # 数字颜色设置
        y_offset = 200
        for num in ["2", "4", "8"]:
            self.draw_section(screen, f"数字{num}颜色",
                              self.tile_presets[num],
                              menu_rect.x + 20, menu_rect.y + y_offset,
                              user_colors["tiles"][num])
            y_offset += 80

        # 保存按钮
        save_btn = pygame.Rect(menu_rect.x + 150, menu_rect.y + 450, 100, 40)
        pygame.draw.rect(screen, (0, 200, 0), save_btn, border_radius=5)
        text = COLOR_FONT.render("保存", True, (255, 255, 255))
        screen.blit(text, (save_btn.x + 30, save_btn.y + 10))

        # 处理点击事件
        self.handle_clicks(menu_rect)

    def draw_section(self, screen, title, presets, x, y, current_color):
        # 标题
        title_surf = MENU_FONT.render(title, True, (0, 0, 0))
        screen.blit(title_surf, (x, y))

        # 当前颜色预览
        preview_rect = pygame.Rect(x, y + 40, 60, 60)
        pygame.draw.rect(screen, current_color, preview_rect)

        # 预设按钮
        btn_x = x + 80
        for i, (color, name) in enumerate(presets):
            btn_rect = pygame.Rect(btn_x + i * 90, y + 40, 80, 30)
            pygame.draw.rect(screen, color, btn_rect, border_radius=5)
            text = COLOR_FONT.render(name, True, (0, 0, 0))
            screen.blit(text, (btn_rect.x + 5, btn_rect.y + 5))

    def handle_clicks(self, menu_rect):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()

            # 检查背景颜色选择
            for i, (color, _) in enumerate(self.color_presets):
                btn_rect = pygame.Rect(menu_rect.x + 20 + 80 + i * 90,
                                       menu_rect.y + 60 + 40, 80, 30)
                if btn_rect.collidepoint(mouse_pos):
                    user_colors["background"] = list(color)

            # 检查数字颜色选择
            y_offset = 200
            for num in ["2", "4", "8"]:
                for i, (color, _) in enumerate(self.tile_presets[num]):
                    btn_rect = pygame.Rect(menu_rect.x + 20 + 80 + i * 90,
                                           menu_rect.y + y_offset + 40, 80, 30)
                    if btn_rect.collidepoint(mouse_pos):
                        user_colors["tiles"][num] = list(color)
                y_offset += 80

            # 检查保存按钮
            save_btn = pygame.Rect(menu_rect.x + 150, menu_rect.y + 450, 100, 40)
            if save_btn.collidepoint(mouse_pos):
                with open('settings.json', 'w') as f:
                    json.dump(user_colors, f, indent=4)
                self.active = False


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.matrix = add_new_tile(self.matrix)
        self.matrix = add_new_tile(self.matrix)
        self.score = 0
        self.game_over = False
        self.game_win = False
        self.start_time = datetime.now()


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def handle_row(row):
    compressed = [num for num in row if num != 0]
    new_row = []
    score = 0
    i = 0
    while i < len(compressed):
        if i + 1 < len(compressed) and compressed[i] == compressed[i + 1]:
            merged_value = compressed[i] * 2
            new_row.append(merged_value)
            score += merged_value
            i += 2
            if "merge" in sounds:
                sounds["merge"].play()
        else:
            new_row.append(compressed[i])
            i += 1
    new_row += [0] * (4 - len(new_row))
    return new_row[:4], score


def move(matrix, direction):
    original_matrix = [row.copy() for row in matrix]
    new_matrix = []
    total_score = 0

    if direction == 'left':
        for row in matrix:
            new_row, score = handle_row(row)
            new_matrix.append(new_row)
            total_score += score
    elif direction == 'right':
        for row in matrix:
            processed, score = handle_row(row[::-1])
            new_matrix.append(processed[::-1])
            total_score += score
    elif direction == 'up':
        transposed = transpose(matrix)
        temp = []
        for row in transposed:
            processed, score = handle_row(row)
            temp.append(processed)
            total_score += score
        new_matrix = transpose(temp)
    elif direction == 'down':
        transposed = transpose(matrix)
        temp = []
        for row in transposed:
            processed, score = handle_row(row[::-1])
            temp.append(processed[::-1])
            total_score += score
        new_matrix = transpose(temp)

    if new_matrix != original_matrix and "move" in sounds:
        sounds["move"].play()
    return new_matrix, total_score


def add_new_tile(matrix):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if matrix[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        matrix[i][j] = 2 if random.random() < 0.9 else 4
    return matrix


def can_move(matrix):
    for row in matrix:
        if 0 in row: return True
    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1]: return True
    for j in range(4):
        for i in range(3):
            if matrix[i][j] == matrix[i + 1][j]: return True
    return False


def draw_gameover(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 150))
    screen.blit(overlay, (0, 0))

    text = GAMEOVER_FONT.render('Game Over!', True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # 重试按钮
    retry_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 40)
    pygame.draw.rect(screen, (0, 200, 0), retry_rect, border_radius=5)
    text = FONT.render('重试', True, (255, 255, 255))
    screen.blit(text, (retry_rect.x + 50, retry_rect.y + 10))

    return retry_rect


def draw_matrix(matrix, score, best_score):
    screen.fill(tuple(user_colors["background"]))

    # 绘制得分
    score_text = SCORE_FONT.render(f'得分: {score}', True, tuple(user_colors["text"]))
    best_text = SCORE_FONT.render(f'最佳: {best_score}', True, tuple(user_colors["text"]))
    screen.blit(score_text, (20, 20))
    screen.blit(best_text, (WIDTH - 150, 20))

    # 绘制方块
    tile_size = 80
    gap = 10
    top_offset = 120
    for i in range(4):
        for j in range(4):
            x = j * (tile_size + gap) + gap
            y = i * (tile_size + gap) + gap + top_offset
            value = matrix[i][j]
            color = tuple(user_colors["tiles"].get(str(value), DEFAULT_COLORS["tiles"]["0"]))
            pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
            if value != 0:
                text = FONT.render(str(value), True, tuple(user_colors["text"]))
                text_rect = text.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
                screen.blit(text, text_rect)

    pygame.display.update()


def save_game_data(score, duration):
    try:
        if not os.path.exists('game_records.txt'):
            with open('game_records.txt', 'w') as f:
                f.write("时间, 得分, 时长(s)\n")

        with open('game_records.txt', 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp}, {score}, {duration}\n")
    except Exception as e:
        print("保存失败:", e)


def main():
    # 加载最佳得分
    try:
        with open('best_score.txt', 'r') as f:
            best_score = int(f.read())
    except:
        best_score = 0

    game = GameState()
    settings_menu = SettingsMenu()
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)
        retry_rect = None

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                duration = (datetime.now() - game.start_time).seconds
                save_game_data(game.score, duration)
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over:
                    x, y = event.pos
                    if retry_rect and retry_rect.collidepoint(x, y):
                        game = GameState()
                        if "gameover" in sounds:
                            sounds["gameover"].play()

                elif settings_menu.active:
                    pass  # 设置菜单点击在SettingsMenu类处理

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_menu.active = not settings_menu.active

                elif not game.game_over and not settings_menu.active:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        direction_map = {
                            pygame.K_LEFT: 'left',
                            pygame.K_RIGHT: 'right',
                            pygame.K_UP: 'up',
                            pygame.K_DOWN: 'down'
                        }
                        direction = direction_map[event.key]
                        game.matrix, score_inc = move(game.matrix, direction)
                        game.score += score_inc

                        if game.matrix != game.matrix:
                            game.matrix = add_new_tile(game.matrix)

                            # 检查胜利条件
                            if any(2048 in row for row in game.matrix):
                                game.game_win = True
                                if "win" in sounds:
                                    sounds["win"].play()

                            # 检查游戏结束
                            if not can_move(game.matrix):
                                game.game_over = True
                                duration = (datetime.now() - game.start_time).seconds
                                save_game_data(game.score, duration)
                                if "gameover" in sounds:
                                    sounds["gameover"].play()
                                if game.score > best_score:
                                    best_score = game.score
                                    with open('best_score.txt', 'w') as f:
                                        f.write(str(best_score))

        # 绘制逻辑
        draw_matrix(game.matrix, game.score, best_score)
        if settings_menu.active:
            settings_menu.draw(screen)
        elif game.game_over:
            retry_rect = draw_gameover(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()