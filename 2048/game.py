# -*- coding: utf-8 -*-
import pygame
import sys
import random
import json

# 初始化Pygame
pygame.init()
pygame.mixer.init()  # 初始化音频系统
try:
    move_sound = pygame.mixer.Sound("点击按钮-叮咚-游戏提示音_系统提示音(Button54)_爱给网_aigei_com.mp3")
except Exception as e:
    print("音效加载失败:", str(e))
    move_sound = None
# 窗口尺寸和标题
WIDTH = 400
HEIGHT = 500
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


class SettingsMenu:
    def __init__(self):
        self.active = False
        self.color_presets = [
            ((187, 173, 160), "默认"),
            ((255, 255, 255), "白色"),
            ((100, 100, 100), "深灰"),
            ((135, 206, 235), "天蓝")
        ]

    def draw(self, screen):
        if not self.active:
            return

        # 半透明遮罩
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # 菜单主体
        menu_rect = pygame.Rect(50, 50, 300, 300)
        pygame.draw.rect(screen, (240, 240, 240), menu_rect, border_radius=10)

        # 标题
        title = MENU_FONT.render("颜色设置", True, (0, 0, 0))
        screen.blit(title, (menu_rect.x + 90, menu_rect.y + 15))

        # 背景颜色选择
        self.draw_section(screen, "背景颜色", menu_rect.x + 20, menu_rect.y + 60)

        # 保存按钮
        save_btn = pygame.Rect(menu_rect.x + 100, menu_rect.y + 250, 100, 40)
        pygame.draw.rect(screen, (0, 200, 0), save_btn, border_radius=5)
        text = MENU_FONT.render("保存", True, (255, 255, 255))
        screen.blit(text, (save_btn.x + 30, save_btn.y + 5))

    def draw_section(self, screen, title, x, y):
        # 标题
        title_surf = MENU_FONT.render(title, True, (0, 0, 0))
        screen.blit(title_surf, (x, y))

        # 颜色按钮
        btn_x = x
        btn_y = y + 40
        for i, (color, name) in enumerate(self.color_presets):
            btn_rect = pygame.Rect(btn_x + (i % 2) * 140, btn_y + (i // 2) * 60, 120, 50)
            pygame.draw.rect(screen, color, btn_rect, border_radius=5)
            text = MENU_FONT.render(name, True, (0, 0, 0))
            screen.blit(text, (btn_rect.x + 10, btn_rect.y + 15))

            # 处理点击事件
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if btn_rect.collidepoint(mouse_pos):
                    user_colors["background"] = list(color)

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(user_colors, f, indent=4)

# 加载用户设置
try:
    with open('settings.json', 'r') as f:
        user_colors = json.load(f)
except:
    user_colors = DEFAULT_COLORS.copy()
    with open('settings.json', 'w') as f:
        json.dump(user_colors, f, indent=4)

FONT = pygame.font.SysFont('SimHei', 30, bold=True)  # 黑体
SCORE_FONT = pygame.font.SysFont('SimHei', 24)  # 黑体
MENU_FONT = pygame.font.SysFont('SimHei', 22, bold=True)
def transpose(matrix):
    """转置矩阵（行列交换）"""
    return [list(row) for row in zip(*matrix)]

def handle_row(row):
    """处理单行，返回新行和合并得分"""
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
        else:
            new_row.append(compressed[i])
            i += 1
    new_row += [0] * (4 - len(new_row))
    return new_row[:4], score

def move(matrix, direction):
    """根据方向移动矩阵，返回新矩阵和得分"""
    new_matrix = []
    total_score = 0
    original_matrix = [row.copy() for row in matrix]
    if direction == 'left':
        for row in matrix:
            new_row, score = handle_row(row)
            new_matrix.append(new_row)
            total_score += score
    elif direction == 'right':
        for row in matrix:
            reversed_row = row[::-1]
            processed, score = handle_row(reversed_row)
            new_row = processed[::-1]
            new_matrix.append(new_row)
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
            reversed_row = row[::-1]
            processed, score = handle_row(reversed_row)
            new_row = processed[::-1]
            temp.append(new_row)
            total_score += score
        new_matrix = transpose(temp)
    else:
        return matrix,
    if new_matrix != original_matrix:
        # 播放音效（如果加载成功）
        if move_sound is not None:
            try:
                move_sound.play()
            except Exception as e:
                print("音效播放失败:", str(e))
    return new_matrix, total_score

def add_new_tile(matrix):
    """在空白位置随机生成2或4"""
    empty_cells = [(i, j) for i in range(4) for j in range(4) if matrix[i][j] == 0]
    if not empty_cells:
        return matrix
    i, j = random.choice(empty_cells)
    matrix[i][j] = 2 if random.random() < 0.9 else 4
    return matrix

def can_move(matrix):
    """检查是否还能移动"""
    # 检查空白格
    for row in matrix:
        if 0 in row:
            return True
    # 检查行相邻
    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1]:
                return True
    # 检查列相邻
    for j in range(4):
        for i in range(3):
            if matrix[i][j] == matrix[i + 1][j]:
                return True
    return False


def draw_matrix(matrix, score, best_score):
    """绘制游戏界面"""
    screen.fill(tuple(user_colors["background"]))
    # 绘制得分
    score_text = SCORE_FONT.render(f'Score: {score}', True, tuple(user_colors["text"]))
    best_text = SCORE_FONT.render(f'Best: {best_score}', True, tuple(user_colors["text"]))
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


def main():
    # 初始化矩阵和分数
    matrix = [[0] * 4 for _ in range(4)]
    matrix = add_new_tile(matrix)
    matrix = add_new_tile(matrix)
    score = 0
    best_score = 0
    running = True
    game_over = False
    settings_menu = SettingsMenu()
    clock = pygame.time.Clock()
    retry_rect = None
    try:
        with open('best_score.txt', 'r') as f:
            best_score = int(f.read())
    except:
        pass

    while running:
        clock.tick(30)
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over and retry_rect:
                    # 处理重试按钮点击
                    x, y = event.pos
                    if  retry_rect.collidepoint(x, y):
                        matrix = [[0] * 4 for _ in range(4)]
                        matrix = add_new_tile(matrix)
                        matrix = add_new_tile(matrix)
                        score = 0
                        game_over = False
                        print("重新开始游戏")

                elif settings_menu.active:
                    # 处理设置菜单点击
                    mouse_pos = pygame.mouse.get_pos()
                    # 保存按钮点击检测
                    save_btn = pygame.Rect(150, 300, 100, 40)
                    if save_btn.collidepoint(mouse_pos):
                        settings_menu.save_settings()
                        settings_menu.active = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC键切换菜单
                    settings_menu.active = not settings_menu.active

                elif not settings_menu.active and not game_over:
                    # 游戏控制处理
                    original_matrix = [row.copy() for row in matrix]
                    direction = None
                    if event.key == pygame.K_LEFT:
                        direction = 'left'
                    elif event.key == pygame.K_RIGHT:
                        direction = 'right'
                    elif event.key == pygame.K_UP:
                        direction = 'up'
                    elif event.key == pygame.K_DOWN:
                        direction = 'down'

                    if direction:
                        new_matrix, score_increment = move(matrix, direction)
                        if new_matrix != original_matrix:
                            matrix = new_matrix
                            score += score_increment
                            if score > best_score:
                                best_score = score
                                with open('best_score.txt', 'w') as f:
                                    f.write(str(best_score))
                            matrix = add_new_tile(matrix)

                            # 检查胜利条件
                            game_win = any(2048 in row for row in matrix)
                            if game_win:
                                print("You Win!")

                            # 检查游戏结束
                            if not can_move(matrix):
                                print("Game Over!")
                                game_over = True
        # 游戏逻辑更新
        if not game_over and not settings_menu.active:
            # 检查游戏是否结束
            if not can_move(matrix):
                game_over = True
                print("游戏结束！")
                # 更新最佳分数
                if score > best_score:
                    best_score = score
                    with open('best_score.txt', 'w') as f:
                        f.write(str(best_score))

        # 绘制逻辑
        if settings_menu.active:
            draw_matrix(matrix, score, best_score)
            settings_menu.draw(screen)
        else:
            draw_matrix(matrix, score, best_score)

        # 游戏结束界面
        if game_over:
            retry_rect = draw_gameover(screen)

        pygame.display.update()

    # 退出前保存最佳分数
    with open('best_score.txt', 'w') as f:
        f.write(str(best_score))
    pygame.quit()



def draw_gameover(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 150))
    screen.blit(overlay, (0, 0))

    text = FONT.render('Game Over!', True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # 重试按钮
    retry_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 40)
    pygame.draw.rect(screen, (0, 200, 0), retry_rect, border_radius=5)
    text = FONT.render('Retry', True, (255, 255, 255))
    screen.blit(text, (retry_rect.x + 45, retry_rect.y + 10))

    return retry_rect

if __name__ == '__main__':
    main()