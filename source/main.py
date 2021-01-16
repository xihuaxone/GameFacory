import random
import time
import pygame
import sys
from configs.config import *
from source.base import Clock, Global, CMap
from source.factories import BackGroundFactory, CharacterFactory

pygame.init()

RUNNING = True


def run():
    global RUNNING
    sprite_group = pygame.sprite.Group()
    background = BackGroundFactory.produce(BackGrounds.lustful_demon)
    scr_w, scr_h = Global.screen_size

    speeds = [
        [300, 0],
        [290, 0]
    ]

    positions = [
        [100, 1500],
        [270, 1500]
    ]

    for _ in range(5):
        c_awesome_dm = CharacterFactory.produce(Characters.awesome_demon, 0.3)
        c_awesome_dm.update_speed([random.randint(-2000, 2000), random.randint(-2000, 2000)])
        # c_awesome_dm.update_speed(speeds[_])
        # c_awesome_dm.update_center(*positions[_])
        ts = time.time()
        while pygame.sprite.spritecollide(c_awesome_dm, sprite_group, False):
            if time.time() - ts > 5 * 1000:
                raise Exception('too many characters')
            c_awesome_dm.rect.left, c_awesome_dm.rect.top = \
                random.randint(0, scr_w - c_awesome_dm.rect.w), \
                random.randint(0, scr_h - c_awesome_dm.rect.h)

        sprite_group.add(c_awesome_dm)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RUNNING = not RUNNING

        if not RUNNING:
            Clock.tick(FPS)
            continue

        Global.screen.fill((0, 0, 0))

        background.blit()

        for character in CMap.iter_characters():
            character.do_move()

        for character in CMap.iter_characters():
            character.collide_react()
            character.fix_position()
            character.blit()

        pygame.display.flip()

        Clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    run()

