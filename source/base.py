import random
import pygame
from configs.config import *
from source.utils import Formulas


class GlobalObj(object):
    __gravity = GRAVITY
    __k_gravity = GRAVITY_COEFFICIENT
    __screen = pygame.display.set_mode(INIT_SCREEN_SIZE)
    __screen_width, __screen_height = __screen.get_size()
    __K_global_friction = K_GLOBAL_FRICTION

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

    @property
    def global_acceleration(self):
        return Formulas.friction_acceleration_cal(self.__K_global_friction, self.gravity)


Global = GlobalObj()


class PicBase(object):
    def __init__(self, pic_path, scale_rate=1.0, fit_screen=False, middle=False):
        self._surface_blit_on = Global.screen
        self._surface = self.scale(self._pic_load(pic_path), scale_rate, fit_screen)
        self._rect = self._surface.get_rect()
        if middle:
            self._rect.centerx = Global.screen_w / 2
            self._rect.centery = Global.screen_h / 2

    def _pic_load(self, path):
        return pygame.image.load(path)

    @staticmethod
    def scale(surface_pic, scale_rate: float, fit_screen):
        origin_width, origin_height = surface_pic.get_size()
        if fit_screen:
            if origin_width / Global.screen_w > origin_height / Global.screen_h:
                scale_rate = Global.screen_w / origin_width
            else:
                scale_rate = Global.screen_h / origin_height
        return pygame.transform.scale(
            surface_pic,
            (int(origin_width * scale_rate),
             int(origin_height * scale_rate)))

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

    def fix_center(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

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


class MapBase(object):
    def __init__(self):
        self._map = {}
        self._max_count = 99999
        self.__wait_delete = []

    def iter_members(self):
        for c in self._map.values():
            yield c

    def register(self, member):
        c_id = random.randint(0, self._max_count)
        while c_id in self._map:
            c_id = random.randint(0, self._max_count)
        self._map[c_id] = member
        return c_id

    def drop(self, m_id):
        self._map.pop(m_id)

    def _get_attr(self, m_id, attr):
        m = self._map.get(m_id, None)
        if m:
            return getattr(m, attr)
        else:
            return None

    def exist(self, m_id):
        return m_id in self._map

    def drop_if_exists(self, m_id):
        if self.exist(m_id):
            self.drop(m_id)

    def delay_delete(self, m_id):
        self.__wait_delete.append(m_id)

    def clear_dead(self):
        for m_id in self.__wait_delete:
            self.drop_if_exists(m_id)


class CharacterMap(MapBase):
    def get_c_speed(self, c_id):
        return self._get_attr(c_id, 'speed')

    def get_c_center(self, c_id):
        return self._get_attr(c_id, 'center')

    def get_c_radius(self, c_id):
        return self._get_attr(c_id, 'radius')

    def get_character(self, c_id):
        return self._map.get(c_id)


class DeadAreaMap(MapBase):
    pass


class WindowUIMap(MapBase):
    pass


class MenuUIMap(MapBase):
    pass


CMap = CharacterMap()
DAMap = DeadAreaMap()
UIMap = WindowUIMap()
MenuMap = MenuUIMap()

Clock = GlobalClock()
