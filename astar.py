import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, end):  # 原有的直接计算路径函数
    # 这里是原来的astar实现，我假设你有这个函数
    # 为兼容性保留，但我们主要用astar_stepwise
    pass

def astar_stepwise(maze, start, end):
    """
    一个生成器版本的A*算法。
    每次扩展一个节点后，yield当前的搜索信息。
    最终找到路径后，yield一个("done", path)并return结束。
    如果没有路径，yield ("done", []) 并return。
    """
    rows, cols = len(maze), len(maze[0])
    
    def valid_move(x, y):
        return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

    open_list = []
    heapq.heappush(open_list, (heuristic(start, end), 0, start))  # (f, g, (x, y))
    came_from = {}
    g_score = {start: 0}
    
    closed_set = set()  # 可选：记录已处理的节点
    
    while open_list:
        _, current_g, current = heapq.heappop(open_list)
        closed_set.add(current)

        # 每扩展一个节点，都将当前搜索状态yield出去
        # 以便外部可视化搜索进度
        yield ("searching", current, list(open_list), came_from, closed_set)
        
        # 检查是否到达终点
        if current == end:
            # 重新构建路径
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            yield ("done", path)
            return

        # 扩展邻居
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            if valid_move(nx, ny) and neighbor not in closed_set:
                tentative_g = current_g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score, tentative_g, neighbor))

    # 如果open_list耗尽，仍然找不到终点，则无路径
    yield ("done", [])
    return