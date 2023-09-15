import pygame
import sys
import random

pygame.init()
WIDTH = 900
HEIGHT = 500
fps = 60
black = (0,0,0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0 , 0)
yellow = (225, 215, 0)
green = (102, 205, 0)
orange = (255, 97, 3)
pygame.display.set_caption("FlappySpace")

# music
'''
pygame.mixer.init()
pygame.mixer.music.load()
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
'''

screen = pygame.display.set_mode((WIDTH,HEIGHT))
timer = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf" , 20)

# Variable Library
player_x = 225
player_y = 225
y_change = 0
jump_height = 12
gravity = .9
obstacles =[400, 700, 1000, 1300, 1600]
generate_places = True
y_positions = []
game_over = False
speed = 3
score = 0
high_score = 0
clouds = []

def draw_player(x_pos, y_pos):
    mouth = pygame.draw.circle(screen, gray, (x_pos + 25, y_pos + 15), 12)
    play = pygame.draw.rect(screen, yellow, [x_pos, y_pos, 30, 30], 0, 12)
    eye = pygame.draw.circle(screen, black, (x_pos + 24, y_pos + 12), 6)
    eye2 = pygame.draw.circle(screen, white, (x_pos + 24, y_pos + 11), 2)
    rocket = pygame.draw.rect(screen, white, [x_pos - 20, y_pos, 21 , 28], 2, 2)
    if y_change <0:
        flame1 = pygame.draw.rect(screen, red, [x_pos - 20, y_pos +29, 7, 20], 0, 2)
        flame1_yellow = pygame.draw.rect(screen, yellow, [x_pos - 18, y_pos + 30, 3, 18], 0, 2)
        flame2 = pygame.draw.rect(screen, orange, [x_pos - 10, y_pos + 29, 7, 20], 0, 2)
        flame2_yellow = pygame.draw.rect(screen, yellow, [x_pos - 8, y_pos +30, 3, 18], 0, 2)
    
    
    return play


def draw_obstacles(obst, y_pos, play):
    global game_over
    for i in range(len(obst)):
        y_coord = y_pos[i]
        top_rect = pygame.draw.rect(screen, green, [obst[i], 0, 30, y_coord])
        top2 = pygame.draw.rect(screen, green, [obst[i] -3, y_coord - 20, 36, 20], 0, 5)
        bot_rect = pygame.draw.rect(screen, green, [obst[i], y_coord + 200, 30, HEIGHT - (y_coord + 70)])
        bot2 = pygame.draw.rect(screen, green, [obst[i] -3, y_coord + 200, 36, 20], 0, 5)
        if top_rect.colliderect(player) or bot_rect.colliderect(player):
            game_over = True


def draw_clouds(clouds):
    global total
    for i in range(total -1 ):
        pygame.draw.rect(screen, white, [clouds[i][0], clouds[i][1], 3, 3], 0, 2)
        clouds[i][0] -= 0.5
        if clouds[i][0] < -3:
            clouds[i][0] = WIDTH + 3 
            clouds[i][1] = random.randint(0, HEIGHT)
    return clouds



running = True
while running:
    timer.tick(fps)
    screen.fill(black)

    if generate_places:
        for i in range(len(obstacles)):
            y_positions.append(random.randint(0,300))
        total = 100
        for i in range(total):
            x_pos = random.randint( 0, WIDTH)
            y_pos = random.randint(0, HEIGHT)
            clouds.append([x_pos, y_pos])
        generate_places = False

    clouds = draw_clouds(clouds)
    player = draw_player(player_x, player_y)
    draw_obstacles(obstacles, y_positions, player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                y_change = -jump_height
            if event.key == pygame.K_SPACE and game_over:
                player_y = 225
                player_x = 225
                y_change = 0
                obstacles =[400, 700, 1000, 1300, 1600]
                generate_places = True
                y_positions = []
                score = 0
                game_over = False

    if player_y + y_change < HEIGHT - 30:
        player_y += y_change
        y_change += gravity
    else:
        player_y = HEIGHT - 30

    for i in range(len(obstacles)):
        if not game_over:
            obstacles[i]-= speed
            if score > 20:
                speed = 6
            if obstacles[i] < -30:
                obstacles.remove(obstacles[i])
                y_positions.remove(y_positions[i])
                obstacles.append(random.randint(obstacles[-1] + 280, obstacles[-1] + 320))
                y_positions.append(random.randint(0, 300))
                score += 1

    if score > high_score:
        high_score = score

    if game_over:
        game_over_text = font.render("GAME OVER! Space Bar to Restart!", True, white)
        screen.blit(game_over_text, (300, 200))

    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 450))
    high_score_text = font.render("High Score: " + str(high_score), True, white)
    screen.blit(high_score_text, (10, 480))

    pygame.display.flip()
pygame.quit()
