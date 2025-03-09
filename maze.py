import random

def generate_maze(rows, cols):
    # 保证行数和列数为奇数（这样迷宫有单元通道）
    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1

    # 初始化迷宫，全部填充为墙（1）
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    # 递归回溯法：从某个单元格开始，挖通道
    def carve_passages_from(cx, cy):
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < cols and 0 < ny < rows and maze[ny][nx] == 1:
                # 打通当前单元格与邻居之间的墙（中间那格）
                maze[cy + dy // 2][cx + dx // 2] = 0
                maze[ny][nx] = 0
                carve_passages_from(nx, ny)

    # 从随机奇数坐标的内部起点开始挖通道
    start_cell = (random.randrange(1, cols, 2), random.randrange(1, rows, 2))
    maze[start_cell[1]][start_cell[0]] = 0
    carve_passages_from(start_cell[0], start_cell[1])

    # 在左右边界设置入口和出口：分别在左侧和右侧随机奇数行开口
    entrance_row = random.randrange(1, rows, 2)
    exit_row = random.randrange(1, rows, 2)
    maze[entrance_row][0] = 0  # 左侧入口
    maze[exit_row][cols - 1] = 0  # 右侧出口

    start = (0, entrance_row)
    end = (cols - 1, exit_row)
    return maze, start, end

if __name__ == '__main__':
    m, s, e = generate_maze(21, 21)
    # 打印迷宫，墙用#表示，通道用空格表示
    for row in m:
        print(''.join(['#' if cell == 1 else ' ' for cell in row]))
    print("Start:", s, "End:", e)
