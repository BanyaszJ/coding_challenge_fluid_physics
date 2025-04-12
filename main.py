from pprint import pp
import pygame
import random
import inputs
import sys

# -------------------------------  WRITE THESE!!!!!!!!!!!!!!!!!!!!!! ---------------------
INPUT_MAP = inputs.height_map_03
EXPECTED_WATER_VAL = inputs.expected_output_3
FALL_INTERVAL = 10  # [ms]
FPS = 60
# ----------------------------------------------------------------------------------------

# --- Colors ---
WHITE = (255, 255, 255)  # free real estate
BLUE = (0, 150, 255)  # falling water blocks
BLACK = (0, 0, 0)  # terrain blocks and text
GRAY = (200, 200, 200)  # grid lines
GREEN = (34, 139, 34)  # for text
RED = (255, 0, 0)  # for text

# --- Init ---
# Init
pygame.init()

screen_width, screen_height = pygame.display.list_modes()[0]  # OS max resolution

COLS = len(INPUT_MAP)
ROWS = max(INPUT_MAP) + 2  # Add vertical buffer
BLOCK_SIZE = min(screen_width // COLS, screen_height // ROWS) - 5

WINDOW_WIDTH = BLOCK_SIZE * COLS
WINDOW_HEIGHT = BLOCK_SIZE * ROWS

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

clock = pygame.time.Clock()
pygame.display.set_caption("Magyar vízügyi igazgatóság vízállás követési alosztálya.mp3.exe")
font = pygame.font.SysFont('Arial', 28)  # You can change font name and size

falling_block = None
last_fall_time = pygame.time.get_ticks()

# --- Init matrix ---
# 0 = empty, 1 = water, 2 = terrain
matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
print("Initial matrix (empty):")
pp(matrix)

# --- Add terrain ---
for x in range(COLS):
    ground_height = INPUT_MAP[x]
    for y in range(ROWS - 1, ROWS - 1 - ground_height, -1):  # fill from bottom up
        matrix[y][x] = 2  # mark as terrain
print("Filling in the terrain...")
pp(matrix)


def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

            if matrix[y][x] == 1:  # water
                pygame.draw.rect(screen, BLUE, rect)
            elif matrix[y][x] == 2:  # ground
                pygame.draw.rect(screen, BLACK, rect)


def spawn_block():
    return [random.randint(1, COLS - 2), 0]


def can_move_down(x, y):
    return y + 1 < ROWS and matrix[y + 1][x] == 0


def draw_falling_block(x, y):
    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, BLUE, rect)


def lock_block(x, y):
    matrix[y][x] = 1


def remove_block(x, y):
    matrix[y][x] = 0


def block_has_legal_rights_to_exist_lol(curr_x, curr_y):
    """Check if there are black blocks (1) present on the left AND right of the water block (2) in the entire row
    """
    print("matrix row: ", matrix[curr_y])
    print("Left side found: ", matrix[curr_y][0:curr_x])
    print(matrix[curr_y][curr_x+1:COLS])
    print("Right side found: ", matrix[curr_y][curr_x+1:COLS])
    left_side = any(cell == 2 for cell in matrix[curr_y][0:curr_x])
    right_side = any(cell == 2 for cell in matrix[curr_y][curr_x+1:COLS])
    if left_side and right_side:
        return True


def main():
    global falling_block, last_fall_time  # I ain't rewriting this, it's saturday, it works, come at me bro, fuck the haters

    running = True
    water_counter = 0
    falling_block = spawn_block()

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()

        if now - last_fall_time > FALL_INTERVAL:
            if falling_block:
                x, y = falling_block
                print("Block coord: ", x, y)
                if can_move_down(x, y):
                    falling_block[1] += 1
                else:
                    lock_block(x, y)
                    print("Falling block locked in; matrix state:")
                    pp(matrix)
                    if block_has_legal_rights_to_exist_lol(x, y):
                        water_counter += 1
                    else:
                        print("Block has no legal rights to exist, removing...")
                        remove_block(x, y)
                        pp(matrix)
                    falling_block = spawn_block()
            last_fall_time = now

        draw_grid()

        if falling_block:
            draw_falling_block(falling_block[0], falling_block[1])

        curr_text_color = GREEN if water_counter == EXPECTED_WATER_VAL else RED
        curr_text = f'Water amount: {water_counter} (expected: {EXPECTED_WATER_VAL})'
        water_level_text = font.render(curr_text, True, curr_text_color)
        text_rect = water_level_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - WINDOW_HEIGHT + 50))
        screen.blit(water_level_text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
