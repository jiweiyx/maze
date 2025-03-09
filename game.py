import pygame
import maze
import astar
import dijkstra
import pygame.freetype
import time

# 设置屏幕大小、迷宫可视区大小与方格大小
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 850    # 增加高度，给按钮留出更多空间
MAZE_DISPLAY_SIZE = 750  # 迷宫显示区域为 750×750
CELL_SIZE = 20

# 根据迷宫显示区域与单元格大小来计算行列数
ROWS = MAZE_DISPLAY_SIZE // CELL_SIZE
COLS = MAZE_DISPLAY_SIZE // CELL_SIZE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()

        # 生成迷宫
        self.maze, self.start, self.end = maze.generate_maze(ROWS, COLS)
        self.maze[self.start[1]][self.start[0]] = 0
        self.maze[self.end[1]][self.end[0]] = 0

        # 按钮矩形区域
        self.regen_button_rect = pygame.Rect(10, 755, 150, 30)     # Generate Maze
        self.clear_button_rect = pygame.Rect(170, 755, 150, 30)    # Clear Path
        self.a_star_button_rect = pygame.Rect(330, 755, 120, 30)   # A* Stepwise
        self.dijkstra_button_rect = pygame.Rect(460, 755, 120, 30) # Dijkstra

        # 字体设置
        self.font = pygame.freetype.SysFont("Arial", 18)
        self.large_font = pygame.freetype.SysFont("Arial", 18)

        self.path = []          # 当前路径
        self.path_color = (0, 255, 0)  # 默认路径颜色（绿色）
        self.message = ""       # 底部消息
        self.path_length = 0    # 路径长度
        self.running = True

        # 用于逐步搜索的状态
        self.searching = False
        self.search_generator = None
        self.current_node = None
        self.open_nodes = []
        self.closed_nodes = set()
        self.last_step_time = 0
        self.step_interval = 0.1  # 每步间隔0.1秒
        self.current_algorithm = None  # 新增：记录当前算法

        self.run()

    def draw_maze(self):
        """绘制迷宫"""
        for y in range(ROWS):
            for x in range(COLS):
                color = (255, 255, 255) if self.maze[y][x] == 0 else (0, 0, 0)
                rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw_search_state(self):
        """绘制搜索过程中的节点"""
        # 绘制open list中的节点（浅绿色）
        for item in self.open_nodes:
            if len(item) == 3:  # A*格式: (f_score, g_score, (x, y))
                _, _, (x, y) = item
            elif len(item) == 2:  # Dijkstra格式: (g_score, (x, y))
                _, (x, y) = item
            else:
                continue
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (144, 238, 144), rect)

        # 绘制closed set中的节点（灰色）
        for (x, y) in self.closed_nodes:
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (169, 169, 169), rect)

        # 绘制当前节点（黄色）
        if self.current_node:
            x, y = self.current_node
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 0), rect)

    def draw_path(self):
        """绘制最终路径"""
        for (px, py) in self.path:
            rect = (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, self.path_color, rect)

    def draw_start_end(self):
        """绘制起点(蓝)和终点(红)"""
        sx, sy = self.start
        ex, ey = self.end
        rect_start = (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, (0, 0, 255), rect_start)
        rect_end = (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, (255, 0, 0), rect_end)

    def draw_buttons(self):
        """绘制按钮"""
        pygame.draw.rect(self.screen, (0, 0, 255), self.regen_button_rect)
        self.font.render_to(self.screen, (15, 760), "Generate Maze", (255, 255, 255))
        pygame.draw.rect(self.screen, (255, 165, 0), self.clear_button_rect)
        self.font.render_to(self.screen, (175, 760), "Clear Path", (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 255, 0), self.a_star_button_rect)
        self.font.render_to(self.screen, (335, 760), "A* Stepwise", (255, 255, 255))
        pygame.draw.rect(self.screen, (255, 0, 0), self.dijkstra_button_rect)
        self.font.render_to(self.screen, (465, 760), "Dijkstra", (255, 255, 255))

    def draw_message(self):
        """显示消息和路径长度"""
        text = self.message
        if self.path_length > 0:
            text += f"   Path Length: {self.path_length}"
        self.large_font.render_to(self.screen, (15, 800), text, (0, 0, 0))

    def update_search(self):
        """更新逐步搜索状态"""
        if not self.searching or self.search_generator is None:
            return

        current_time = time.time()
        if current_time - self.last_step_time < self.step_interval:
            return

        try:
            state, *data = next(self.search_generator)
            self.last_step_time = current_time

            if state == "searching":
                self.current_node, self.open_nodes, _, self.closed_nodes = data
                self.message = "Searching..."
            elif state == "done":
                self.path = data[0]
                self.searching = False
                self.search_generator = None
                if self.path:
                    self.message = "Path Found!"
                    self.path_length = len(self.path)
                    # 路径颜色已在handle_events中设置，这里无需再次设置
                else:
                    self.message = "No Path Found!"
                    self.path_length = 0
        except StopIteration:
            self.searching = False
            self.search_generator = None

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.regen_button_rect.collidepoint(event.pos):
                    self.maze, self.start, self.end = maze.generate_maze(ROWS, COLS)
                    self.maze[self.start[1]][self.start[0]] = 0
                    self.maze[self.end[1]][self.end[0]] = 0
                    self.path = []
                    self.path_length = 0
                    self.searching = False
                    self.search_generator = None
                    self.current_algorithm = None
                    self.message = "Maze Generated!"
                elif self.clear_button_rect.collidepoint(event.pos):
                    self.path = []
                    self.path_length = 0
                    self.searching = False
                    self.search_generator = None
                    self.current_node = None
                    self.open_nodes = []
                    self.closed_nodes = set()
                    self.current_algorithm = None
                    self.message = "Path Cleared!"
                elif self.a_star_button_rect.collidepoint(event.pos):
                    if not self.searching:
                        self.path = []
                        self.path_length = 0
                        self.search_generator = astar.astar_stepwise(self.maze, self.start, self.end)
                        self.searching = True
                        self.current_node = None
                        self.open_nodes = []
                        self.closed_nodes = set()
                        self.current_algorithm = "astar"
                        self.path_color = (0, 255, 0)  # A*路径为绿色
                        self.message = "Starting A* Search..."
                elif self.dijkstra_button_rect.collidepoint(event.pos):
                    if not self.searching:
                        self.path = []
                        self.path_length = 0
                        self.search_generator = dijkstra.dijkstra_stepwise(self.maze, self.start, self.end)
                        self.searching = True
                        self.current_node = None
                        self.open_nodes = []
                        self.closed_nodes = set()
                        self.current_algorithm = "dijkstra"
                        self.path_color = (255, 0, 0)  # Dijkstra路径为红色
                        self.message = "Starting Dijkstra Search..."

    def run(self):
        """主循环"""
        while self.running:
            self.screen.fill((255, 255, 255))

            self.draw_maze()
            if self.searching:
                self.update_search()
                self.draw_search_state()
            self.draw_path()
            self.draw_buttons()
            self.draw_message()
            self.draw_start_end()

            self.handle_events()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    Game()