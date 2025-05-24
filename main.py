import pygame
import os
import sys
import random

pygame.font.init()
pygame.mixer.init()

WIDTH = 760
HEIGHT = 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tetopong")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # Set by PyInstaller at runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

BULLET_HIT_SOUND = pygame.mixer.Sound(resource_path(os.path.join('Assets', 'Grenade+1.mp3')))
BULLET_FIRE_SOUND = pygame.mixer.Sound(resource_path(os.path.join('Assets', 'luka.mp3')))
BULLET_FIRE_SOUND.set_volume(0.5)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 50

GIRL_WIDTH = 40
GIRL_HEIGHT = 55

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

VOCALOID_WIDTH = 300
VOCALOID_HEIGHT = 200
TAKO_WIDTH = 50
TAKO_HEIGHT = 50

BLUE_GIRL_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'miku.png')))
BLUE_GIRL = pygame.transform.scale(pygame.transform.rotate(
    BLUE_GIRL_IMAGE, 90), (GIRL_WIDTH, GIRL_HEIGHT))
RED_GIRL_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'teto.png')))
RED_GIRL = pygame.transform.scale(pygame.transform.rotate(
    RED_GIRL_IMAGE, 270), (GIRL_WIDTH, GIRL_HEIGHT))

TETO_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'teto.png')))
TETO = pygame.transform.scale(TETO_IMAGE, (VOCALOID_WIDTH, VOCALOID_HEIGHT))
MIKU_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'miku.png')))
MIKU = pygame.transform.scale(MIKU_IMAGE, (VOCALOID_WIDTH, VOCALOID_HEIGHT))
TAKO_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'tako.png')))
TAKO = pygame.transform.scale(TAKO_IMAGE, (TAKO_WIDTH, TAKO_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(resource_path(os.path.join('Assets', 'space.png'))), (WIDTH, HEIGHT))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)



def draw_window(red, blue, teto, miku, red_bullets, blue_bullets, red_health, blue_health):
    WIN.blit(SPACE, (0, 0))

    pygame.draw.rect(WIN, RED, BORDER)

    WIN.blit(TETO, (teto.x, teto.y))
    WIN.blit(MIKU, (miku.x, miku.y))

    red_health_text = HEALTH_FONT.render("energy: " + str(red_health), 0, WHITE)
    blue_health_text = HEALTH_FONT.render("eneryg: " + str(blue_health), 0, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    #draw rectangle for red girl
    pygame.draw.rect(WIN, RED, red)
    WIN.blit(RED_GIRL, (red.x, red.y))
    pygame.draw.rect(WIN, BLUE, blue)
    WIN.blit(BLUE_GIRL, (blue.x, blue.y))

    for bullet in blue_bullets:
        # pygame.draw.rect(WIN, BLUE, bullet)
        WIN.blit(TAKO, (bullet.x, bullet.y))
    for bullet in red_bullets:
        # pygame.draw.rect(WIN, RED, bullet)
        WIN.blit(TAKO, (bullet.x, bullet.y))

    pygame.display.update()

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:  # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0:  # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT:  # DOWN
        blue.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL

def handle_bullets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH: 
            blue_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0: 
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 0, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    newgame = WINNER_FONT.render("new game in ", 0, WHITE)
    WIN.blit(newgame, (WIDTH//2 - newgame.get_width() // 2, HEIGHT // 2 - newgame.get_height() // 2 + 100))
    for i in range(5, 0, -1):
        # Redraw background over the countdown area
        WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
        WIN.blit(newgame, (WIDTH // 2 - newgame.get_width() // 2, HEIGHT // 2 - newgame.get_height() // 2 + 100))

        countdown = WINNER_FONT.render(str(i), 0, WHITE)
        # draw black rectangle over the countdown area
        pygame.draw.rect(WIN, (0, 0, 0), (WIDTH // 2 - countdown.get_width() // 2, HEIGHT // 2 - countdown.get_height() // 2 + 200, countdown.get_width(), countdown.get_height()))
        # WIN.blit(SPACE, (WIDTH // 2 - countdown.get_width() // 2, HEIGHT // 2 - countdown.get_height() // 2 + 200))
        WIN.blit(countdown, (WIDTH // 2 - countdown.get_width() // 2, HEIGHT // 2 - countdown.get_height() // 2 + 200))

        pygame.display.update()
        pygame.time.delay(random.randint(0, 2000))
    # pygame.display.update()
    # pygame.time.delay(1000)

def main():
    red = pygame.Rect(WIDTH - GIRL_WIDTH - 10, HEIGHT // 2 - GIRL_HEIGHT // 2, GIRL_WIDTH, GIRL_HEIGHT)
    blue = pygame.Rect(10, HEIGHT // 2 - GIRL_HEIGHT // 2, GIRL_WIDTH, GIRL_HEIGHT)
    teto = pygame.Rect(WIDTH - VOCALOID_WIDTH - 10 , 10 , VOCALOID_WIDTH, VOCALOID_HEIGHT)
    miku = pygame.Rect(10, 10 , VOCALOID_WIDTH, VOCALOID_HEIGHT)

    red_bullets = []
    blue_bullets = []

    red_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height // 2 - TAKO_HEIGHT // 2, TAKO_WIDTH, TAKO_HEIGHT)
                    blue_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(red.x - TAKO_WIDTH, red.y + red.height // 2 - TAKO_HEIGHT // 2, TAKO_WIDTH, TAKO_HEIGHT)
                    red_bullets.append(bullet)
                
            if event.type == RED_HIT:
                BULLET_HIT_SOUND.play()
                red_health -= 1
                
            if event.type == BLUE_HIT:
                BULLET_HIT_SOUND.play()
                blue_health -= 1

        

        print(red_bullets, blue_bullets)

        #key handling
        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed, blue)
        red_handle_movement(keys_pressed, red)

        handle_bullets(blue_bullets, red_bullets, blue, red)

        draw_window(red, blue, teto, miku, red_bullets, blue_bullets, red_health, blue_health)

        #check for winner
        winner_text = ""
        if red_health <= 0:
            winner_text = "BLUE WINS"
        if blue_health <= 0:
            winner_text = "RED WINS"
        if winner_text != "":
            draw_winner(winner_text)
            break
    if run:
        main()
    else:
        pygame.quit()
    # pygame.quit()

if __name__ == "__main__":
    main()