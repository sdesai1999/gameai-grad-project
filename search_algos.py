from queue import PriorityQueue
import numpy as np
from itertools import count

num_cols = num_rows = 43

def bfs(grid, snake, food):
    directions = []

    # initialize visited matrix, and set the start to the snake head and goal to the food pellet
    visited = [[False for j in range(num_cols)] for i in range(num_rows)]
    init = grid[snake[-1].x][snake[-1].y]
    goal = grid[food.x][food.y]

    queue = [init]

    # mark start as visited
    visited[init.x][init.y] = True
    curr = None

    while len(queue) > 0:
        curr = queue.pop(0)
        #visited[curr.x][curr.y] = True

        # stop if goal is found
        if curr.x == goal.x and curr.y == goal.y:
            while curr != init:
                direction = (curr.x - curr.previous.x, curr.y - curr.previous.y)  # 0 = up, 1 = right, 2 = down, 3 = left but we flip since we are going backwards
                if direction == (0, -1): # if down, add up
                    direction = 0
                elif direction == (0, 1): #if up, add down
                    direction = 2
                elif direction == (1, 0): #if right, add left
                    direction = 1
                elif direction == (-1, 0): #if left, add right
                    direction = 3
                directions.append(direction)
                curr = curr.previous
            return directions

        # generate the four neighbors
        neighbors = [(curr.x, curr.y-1), (curr.x+1, curr.y), (curr.x, curr.y+1), (curr.x-1, curr.y)] #up right down left

        for n in neighbors:
            new_x, new_y = n

            # if new coords are in bounds, not visited, and not part of the snake, push the coords to the queue
            if new_x >= num_rows or new_x < 0 or new_y >= num_cols or new_y < 0:
                continue

            newCell = grid[new_x][new_y]

            if newCell in snake or visited[new_x][new_y]:
                continue

            if newCell not in queue:
                newCell.previous = curr
                queue.append(newCell)
                visited[new_x][new_y] = True

    return directions

def dfs(grid, snake, food):
    directions = []

    # initialize visited matrix, and set the start to the snake head and goal to the food pellet
    visited = [[False for j in range(num_cols)] for i in range(num_rows)]
    init = grid[snake[-1].x][snake[-1].y]
    goal = grid[food.x][food.y]

    stack = [init]

    # mark start as visited
    visited[init.x][init.y] = True
    curr = None

    while len(stack) > 0:
        curr = stack.pop(-1)
        visited[curr.x][curr.y] = True

        # stop if goal is found
        if curr.x == goal.x and curr.y == goal.y:
            while curr != init:
                direction = (curr.x - curr.previous.x, curr.y - curr.previous.y)  # 0 = up, 1 = right, 2 = down, 3 = left but we flip since we are going backwards
                if direction == (0, -1): # if down, add up
                    direction = 0
                elif direction == (0, 1): #if up, add down
                    direction = 2
                elif direction == (1, 0): #if right, add left
                    direction = 1
                elif direction == (-1, 0): #if left, add right
                    direction = 3
                directions.append(direction)
                curr = curr.previous
            return directions

        # generate the four neighbors
        neighbors = [(curr.x, curr.y-1), (curr.x+1, curr.y), (curr.x, curr.y+1), (curr.x-1, curr.y)] #up right down left

        for n in neighbors:
            new_x, new_y = n

            # if new coords are in bounds, not visited, and not part of the snake, push the coords to the stack
            if new_x >= num_rows or new_x < 0 or new_y >= num_cols or new_y < 0:
                continue

            newCell = grid[new_x][new_y]

            if newCell in snake or visited[new_x][new_y]:
                continue

            if newCell not in stack:
                newCell.previous = curr
                stack.append(newCell)

    return directions

def astar(grid, snake, food):
    directions = []

    # initialize visited matrix, and set the start to the snake head and goal to the food pellet
    visited = [[False for j in range(num_cols)] for i in range(num_rows)]
    init = grid[snake[-1].x][snake[-1].y]
    goal = grid[food.x][food.y]

    pq = PriorityQueue()
    u = count()

    pq.put((0, next(u), init))
    curr = None

    while not pq.empty():
        curr = pq.get()[2]
        if curr.x == goal.x and curr.y == goal.y:
            # we have reached the food
            break

        if visited[curr.x][curr.y]:
            continue

        visited[curr.x][curr.y] = True
        # generate the four neighbors
        neighbors = [(curr.x, curr.y-1), (curr.x+1, curr.y), (curr.x, curr.y+1), (curr.x-1, curr.y)] #up right down left

        for n in neighbors:
            new_x, new_y = n

            # if new coords are in bounds, not visited, and not part of the snake, push the coords to the stack
            if new_x >= num_rows or new_x < 0 or new_y >= num_cols or new_y < 0:
                continue

            newCell = grid[new_x][new_y]
            if newCell in snake or visited[new_x][new_y]:
                continue
            
            newCell.h = np.sqrt((newCell.x - goal.x) ** 2 + (newCell.y - goal.y) ** 2)
            newCell.g = curr.g + 1
            newCell.f = newCell.g + newCell.h
            newCell.previous = curr

            pq.put((newCell.f, next(u), newCell))
        
    while curr != init:
        curr_x = curr.x
        px = curr.previous.x
        curr_y = curr.y
        py = curr.previous.y
        direction = (curr_x - px, curr_y - py)  # 0 = up, 1 = right, 2 = down, 3 = left but we flip since we are going backwards
        if direction == (0, -1): # if down, add up
            direction = 0
        elif direction == (0, 1): #if up, add down
            direction = 2
        elif direction == (1, 0): #if right, add left
            direction = 1
        elif direction == (-1, 0): #if left, add right
            direction = 3
        directions.append(direction)
        curr = curr.previous

    return directions
