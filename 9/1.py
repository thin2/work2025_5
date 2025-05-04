import pygame
import random
pygame.init()
pygame.font.init()


font_small = pygame.font.SysFont("Microsoft YaHei", 24)
font_large = pygame.font.SysFont("Microsoft YaHei", 48)

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 颜色定义
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),   # 青色 - I 形
    (0, 0, 255),     # 蓝色 - J 形
    (255, 165, 0),   # 橙色 - L 形
    (255, 255, 0),   # 黄色 - O 形
    (0, 255, 0),     # 绿色 - S 形
    (128, 0, 128),   # 紫色 - T 形
    (255, 0, 0)      # 红色 - Z 形
]

SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1],
         [1],
         [1],
         [1]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ]
}


grid = [[None for _ in range(10)] for _ in range(20)]



# 定义Piece类
class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.rotations = SHAPES[shape]
        self.rotation_index = 0
        self.matrix = self.rotations[self.rotation_index]
        self.x = 10 // 2 - len(self.matrix[0]) // 2
        self.y = 0
        self.color = COLORS[list(SHAPES.keys()).index(shape)]

    def rotate(self):
        # 尝试旋转
        old_rotation = self.rotation_index
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
        self.matrix = self.rotations[self.rotation_index]
        if not valid_space(self):
            self.rotation_index = old_rotation
            self.matrix = self.rotations[self.rotation_index]

    def move(self, dx, dy):
        old_x = self.x
        old_y = self.y
        self.x += dx
        self.y += dy
        if not valid_space(self):
            self.x = old_x
            self.y = old_y
            return False
        return True


def valid_space(piece):
    for i, row in enumerate(piece.matrix):
        for j, cell in enumerate(row):
            if cell:
                x = piece.x + j
                y = piece.y + i
                if x < 0 or x >= 10 or y < 0 or y >= 20:
                    return False
                if grid[y][x]:
                    return False
    return True

def add_piece_to_grid(piece):
    for i, row in enumerate(piece.matrix):
        for j, cell in enumerate(row):
            if cell:
                grid[piece.y + i][piece.x + j] = piece.color


def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell is None for cell in row)]
    cleared_lines = 20 - len(new_grid)
    for _ in range(cleared_lines):
        new_grid.insert(0, [None for _ in range(10)])
    grid = new_grid
    return cleared_lines

# 绘制游戏网格和已经固定的方块
def draw_grid():
    for i in range(20):
        for j in range(10):
            rect = pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if grid[i][j]:
                pygame.draw.rect(screen, grid[i][j], rect)
# 绘制正在下落的方块
def draw_piece(piece):
    for i, row in enumerate(piece.matrix):
        for j, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((piece.x + j) * BLOCK_SIZE, (piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, piece.color, rect)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# 开始界面
def show_start_screen():
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text("俄罗斯方块", font_large, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text("按任意键开始", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# 游戏结束界面
def show_game_over_screen(score):
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text("游戏结束", font_large, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(f"得分: {score}", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("按任意键重新开始", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    global grid
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 500  # 毫秒

    # 初始化网格与得分
    grid = [[None for _ in range(10)] for _ in range(20)]
    score = 0
    current_piece = Piece(random.choice(list(SHAPES.keys())))
    running = True

    while running:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    # 提高下落速度
                    if not current_piece.move(0, 1):
                        pass
                elif event.key == pygame.K_UP:
                    current_piece.rotate()

        # 自动下落逻辑
        if fall_time > fall_speed:
            fall_time = 0
            # 向下移动一步，如果无法移动则固定当前块
            if not current_piece.move(0, 1):
                add_piece_to_grid(current_piece)
                cleared = clear_lines()
                # 根据消除的行数增加得分（例如每行 100 分）
                score += cleared * 10
                current_piece = Piece(random.choice(list(SHAPES.keys())))
                if not valid_space(current_piece):
                    running = False

        screen.fill(BLACK)
        draw_grid()
        draw_piece(current_piece)
        # 在屏幕顶部显示得分
        score_text = font_small.render(f"得分: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.update()

    pygame.time.delay(500)
    show_game_over_screen(score)

if __name__ == "__main__":
    show_start_screen()
    while True:
        main()
