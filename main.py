import sys
from settings import Settings
from point import *
from pygame.sprite import Group
from paku import Paku
from enemy import *

def timer_function(enemy):
    enemy.weakness = False
    enemy.image = pygame.image.load("images/enemy.png")
    if enemy.horizontal == False:
        enemy.flip_image(horizontal=True)
    return enemy.weakness

def timer_respawn(enemy, paku):
    enemy.die = False
    if paku.rect.x > 400:
        enemy.rect.x = 30
        enemy.moving = True
        enemy.flip_image(horizontal=True)
    else:
        enemy.rect.x = 770
        enemy.moving = False
    return enemy

def screen_create(paku_settings, screen):
    screen.fill(paku_settings.bg_color)
    pygame.draw.line(screen, (255, 255, 255), (0, 100), (800, 100), 3)
    pygame.draw.line(screen, (255, 255, 255), (0, 200), (800, 200), 3)
    pygame.draw.line(screen, (255, 255, 255), (0, 110), (800, 110), 3)
    pygame.draw.line(screen, (255, 255, 255), (0, 190), (800, 190), 3)


def run_game():
    x = 0
    tickrate = 57
    hight_score = 0
    pygame.init()
    paku_settings = Settings()
    screen = pygame.display.set_mode((paku_settings.screen_width, paku_settings.screen_height))
    pygame.display.set_caption("Paku")
    paku = Paku(screen)
    points = Group()
    pakues = Group()
    pakues.add(paku)
    enemies = Group()
    enemy = Enemy(screen)
    enemies.add(enemy)
    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, 5000)
    clock = pygame.time.Clock()
    while True:
        screen_create(paku_settings, screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and paku.moving and paku_settings.game_status:
                    paku.moving = False
                    paku.flip_image(horizontal=True)
                elif event.key == pygame.K_SPACE and not paku.moving and paku_settings.game_status:
                    paku.moving = True
                    paku.flip_image(horizontal=True)
                elif event.key == pygame.K_ESCAPE and paku_settings.game_status:
                    paku_settings.game_status = 0
                elif event.key == pygame.K_ESCAPE and not paku_settings.game_status:
                    paku_settings.game_status = 1
            if event.type == TIMER_EVENT:
                if enemy.weakness:
                    timer_function(enemy)
                if enemy.die:
                    timer_respawn(enemy, paku)
        points.draw(screen)
        pakues.draw(screen)
        enemies.draw(screen)

        if paku_settings.game_status:
            paku.update(enemy)
            enemy.update()
            collisions_enemy = pygame.sprite.groupcollide(pakues, enemies, False, False)
            collisions = pygame.sprite.groupcollide(pakues, points, False, True)
            if str(collisions_enemy) == '{<Paku Sprite(in 1 groups)>: [<Enemy Sprite(in 1 groups)>]}' and enemy.weakness == False:
                collisions_enemy = pygame.sprite.groupcollide(pakues, enemies, True, True)
                enemy = Enemy(screen)
                enemies.add(enemy)
                paku = Paku(screen)
                pakues.add(paku)
                points.empty()
                x = 0
                if hight_score < paku_settings.point:
                    hight_score = paku_settings.point
                paku_settings.point = 0
                paku_settings.game_status = 0
                tickrate = 60
            if str(collisions_enemy) == '{<Paku Sprite(in 1 groups)>: [<Enemy Sprite(in 1 groups)>]}' and enemy.weakness == True:
                collisions_enemy = pygame.sprite.groupcollide(pakues, enemies, False, True)
                enemy = Enemy(screen)
                enemy.rect.x = 900
                enemies.add(enemy)
                enemy.die = True
                paku_settings.point += 10 * x
                x += 1
                tickrate += 3
            if str(collisions) != '{}':
                paku_settings.point += (1*x)
            if str(collisions) == '{<Paku Sprite(in 1 groups)>: [<Super_point Sprite(in 0 groups)>]}' and enemy.horizontal:
                enemy.weakness = 1
                enemy.image = pygame.image.load("images/w_enemy.png")
                enemy.flip_image(horizontal=True)
            elif str(collisions) == '{<Paku Sprite(in 1 groups)>: [<Super_point Sprite(in 0 groups)>]}' and enemy.horizontal == False:
                enemy.weakness = 1
                enemy.image = pygame.image.load("images/w_enemy.png")
        clock.tick(tickrate)

        if len(points) == 0:
            points_draw(screen, points, paku)
            x += 1
            tickrate += 3
        text = paku_settings.font.render(f' Score: {paku_settings.point}', True, (255, 255, 255))
        screen.blit(text, (10,10))
        text = paku_settings.font.render(f' X: {x}', True, (255, 255, 255))
        screen.blit(text, (10, 46))
        text = paku_settings.font.render(f' High: {hight_score}', True, (255, 255, 255))
        screen.blit(text, (400, 46))

        if paku_settings.game_status == 0:
            text = paku_settings.font.render(f' Press esc to start/continue', True, (255, 255, 255))
            screen.blit(text, (400, 10))
        pygame.display.flip()

run_game()
