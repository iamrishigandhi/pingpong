import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Create the paddles
player_paddle = pygame.Rect((HEIGHT//10), HEIGHT // 2 - (WIDTH//50), (WIDTH//100), (HEIGHT//15))
opponent_paddle = pygame.Rect(WIDTH - (HEIGHT//10), HEIGHT // 2 - (WIDTH//50), (WIDTH//100), (HEIGHT//15))

# Create the ball
ball_size_percentage = 5  
ball_width = int(HEIGHT * ball_size_percentage / 100)
ball_height = int(HEIGHT * ball_size_percentage / 100)

ball = pygame.Rect(WIDTH // 2 - ball_width // 2, HEIGHT // 2 - ball_height // 2, ball_width, ball_height)
ball_speed_x = ball_speed_y = 6
ball_speed = [ball_speed_x, ball_speed_y]

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Game over variables
game_over = False
game_over_font = pygame.font.Font(None, 50)

# Restart button
restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 45, 120, 60)

# Score increment variables
last_score_time = pygame.time.get_ticks()
score_increment_interval = 100  # 10 milliseconds

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
        player_paddle_speed = 8
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_paddle.top > 0:
            player_paddle.y -= player_paddle_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_paddle.bottom < HEIGHT:
            player_paddle.y += player_paddle_speed

        # Ball collisions with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Update ball position
        ball_next_position = ball.copy()
        ball_next_position.x += ball_speed[0]
        ball_next_position.y += ball_speed[1]

        # Ball collisions with paddles
        if ball_next_position.colliderect(player_paddle):
            ball_speed[0] = -ball_speed[0]
            current_time = pygame.time.get_ticks()
            if current_time - last_score_time >= score_increment_interval:
                score += 1  # Increase the score when the ball hits the player's paddle
                last_score_time = current_time
        elif ball_next_position.colliderect(opponent_paddle):
            ball_speed[0] = -ball_speed[0]

        # Move opponent paddle towards the ball
        target_position = ball.centery
        opponent_paddle_speed = 15
        if opponent_paddle.centery < target_position:
            opponent_paddle.y += min(opponent_paddle_speed, target_position - opponent_paddle.centery)
        elif opponent_paddle.centery > target_position:
            opponent_paddle.y -= min(opponent_paddle_speed, opponent_paddle.centery - target_position)

        # Check if the ball goes beyond the player paddle
        if ball.left <= 0:
            game_over = True

        if ball.right >= WIDTH:
            game_over = True

        # Update ball position
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    if game_over:

        if ball.left<=0:
            # Display "Game Over" text
            game_over_text = game_over_font.render("GAME OVER", True, WHITE)
            screen_rect = screen.get_rect()
            screen.blit(game_over_text, (screen_rect.centerx - game_over_text.get_width() // 2,
                                        screen_rect.centery - 50))
        
        else:
            game_over_text = game_over_font.render("YOU WIN!", True, WHITE)
            screen_rect = screen.get_rect()
            screen.blit(game_over_text, (screen_rect.centerx - game_over_text.get_width() // 2,
                                        screen_rect.centery - 50))

        # Display player's score
        score_text = font.render("SCORE: {}".format(score), True, WHITE)
        screen.blit(score_text, (screen_rect.centerx - score_text.get_width() // 2,
                                 screen_rect.centery))

        # Draw restart button
        pygame.draw.rect(screen, WHITE, restart_button)
        restart_text = font.render("RESTART", True, BLACK)
        screen.blit(restart_text, (screen_rect.centerx - restart_text.get_width() // 2,
                                   screen_rect.centery + 60))

    else:
        # Display the score
        score_text = font.render("SCORE: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(FPS)