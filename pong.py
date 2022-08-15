import sys
import pygame
from pygame.math import Vector2
from random import randint, choice

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

width, height = 720, 480

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")


def init_ball():
    global ball_dia, ball, ball_speed_x, ball_speed_y, direction
    ball_dia = 15
    ball = pygame.Rect(width / 2 - ball_dia / 2, height /
                       2 - ball_dia / 2, ball_dia, ball_dia)
    ball_speed_x = 4
    ball_speed_y = choice((-3, 3))
    direction = randint(0, 1)
    if direction == 0:
        ball_speed_x *= -1


def init_paddles():
    global paddle_depth, paddle_length, player_paddle, opp_paddle
    paddle_depth = 5
    paddle_length = 75
    player_paddle = pygame.Rect(5, height / 2 - paddle_length / 2,
                                paddle_depth, paddle_length)
    opp_paddle = pygame.Rect(width - paddle_depth - 5, height /
                             2 - paddle_length / 2, paddle_depth, paddle_length)


light_grey = 211, 211, 211
blue = 0, 0, 30
white = 255, 255, 255

init_ball()
init_paddles()
player_speed = 0
opp_speed = 4
player_score, opp_score = 0, 0
scoreboard_font = pygame.font.SysFont("Calibri", 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 4
            if event.key == pygame.K_DOWN:
                player_speed += 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 4
            if event.key == pygame.K_DOWN:
                player_speed -= 4

    if (player_paddle.top >= 0 and player_speed < 0 or
            player_paddle.bottom <= height and player_speed > 0):
        player_paddle.move_ip(0, player_speed)
    if player_paddle.top < 0:
        player_paddle.move(5, 0)
    if player_paddle.bottom > height:
        player_paddle.move(5, height)

    if opp_paddle.top <= ball.bottom:
        opp_paddle.move_ip(0, opp_speed)
    if opp_paddle.bottom >= ball.top:
        opp_paddle.move_ip(0, -opp_speed)

    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1

    if player_paddle.colliderect(ball) and ball_speed_x < 0:
        ball_speed_x *= -1
    if opp_paddle.colliderect(ball) and ball_speed_x > 0:
        ball_speed_x *= -1

    ball.move_ip(ball_speed_x, ball_speed_y)

    if ball.right <= 0:
        opp_score += 1
        opp_speed -= 1
        pygame.time.wait(3000)
        init_ball()
        init_paddles()
    if ball.left >= width:
        player_score += 1
        opp_speed += 1
        pygame.time.wait(3000)
        init_ball()
        init_paddles()

    scoreboard_surface = scoreboard_font.render(
        f"{player_score} - {opp_score}", False, white)
    scoreboard_rect = scoreboard_surface.get_rect(
        center=(width / 2, height / 6))

    screen.fill(blue)
    screen.blit(scoreboard_surface, scoreboard_rect)
    pygame.draw.line(screen, white, Vector2(
        width / 2, 0), Vector2(width / 2, height))
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.rect(screen, white, player_paddle)
    pygame.draw.rect(screen, white, opp_paddle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
