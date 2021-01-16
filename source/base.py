import random

import pygame

from configs.config import *


class GlobalObj(object):
    __gravity = GRAVITY
    __k_gravity = GRAVITY_COEFFICIENT
    __screen = pygame.display.set_mode(INIT_SCREEN_SIZE)
    __screen_width, __screen_height = __screen.get_size()

    @property
    def screen(self):
        return self.__screen

    @property
    def screen_size(self):
        return [self.__screen_width, self.__screen_height]

    @property
    def screen_w(self):
        return self.__screen_width

    @property
    def screen_h(self):
        return self.__screen_height

    @property
    def gravity(self):
        return self.__gravity * GRAVITY_COEFFICIENT


Global = GlobalObj()


class PicBase(object):
    def __init__(self):
        self._surface_blit_on = Global.screen

    def _pic_load(self, path):
        return pygame.image.load(path)

    @property
    def surface(self):
        return getattr(self, '_surface', None)

    @property
    def rect(self):
        # 获取矩形区域
        if not getattr(self, '_rect'):
            if getattr(self, '_surface'):
                setattr(self, '_rect', self.surface.get_rect())
        return getattr(self, '_rect', None)

    @rect.setter
    def rect(self, rect):
        setattr(self, '_rect', rect)

    @property
    def center(self):
        return self.rect.center

    def update_center(self, x: int, y: int):
        self.rect.center = [x, y]

    def update_position(self, left=None, right=None, top=None, bottom=None):
        if left is not None:
            self.rect.left = left
        if right is not None:
            self.rect.right = right
        if top is not None:
            self.rect.top = top
        if bottom is not None:
            self.rect.bottom = bottom

    def fix_position(self):
        scr_w, scr_h = Global.screen_size
        if self.rect.bottom > scr_h:
            self.update_position(bottom=scr_h)
        elif self.rect.top < 0:
            self.update_position(top=0)

        if self.rect.right > scr_w:
            self.update_position(right=scr_w)
        elif self.rect.left < 0:
            self.update_position(left=0)

    def blit(self):
        self._surface_blit_on.blit(self.surface, self.rect)


class GlobalClock(object):
    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.__fps_store_limit = 500
        self.__fps_store_count = 0
        self.__fps_history = []

    def __flush_fps(self, recent_fps):
        if self.__fps_store_count >= self.__fps_store_limit:
            self.__fps_history.pop(0)
            self.__fps_store_count -= 1

        self.__fps_history.append(recent_fps)
        self.__fps_store_count += 1

    def get_trend_fps(self):
        if self.__fps_store_count > 0:
            trend_fps = sum(self.__fps_history) /\
                        len(self.__fps_history)
        else:
            trend_fps = FPS * 1.0
        return trend_fps

    def get_trend_spf(self):
        return 1 / self.get_trend_fps()

    def __record_fps(self):
        print('latest fps: %.3f, recent fps: %.3f'
              % (self.__clock.get_fps(), self.get_trend_fps()))

    def tick(self, framerate):
        recent_fps = self.__clock.get_fps()
        if recent_fps:
            self.__flush_fps(recent_fps)
        else:
            self.__flush_fps(FPS)

        if FPS_WATCH:
            self.__record_fps()

        return self.__clock.tick(framerate)

    def get_fps(self):
        return self.__clock.get_fps()


class CharacterMap(object):
    __c_map = {}
    _max_count = 99999

    def iter_characters(self):
        for c in self.__c_map.values():
            yield c

    def register(self, character):
        c_id = random.randint(0, self._max_count)
        while c_id in self.__c_map:
            c_id = random.randint(0, self._max_count)
        self.__c_map[c_id] = character
        return c_id

    def drop(self, c_id):
        self.__c_map.pop(c_id)

    def __get_attr(self, c_id, attr):
        c = self.__c_map.get(c_id, None)
        if c:
            return getattr(c, attr)
        else:
            return None

    def exist(self, c_id):
        return c_id in self.__c_map

    def drop_if_exists(self, c_id):
        if self.exist(c_id):
            self.drop(c_id)

    def get_c_speed(self, c_id):
        return self.__get_attr(c_id, 'speed')

    def get_c_center(self, c_id):
        return self.__get_attr(c_id, 'center')

    def get_c_radius(self, c_id):
        return self.__get_attr(c_id, 'radius')


CMap = CharacterMap()

Clock = GlobalClock()
