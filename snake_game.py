from random import randint
import pygame
import sys
from search_algos import bfs, dfs, astar

if len(sys.argv) != 2:
    print('input dfs, bfs, or astar as an arg')
    sys.exit(1)

if sys.argv[1] == 'bfs':
    SEARCH_ALGO = bfs
elif sys.argv[1] == 'dfs':
    SEARCH_ALGO = dfs
elif sys.argv[1] == 'astar':
    SEARCH_ALGO = astar
else:
    print('input dfs, bfs, or astar as an arg')
    sys.exit(1)

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)

num_cols = num_rows = 30
total_width = total_height = 660

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
curr = snake[-1]

food = grid[randint(0, num_rows-1)][randint(0, num_cols-1)]

# directions: 0=up, 1=right, 2=down, 3=left

done = False
dirs = SEARCH_ALGO(grid, snake, food) #[0]

while dirs == []:
    dirs = SEARCH_ALGO(grid, snake, food)

while not done:
    clock.tick(20)
    screen.fill(BLACK)
    curr_dir = dirs.pop()

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

    if new_x >= num_rows or new_x < 0 or new_y >= num_cols or new_y < 0:
        break

    newCell = grid[new_x][new_y]
    if newCell in snake:
        break

    snake.append(newCell)

    curr = snake[-1]
    if curr.x == food.x and curr.y == food.y:
        food = grid[randint(0, num_rows-1)][randint(0, num_cols-1)]
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
    else:
        snake.pop(0)


    food.show_color(GREEN)
    for i in snake:
        i.show_color(WHITE)
    snake[-1].show_color(YELLOW)

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
