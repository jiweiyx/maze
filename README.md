# Maze Pathfinding Demo

这是一个基于 Pygame 的迷宫路径搜索演示项目，旨在帮助学习算法的人通过可视化方式理解 A* 和 Dijkstra 算法的运作过程。项目通过逐步展示搜索步骤，让用户直观地看到算法如何在迷宫中找到从起点到终点的路径。

## 项目结构

- **game.py**: 主程序，负责运行游戏循环、绘制界面并处理用户交互。
- **maze.py**: 迷宫生成模块，生成随机的迷宫，包括起点和终点。
- **astar.py**: 实现 A* 算法，包括逐步搜索版本 (`astar_stepwise`)。
- **dijkstra.py**: 实现 Dijkstra 算法，包括逐步搜索版本 (`dijkstra_stepwise`)。

## 功能特点

1. **迷宫生成**:
   - 使用 `maze.py` 中的 `generate_maze` 函数生成一个随机的迷宫。
   - 迷宫由 0（可通行）和 1（墙壁）组成，起点和终点强制设置为可通行。

2. **路径搜索算法**:
   - **A* 算法** (`astar_stepwise`):
     - 使用启发式函数（曼哈顿距离）优化搜索。
     - 逐步展示搜索过程，最终路径显示为绿色。
   - **Dijkstra 算法** (`dijkstra_stepwise`):
     - 基于均匀代价的广度优先搜索。
     - 逐步展示搜索过程，最终路径显示为红色。

3. **逐步演示**:
   - 搜索过程每 0.1 秒更新一步。
   - 可视化元素：
     - **浅绿色**：待探索的节点（Open List）。
     - **灰色**：已探索的节点（Closed Set）。
     - **黄色**：当前正在处理的节点。
     - **绿色/红色**：最终路径（A* 为绿色，Dijkstra 为红色）。
     - **蓝色**：起点。
     - **红色**：终点。

4. **用户交互**:
   - **Generate Maze**：重新生成一个随机迷宫。
   - **Clear Path**：清除当前路径和搜索状态。
   - **A* Stepwise**：启动 A* 算法的逐步搜索。
   - **Dijkstra**：启动 Dijkstra 算法的逐步搜索。

## 运行项目

### 依赖
- Python 3.x
- Pygame（安装：`pip install pygame`）

### 运行步骤
1. 确保所有文件（`game.py`, `maze.py`, `astar.py`, `dijkstra.py`）在同一目录下。
2. 在终端运行：
  ```python
  python game.py
  ```

3. 使用鼠标点击界面上的按钮进行操作。

## 学习算法

这个项目非常适合学习路径搜索算法的初学者或教学使用。以下是源码中的关键点，供学习参考：

### 迷宫生成 (`maze.py`)
- 函数 `generate_maze(rows, cols)` 使用递归分割算法生成迷宫。
- 返回 `(maze, start, end)`，其中 `maze` 是一个二维数组，`start` 和 `end` 是坐标元组。

### A* 算法 (`astar.py`)
- **heuristic(a, b)**: 计算曼哈顿距离作为启发式估计。
- **astar_stepwise(maze, start, end)**: 生成器版本的 A* 算法，每次扩展一个节点时 yield 当前状态：
  - Open List 使用优先队列（`heapq`）维护，排序依据 `f_score = g_score + heuristic`。
  - Closed Set 记录已处理的节点，避免重复访问。
  - 通过 `came_from` 重建路径。

### Dijkstra 算法 (`dijkstra.py`)
- **dijkstra_stepwise(maze, start, end)**: 生成器版本的 Dijkstra 算法，每次扩展一个节点时 yield 当前状态：
  - Open List 使用优先队列，排序依据 `g_score`（从起点到当前节点的代价）。
  - 不使用启发式函数，与 A* 的区别在于均匀探索。
  - 同样通过 `came_from` 重建路径。

### 主程序 (`game.py`)
- **Game 类**：
  - 初始化 Pygame，设置窗口和迷宫。
  - `draw_search_state()`: 绘制搜索过程中的节点状态。
  - `update_search()`: 控制逐步搜索，每 0.1 秒更新一步。
  - `handle_events()`: 处理按钮点击，启动算法或重置迷宫。

## 教学建议
1. **理解算法差异**:
   - 比较 A* 和 Dijkstra 在相同迷宫上的搜索过程，观察 A* 如何利用启发式函数更快找到路径。
   - 注意 Open List 和 Closed Set 的变化。

2. **修改代码实验**:
   - 调整 `step_interval`（在 `game.py` 中）改变搜索速度。
   - 修改 `heuristic` 函数（在 `astar.py` 中）尝试其他距离度量（如欧几里得距离）。
   - 在 `draw_search_state` 中更改颜色，便于区分不同状态。

3. **源码阅读**:
   - 从 `astar_stepwise` 和 `dijkstra_stepwise` 的 `yield` 语句入手，理解逐步执行的逻辑。
   - 查看 `game.py` 中的 `update_search`，学习如何与生成器协作。

## 示例截图
（你可以运行程序后截图添加，例如初始迷宫、搜索过程和最终路径的图片）

## 贡献
欢迎提交问题或改进建议！如果想添加新功能（如其他算法或迷宫样式），请 fork 项目并提交 pull request。
