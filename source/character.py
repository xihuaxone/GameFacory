from copy import deepcopy
import pygame
import pygame.gfxdraw
from configs.config import *
from source.base import PicBase, CMap, Global
from source.move_control import FrictionObj, Collide, Gravity
from source.utils import Coordinate


class Character(PicBase, FrictionObj, pygame.sprite.Sprite):
    def __init__(self, pic_path, scale_rate: float, border_collied_react, *args, **kwargs):
        PicBase.__init__(self)
        FrictionObj.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.border_collied_react = border_collied_react
        self._surface = self.scale(self._pic_load(pic_path), scale_rate)
        self._rect = self._surface.get_rect()
        self.mv_fix_x = 0
        self.mv_fix_y = 0
        self.health = 100
        self.defence = 0
        self.damage = 100
        self.radius = (self._surface.get_width() + self._surface.get_height()) / 4
        self.c_id = self.__map_register()

    def __map_register(self):
        return CMap.register(self)

    def destroy(self):
        CMap.delay_delete(self.c_id)

    @staticmethod
    def scale(surface_pic, scale_rate: float):
        origin_width, origin_height = surface_pic.get_size()

        return pygame.transform.scale(
            surface_pic,
            (int(origin_width * scale_rate),
             int(origin_height * scale_rate)))

    def piercing_fix(self, by_center, by_radius):
        fix_vertex = Collide.cal_circle_pierce_fix_vertex(
            self.center, by_center, self.radius, by_radius)
        fixed_center = Coordinate.sum(self.center, fix_vertex)
        self.update_center(fixed_center[0], fixed_center[1])

    def take_collide(self, by_center, by_speed, by_radius, by_mass, *args, **kwargs):
        self.piercing_fix(by_center, by_radius)
        self.feedback(by_speed, by_center, by_mass)

    def take_damage(self, damage):
        self.health = self.health + min(self.defence - damage, 0)

    def collide_react(self):
        for other in CMap.iter_members():
            if other.c_id == self.c_id:
                continue
            distance = Coordinate.cal_distance(self.center, other.center)
            if distance <= (self.radius + other.radius):
                other_speed = deepcopy(other.speed)
                other_center = deepcopy(CMap.get_c_center(other.c_id))
                other.take_collide(self.center, self.speed, self.radius, self.mass)
                self.take_collide(other_center, other_speed, other.radius, other.mass)

    def do_move(self):
        self._border_collide_check()

        if FALL_GRAVITY:
            g_vertex = Gravity.speed_fix_vertex()
            self.fix_speed(g_vertex)

        self.global_friction_speed_fix(self.speed, Global.gravity, K_GLOBAL_FRICTION)

        trends_step = self._calculate_trends_step()

        self.rect = self.rect.move(trends_step)

    def damage_settle(self):
        pass

    def blit(self):
        if TEST_MODE:
            x, y = self.center
            r = int(self.radius)
            pygame.gfxdraw.aacircle(self._surface_blit_on, x, y, r, (130, 130, 130))
            pygame.draw.rect(self._surface_blit_on, (130, 130, 130), self.rect, 2)
        PicBase.blit(self)
