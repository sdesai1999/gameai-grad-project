from random import randint
import pygame
import sys
from search_algos import bfs, dfs, astar, astar_manhattan

if len(sys.argv) != 2:
    print('input dfs, bfs, or astar as an arg')
    sys.exit(1)

SECOND_ALGO = None

FRUIT_COUNTER = 0
if sys.argv[1] == 'bfs':
    SEARCH_ALGO = bfs
elif sys.argv[1] == 'dfs':
    SEARCH_ALGO = dfs
elif sys.argv[1] == 'astar':
    SEARCH_ALGO = astar
elif sys.argv[1] == 'astar_manhattan':
    SEARCH_ALGO = astar_manhattan
elif sys.argv[1] == 'both':
    SEARCH_ALGO = dfs
    SECOND_ALGO = astar_manhattan
else:
    print('input dfs, bfs, or astar as an arg')
    sys.exit(1)

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255) #snake body
BLUE = (0, 0, 255) #snake head 2
GREEN = (0, 255, 0)
RED = (255, 0, 0) #snake body 2
YELLOW = (255,255,0) #snakehead



num_cols = num_rows = 43
total_width = total_height = 946

cell_w = total_width // num_cols
cell_h = total_height // num_rows

screen = pygame.display.set_mode([total_width, total_height])
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # a star stuff
        self.g = 0
        self.h = 0
        self.f = 0
        self.previous = None

    def show_color(self, color):
        pygame.draw.rect(screen, color, [self.x*cell_h+1, self.y*cell_w+1, cell_h-2, cell_w-2])






grid = [[Cell(i, j) for j in range(num_cols)] for i in range(num_rows)]
snake = [grid[round(num_rows/2)][round(num_cols/2)]]
snake2 = snake

if SECOND_ALGO:
    snake = [grid[randint(0, num_rows-1)][randint(0, num_cols-1)]]
    snake2 = [grid[randint(0, num_rows-1)][randint(0, num_cols-1)]]
    while snake2 == snake:
        snake2 = [grid[randint(0, num_rows-1)][randint(0, num_cols-1)]]

curr = snake[-1]
curr2 = snake2[-1]

food = grid[randint(0, num_rows-1)][randint(0, num_cols-1)]

# directions: 0=up, 1=right, 2=down, 3=left

done = False
dirs = SEARCH_ALGO(grid, snake, food) #[0]
dirs2 = dirs[:]
if SECOND_ALGO:
    dirs2 = SECOND_ALGO(grid, snake2, food)

while dirs == [] or dirs2 == []:
    dirs = SEARCH_ALGO(grid, snake, food)

    dirs2 = SECOND_ALGO(grid, snake2, food)

while not done:
    clock.tick(7000)
    screen.fill(BLACK)
    curr_dir = dirs.pop()
    if SECOND_ALGO:
        curr_dir2 = dirs2.pop()

    new_x = curr.x
    new_y = curr.y

    if curr_dir == 0:
        new_y -= 1
    elif curr_dir == 1:
        new_x += 1
    elif curr_dir == 2:
        new_y += 1
    elif curr_dir == 3:
        new_x -= 1

    # Collission checks
    if new_x >= num_rows or new_x < 0 or new_y >= num_cols or new_y < 0:
        break

    newCell = grid[new_x][new_y]
    if newCell in snake:
        break
    snake.append(newCell)

    if SECOND_ALGO:
        new_x2 = curr2.x
        new_y2 = curr2.y

        if curr_dir2 == 0:
            new_y2 -= 1
        elif curr_dir2 == 1:
            new_x2 += 1
        elif curr_dir2 == 2:
            new_y2 += 1
        elif curr_dir2 == 3:
            new_x2 -= 1
        if new_x2 >= num_rows or new_x2 < 0 or new_y2 >= num_cols or new_y2 < 0:
            break
        newCell2 = grid[new_x2][new_y2]
        if newCell2 in snake2 or newCell2 in snake or newCell in snake2:
            break
        snake2.append(newCell2)



    curr = snake[-1]
    if SECOND_ALGO:
        curr2 = snake2[-1]

    if curr.x == food.x and curr.y == food.y:
        food = grid[randint(0, num_rows-1)][randint(0, num_cols-1)]
        FRUIT_COUNTER += 1
        print(FRUIT_COUNTER)
        while food in snake:
            food = grid[randint(0, num_rows-1)][randint(0, num_cols-1)]
        # print(food.x, food.y)
        for i, x in enumerate(grid):
            for j, y in enumerate(grid[i]):
                grid[i][j].g = 0
                grid[i][j].h = 0
                grid[i][j].f = 0
                grid[i][j].previous = None

        dirs = SEARCH_ALGO(grid, snake, food)
        if SECOND_ALGO:
            dirs2 = SECOND_ALGO(grid, snake2, food)
            snake2.pop(0)

    elif SECOND_ALGO and curr2.x == food.x and curr2.y == food.y:
        food = grid[randint(0, num_rows-1)][randint(0, num_cols-1)]
        while food in snake2:
            food = grid[randint(0, num_rows-1)][randint(0, num_cols-1)]
        # print(food.x, food.y)
        for i, x in enumerate(grid):
            for j, y in enumerate(grid[i]):
                grid[i][j].g = 0
                grid[i][j].h = 0
                grid[i][j].f = 0
                grid[i][j].previous = None

        dirs = SEARCH_ALGO(grid, snake, food)
        dirs2 = SECOND_ALGO(grid, snake2, food)
        snake.pop(0)
    else:
        snake.pop(0)
        if SECOND_ALGO:
            snake2.pop(0)

    food.show_color(GREEN)
    for i in snake:
        i.show_color(WHITE)

    if SECOND_ALGO:
        for i in snake2:
            i.show_color(BLUE)

    snake[-1].show_color(YELLOW)
    if SECOND_ALGO:
        snake2[-1].show_color(RED)

    pygame.display.update()

    # dir_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP and curr_dir != 2:
        #         dirs.append(0)
        #         dir_changed = True
        #     if event.key == pygame.K_DOWN and curr_dir != 0:
        #         dirs.append(2)
        #         dir_changed = True
        #     if event.key == pygame.K_LEFT and curr_dir != 1:
        #         dirs.append(3)
        #         dir_changed = True
        #     if event.key == pygame.K_RIGHT and curr_dir != 3:
        #         dirs.append(1)
        #         dir_changed = True

    # if not dir_changed:
    #     dirs.append(curr_dir)
