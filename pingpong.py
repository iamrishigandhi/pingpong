import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Create the paddles
player_paddle = pygame.Rect(50, HEIGHT // 2 - 20, 10, 40)
opponent_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 20, 10, 40)

# Create the ball
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_speed = [3, 3]

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Game over variables
game_over = False
game_over_font = pygame.font.Font(None, 50)

# Restart button
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)

# Score increment variables
last_score_time = pygame.time.get_ticks()
score_increment_interval = 100  # 100 milliseconds (0.1 seconds)

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # Restart the game when the mouse is clicked on the restart button
            if restart_button.collidepoint(event.pos):
                game_over = False
                score = 0
                ball.x = WIDTH // 2 - 10
                ball.y = HEIGHT // 2 - 10

    keys = pygame.key.get_pressed()

    if not game_over:
        # Update player paddle position
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_paddle.top > 0:
            player_paddle.y -= 5
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_paddle.bottom < HEIGHT:
            player_paddle.y += 5

        # Update ball position
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collisions with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Ball collisions with paddles
        if ball.colliderect(player_paddle):
            ball_speed[0] = -ball_speed[0]
            current_time = pygame.time.get_ticks()
            if current_time - last_score_time >= score_increment_interval:
                score += 1  # Increase the score when the ball hits the player's paddle
                last_score_time = current_time
        elif ball.colliderect(opponent_paddle):
            ball_speed[0] = -ball_speed[0]

        # Move opponent paddle towards the ball
        if opponent_paddle.centery < ball.centery:
            opponent_paddle.y += 3
        elif opponent_paddle.centery > ball.centery:
            opponent_paddle.y -= 3

        # Check if the ball goes beyond the player paddle
        if ball.left <= 0:
            game_over = True

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    if game_over:
        # Display "Game Over" text
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        # Display player's score
        score_text = font.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 40, HEIGHT // 2))

        # Draw restart button
        pygame.draw.rect(screen, WHITE, restart_button)
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - 35, HEIGHT // 2 + 60))

    else:
        # Display the score
        score_text = font.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(FPS)