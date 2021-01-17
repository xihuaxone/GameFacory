import random
import time
import pygame
import sys

from configs.config import *
from source.base import Clock, Global, CMap, DAMap
from source.factories import BackGroundFactory, CharacterFactory, AreaFactory
from source.utils import Coordinate

pygame.init()

RUNNING = True

MouseMotion = [None, None, None]


def gen_holes(ball_radius):
    AreaFactory.produce(Areas.billiard_holes, ball_radius)


def gen_balls():
    scr_w, scr_h = Global.screen_size

    speeds = [
        [300, 0],
        [290, 0]
    ]

    positions = [
        [100, 1500],
        [270, 1500]
    ]

    sprite_group = pygame.sprite.Group()

    for _ in range(0):
        c_awesome_dm = CharacterFactory.produce(Characters.billiard, 50)
        c_awesome_dm.update_speed([random.randint(-2000, 2000), random.randint(-2000, 2000)])
        c_awesome_dm.update_speed(speeds[_])
        c_awesome_dm.update_center(*positions[_])
        ts = time.time()
        while pygame.sprite.spritecollide(c_awesome_dm, sprite_group, False):
            if time.time() - ts > 5 * 1000:
                raise Exception('too many characters')
            c_awesome_dm.rect.left, c_awesome_dm.rect.top = \
                random.randint(0, scr_w - c_awesome_dm.rect.w), \
                random.randint(0, scr_h - c_awesome_dm.rect.h)

        sprite_group.add(c_awesome_dm)


def mouse_motion_react():
    if MouseMotion[2] is not None:
        nc_pos = MouseMotion[0]
        if not isinstance(nc_pos, tuple):
            raise Exception('mouse motion event catch err. %s'
                            % str(MouseMotion))
        nc_speed = Coordinate.subtract(MouseMotion[2], MouseMotion[0])
        nc_speed = Coordinate.multiply(nc_speed, 20)
        nc = CharacterFactory.produce(Characters.billiard, 50)
        nc.update_center(*nc_pos)
        nc.update_speed(nc_speed)
        MouseMotion[0] = MouseMotion[1] = MouseMotion[2] = None


def run():
    global RUNNING
    background = BackGroundFactory.produce(BackGrounds.lustful_demon)

    gen_balls()

    gen_holes(70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RUNNING = not RUNNING
            elif event.type == pygame.MOUSEBUTTONDOWN:
                MouseMotion[0] = event.pos
            elif event.type == pygame.MOUSEMOTION:
                MouseMotion[1] = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                MouseMotion[2] = event.pos

        mouse_motion_react()

        if not RUNNING:
            Clock.tick(FPS)
            continue

        Global.screen.fill((0, 0, 0))

        background.blit()

        for h in DAMap.iter_members():
            h.blit()

        for character in CMap.iter_members():
            character.do_move()

        for character in CMap.iter_members():
            character.collide_react()
            character.fix_position()
            character.damage_settle()
            if character.health == 0:
                character.destroy()
            character.blit()

        CMap.clear_dead()

        pygame.display.flip()

        Clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    run()

