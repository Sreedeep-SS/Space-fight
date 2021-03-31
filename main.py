import pygame
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LESSSGOO ")

BGC = (90, 0, 150)
WHITE = (255, 255 , 255)
BLACK = (0 ,0 ,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
SPEED = 5
BULLET_SPEED = 7
MAX = 3


BORDER = pygame.Rect(445 , 0 , 10 , 500)

BULLET_FIRE_SOUND=pygame.mixer.Sound(#include gun silencer mp3 path
)
BULLET_HIT_SOUND=pygame.mixer.Sound(#include grenade mp3 path
)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACE = pygame.image.load(#include space png file path
)
SPACE = pygame.transform.scale(SPACE, (WIDTH,HEIGHT))
Yellow_boi = pygame.image.load(#include yellow ship png file path
)
Yellow_boi = pygame.transform.scale(Yellow_boi, (55,45))
Yellow_boi = pygame.transform.rotate(Yellow_boi, 90)

Red_boi = pygame.image.load(#include red ship png file path
)
Red_boi = pygame.transform.scale(Red_boi, (55,45))
Red_boi = pygame.transform.rotate(Red_boi, 270)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(Yellow_boi, (yellow.x, yellow.y))
    WIN.blit(Red_boi, (red.x, red.y))



    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)



    pygame.display.update()

def yellow_boi_movement(key, yellow):
    if key[pygame.K_a] and (yellow.x - SPEED > 0):
        yellow.x -= SPEED
    if key[pygame.K_d] and (yellow.x + SPEED  < (BORDER.x - 45)):
        yellow.x += SPEED
    if key[pygame.K_w] and (yellow.y - SPEED > 0):
        yellow.y -= SPEED
    if key[pygame.K_s] and (yellow.y + SPEED + yellow.height < 490):
        yellow.y += SPEED

def red_boi_movement(key, red):
    if key[pygame.K_LEFT] and (red.x - SPEED > (BORDER.x + BORDER.width)):
        red.x -= SPEED
    if key[pygame.K_RIGHT] and (red.x + SPEED < WIDTH - red.width + 10):
        red.x += SPEED
    if key[pygame.K_UP] and (red.y - SPEED > 0):
        red.y -= SPEED
    if key[pygame.K_DOWN] and (red.y + SPEED + red.height < 490):
        red.y += SPEED

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -=BULLET_SPEED

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1 , WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(10000)



def main():

    red = pygame.Rect(700, 215 , 55 , 45)
    yellow = pygame.Rect(145,215 , 55 , 45)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and (len(yellow_bullets)<MAX):
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + (yellow.height//2), 10 , 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()




                if event.key == pygame.K_RCTRL and (len(red_bullets)<MAX):
                    bullet = pygame.Rect(red.x, red.y + (red.height // 2), 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text= ""
        if red_health <=0:
            winner_text = "Yellow Wins!"

        if yellow_health <=0:
            winner_text = "Red Win!"

        if winner_text!= "":
            draw_winner(winner_text)
            break


        handle_bullets(yellow_bullets,red_bullets, yellow, red)


        keys_pressed = pygame.key.get_pressed()
        yellow_boi_movement(keys_pressed, yellow)
        red_boi_movement(keys_pressed, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)



    main()

if __name__ == "__main__":
    main()
