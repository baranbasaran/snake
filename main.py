import pygame
import sys
import random

pygame.init()

width, height = 1024, 600
rows, cols = 15, 35
square_size = 25  
dt = 0

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Initial snake position aligned with grid
start_x = 75
start_y = 100
player_pos = pygame.Vector2(start_x + 5 * square_size, start_y + 5 * square_size)
snake_body = [player_pos.copy()]

# Initial food position
food_pos = pygame.Vector2(
    random.randint(0, cols - 1) * square_size + start_x,
    random.randint(0, rows - 1) * square_size + start_y
)

# Snake direction (initially moving right)
direction = pygame.Vector2(1, 0)

# Colors
background_color = (30, 30, 30)  # Dark gray background
grid_color1 = (50, 50, 50)  # Slightly lighter gray for grid pattern
grid_color2 = (40, 40, 40)  # Slightly darker gray for grid pattern
snake_color = (0, 255, 0)  # Bright green snake
food_color = (255, 0, 0)  # Bright red food
border_color = (255, 215, 0)  # Gold color for the border

def draw_board(window, rows, cols, square_size, start_x, start_y):
    for row in range(rows):
        for col in range(cols):
            color = grid_color1 if (row + col) % 2 == 0 else grid_color2
            pygame.draw.rect(window, color, (start_x + col * square_size, start_y + row * square_size, square_size, square_size))

    # Draw the border
    pygame.draw.rect(window, border_color, (start_x, start_y, cols * square_size, rows * square_size), 2)

def place_new_food():
    return pygame.Vector2(
        random.randint(0, cols - 1) * square_size + start_x,
        random.randint(0, rows - 1) * square_size + start_y
    )

def is_move_valid(player_pos, snake_body):
    # Collision check
    for segment in snake_body[1:]:
        if player_pos.distance_to(segment) < square_size:
            return False
    return True

# Main loop
running = True
while running:
    direction_changed = False  # Reset the flag at the start of each frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not direction_changed:
            if event.key == pygame.K_w and direction != pygame.Vector2(0, 1):
                new_direction = pygame.Vector2(0, -1)
            elif event.key == pygame.K_s and direction != pygame.Vector2(0, -1):
                new_direction = pygame.Vector2(0, 1)
            elif event.key == pygame.K_a and direction != pygame.Vector2(1, 0):
                new_direction = pygame.Vector2(-1, 0)
            elif event.key == pygame.K_d and direction != pygame.Vector2(-1, 0):
                new_direction = pygame.Vector2(1, 0)
            else:
                new_direction = direction

            # Flag control to not do more than 1 move at a frame
            if new_direction != -direction:
                direction = new_direction
                direction_changed = True  # Set the flag after a valid direction change

    window.fill(background_color)  

    draw_board(window, rows, cols, square_size, start_x, start_y)

    # Move the snake
    player_pos += direction * square_size

    # Wrap-around logic
    if player_pos.x < start_x:
        player_pos.x = start_x + (cols - 1) * square_size
    elif player_pos.x >= start_x + cols * square_size:
        player_pos.x = start_x
    if player_pos.y < start_y:
        player_pos.y = start_y + (rows - 1) * square_size
    elif player_pos.y >= start_y + rows * square_size:
        player_pos.y = start_y

    # Detect collision with food
    if player_pos.distance_to(food_pos) < square_size:
        food_pos = place_new_food()
        snake_body.append(snake_body[-1].copy())

    # Check for self-collision
    if not is_move_valid(player_pos, snake_body):
        running = False
        print("Game Over")

    # Update snake body
    if len(snake_body) > 1:
        for i in range(len(snake_body) - 1, 0, -1):
            snake_body[i] = snake_body[i - 1].copy()
    snake_body[0] = player_pos.copy()

    # Draw the food
    pygame.draw.rect(window, food_color, (food_pos.x, food_pos.y, square_size, square_size))

    # Draw the snake
    for segment in snake_body:
        pygame.draw.rect(window, snake_color, (segment.x, segment.y, square_size, square_size))
    
    dt = clock.tick(10) / 1000  # Set to 15 FPS for square-by-square movement
    pygame.display.flip()

pygame.quit()
sys.exit()
