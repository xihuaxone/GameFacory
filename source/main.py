import random
import time
import pygame
import sys
from configs.config import *
from source.base import Clock, Global, CMap, DAMap
from source.factories.area_factory import AreaFct
from source.factories.background_factory import BGFct
from source.factories.character_factory import CFct
from source.utils import Coordinate

pygame.init()

RUNNING = True

MouseMotion = [None, None, None]


def gen_holes(ball_radius):
    AreaFct.produce(Areas.billiard_holes, ball_radius)


def gen_balls():
    scr_w, scr_h = Global.screen_size

    speeds = [
        [0, 0]
    ]

    positions = [(548, 466), (483, 503), (483, 424), (417, 462),
                 (419, 393), (418, 534), (354, 489), (358, 559),
                 (357, 340), (297, 368), (288, 517), (286, 582),
                 (295, 289), (353, 413), (282, 440)]

    sprite_group = pygame.sprite.Group()

    for _ in range(len(positions)):
        c_awesome_dm = CFct.produce(Characters.billiard, 40)
        # c_awesome_dm.update_speed([random.randint(-2000, 2000), random.randint(-2000, 2000)])
        # c_awesome_dm.update_speed(speeds[_])
        c_awesome_dm.update_center(*positions[_])
        ts = time.time()
        while pygame.sprite.spritecollide(c_awesome_dm, sprite_group, False):
            if time.time() - ts > 5 * 1000:
                raise Exception('too many characters')
            c_awesome_dm.rect.left, c_awesome_dm.rect.top = \
                random.randint(0, scr_w - c_awesome_dm.rect.w), \
                random.randint(0, scr_h - c_awesome_dm.rect.h)

        sprite_group.add(c_awesome_dm)


hunter = None


def mouse_motion_react():
    global hunter
    pd, pm, pu = MouseMotion
    if pu is not None:
        nc_pos = pd
        if not isinstance(nc_pos, tuple):
            raise Exception('mouse motion event catch err. %s'
                            % str(MouseMotion))

        nc_speed = Coordinate.subtract(pu, pd)
        nc_speed = Coordinate.multiply(nc_speed, 20)
        if not hunter or not CMap.get_character(hunter):
            nc = CFct.produce(Characters.billiard, 40, Color.black)
            nc.update_center(*nc_pos)
            hunter = nc.c_id

        CMap.get_character(hunter).update_speed(nc_speed)

        MouseMotion[0] = MouseMotion[1] = MouseMotion[2] = None


def run():
    global RUNNING
    background = BGFct.produce(BackGrounds.lustful_demon)

    gen_balls()

    gen_holes(50)
    test_me = CFct.produce(Characters.test_me, 0.2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = not RUNNING
                    break

            if RUNNING:
                test_me.event_monitor(event)

        # mouse_motion_react()

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

