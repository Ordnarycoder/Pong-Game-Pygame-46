import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Paddle settings
paddle_width, paddle_height = 10, 100
paddle_speed = 7

# Ball settings
ball_size = 20
ball_speed_x = 5
ball_speed_y = 5

# Bullet settings
bullet_size = 10
bullet_speed = -10  # Negative so it moves left

# Define paddle positions
left_paddle = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Define ball position
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)

# Define bullet position and state (start off-screen)
bullet = pygame.Rect(-100, -100, bullet_size, bullet_size)
bullet_active = False

# Variables for computer invisibility
computer_invisible = False
invisible_start_time = 0  # Timestamp when invisibility starts

# Game clock
clock = pygame.time.Clock()

def move_ball():
    global ball_speed_x, ball_speed_y

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collision with top and bottom
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1

    # Bounce off paddles: only consider left paddle collision if computer is visible.
    if (not computer_invisible and ball.colliderect(left_paddle)) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Reset ball if it goes out of bounds
    if ball.left <= 0 or ball.right >= width:
        ball.center = (width // 2, height // 2)
        ball_speed_x *= -1


def move_bullet():
    global bullet_active, computer_invisible, invisible_start_time
    if bullet_active:
        bullet.x += bullet_speed
        # Deactivate bullet if it goes off-screen
        if bullet.x > width or bullet.x < 0:
            bullet.x = -100
            bullet.y = -100
            bullet_active = False

    # Check collision of bullet with paddles
    # When bullet hits the computer (left) paddle, hide it for 3 seconds.
    if bullet.colliderect(left_paddle):
        bullet.x = -100
        bullet.y = -100
        bullet_active = False
        computer_invisible = True
        invisible_start_time = pygame.time.get_ticks()
        
    # Also, if bullet collides with right paddle, just deactivate it
    if bullet.colliderect(right_paddle):
        bullet.x = -100
        bullet.y = -100
        bullet_active = False

def move_computer():
    # Simple AI: move left paddle towards the ball's y coordinate
    # Even if invisible, we update its position (so it resumes correctly)
    if left_paddle.centery < ball.centery and left_paddle.bottom < height:
        left_paddle.y += paddle_speed
    elif left_paddle.centery > ball.centery and left_paddle.top > 0:
        left_paddle.y -= paddle_speed

def move_paddles(keys):
    global bullet_active
    # Move right paddle (human player)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < height:
        right_paddle.y += paddle_speed

    # Shoot bullet when SPACE is pressed (only if no bullet is active)
    if keys[pygame.K_SPACE] and not bullet_active:
        # Position bullet at the center of the right paddle
        bullet.center = right_paddle.center
        bullet_active = True

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check if computer invisibility period is over (3 seconds)
    if computer_invisible:
        current_time = pygame.time.get_ticks()
        if current_time - invisible_start_time >= 3000:
            computer_invisible = False

    # Get pressed keys and move paddles
    keys = pygame.key.get_pressed()
    move_paddles(keys)
    move_computer()  # control the left paddle with computer
    move_ball()
    move_bullet()

    # Draw everything
    win.fill(BLACK)
    # Draw left paddle only if it's not invisible
    if not computer_invisible:
        pygame.draw.rect(win, WHITE, left_paddle)
    pygame.draw.rect(win, WHITE, right_paddle)
    pygame.draw.ellipse(win, WHITE, ball)
    pygame.draw.rect(win, RED, bullet)
    pygame.draw.aaline(win, WHITE, (width // 2, 0), (width // 2, height))

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # 60 frames per second
