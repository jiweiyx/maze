import heapq

# 原有的Dijkstra算法（保留以供参考或兼容性）
def dijkstra(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    
    def valid_move(x, y):
        return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

    open_list = []
    heapq.heappush(open_list, (0, start))  # (g, (x, y))
    came_from = {}
    g_score = {start: 0}
    
    while open_list:
        current_g, current = heapq.heappop(open_list)
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if valid_move(neighbor[0], neighbor[1]):
                tentative_g = current_g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heapq.heappush(open_list, (tentative_g, neighbor))
    
    return []

# 逐步执行的Dijkstra算法
def dijkstra_stepwise(maze, start, end):
    """
    一个生成器版本的Dijkstra算法。
    每次扩展一个节点后，yield当前的搜索信息。
    最终找到路径后，yield一个("done", path)并return结束。
    如果没有路径，yield ("done", []) 并return。
    与astar_stepwise保持一致的输出格式。
    """
    rows, cols = len(maze), len(maze[0])
    
    def valid_move(x, y):
        return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

    open_list = []
    heapq.heappush(open_list, (0, start))  # (g, (x, y))
    came_from = {}
    g_score = {start: 0}
    closed_set = set()  # 用于记录已处理的节点，与astar_stepwise保持一致
    
    while open_list:
        current_g, current = heapq.heappop(open_list)
        closed_set.add(current)

        # 每扩展一个节点，yield当前搜索状态
        # 格式与astar_stepwise一致：("searching", current, open_list, came_from, closed_set)
        yield ("searching", current, list(open_list), came_from, closed_set)
        
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
        
        # 检查四个方向
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if valid_move(neighbor[0], neighbor[1]) and neighbor not in closed_set:
                tentative_g = current_g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heapq.heappush(open_list, (tentative_g, neighbor))
    
    # 如果open_list耗尽，仍然找不到终点，则无路径
    yield ("done", [])
    return
