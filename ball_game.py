import pygame
import sys #module used to be able to exit the program after game is over 

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_COLOR = (255, 0, 0)  # Red
PADDLE_COLOR = (0, 255, 0)  # Green
BG_COLOR = (0, 0, 0)  # Black
SPEED_X, SPEED_Y = 5, 5

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beachball")

# Ball start position
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [SPEED_X, SPEED_Y]

# Paddle start position
paddle_pos = [WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30]

# Counter for successful ball returns
successful_hits = 0
max_hits = 5  # Game ends after 5 successful hits

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position and set paddle position
    mouse_x = pygame.mouse.get_pos()[0]
    paddle_pos[0] = mouse_x - PADDLE_WIDTH // 2

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Check for collision with walls and change direction
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - BALL_SIZE:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]

    # Check for collision with the paddle
    if (paddle_pos[0] < ball_pos[0] < paddle_pos[0] + PADDLE_WIDTH and
            paddle_pos[1] < ball_pos[1] + BALL_SIZE < paddle_pos[1] + PADDLE_HEIGHT):
        ball_speed[1] = -ball_speed[1]
        successful_hits += 1
        if successful_hits == max_hits:
            print("You won!")
            running = False

    # End the game if the ball touches the bottom of the screen
    if ball_pos[1] >= HEIGHT - BALL_SIZE:
        print("The pet won!")
        running = False

    # Update the screen
    screen.fill(BG_COLOR)
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, BALL_SIZE)
    pygame.draw.rect(screen, PADDLE_COLOR, (paddle_pos[0], paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
