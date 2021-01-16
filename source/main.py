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
        [2400, 0],
        [-2350, 0]
    ]

    positions = [
        [300, 1000],
        [1300, 1000]
    ]

    for _ in range(1):
        c_awesome_dm = CharacterFactory.produce(Characters.awesome_demon, 0.3)
        c_awesome_dm.update_speed([random.randint(-2000, 2000), random.randint(-2000, 2000)])
        # c_awesome_dm.update_speed(speeds[_])
        # c_awesome_dm.update_center(*positions[0])
        ts = time.time()
        while pygame.sprite.spritecollide(c_awesome_dm, sprite_group, False):
            if time.time() - ts > 5 * 1000:
                raise Exception('too many characters')
            c_awesome_dm.rect.left, c_awesome_dm.rect.top = \
                random.randint(0, scr_w - c_awesome_dm.rect.w), \
                random.randint(0, scr_h - c_awesome_dm.rect.h)

        sprite_group.add(c_awesome_dm)

    while True:  # 死循环确保窗口一直显示
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
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

        pygame.display.flip()  # 更新全部显示

        Clock.tick(FPS)

    pygame.quit()  # 退出pygame


if __name__ == '__main__':
    run()

