import math
from copy import deepcopy

import pygame
import pygame.gfxdraw
from configs.config import *
from source.base import PicBase, CMap, DAMap, Global
from source.event_catcher import EventMonitor
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


class Billiard(Character):

    def __init__(self, pic_path, scale_rate: float, border_collied_react, color, *args, **kwargs):
        Character.__init__(self, pic_path, scale_rate, border_collied_react, *args, **kwargs)
        self.radius = math.ceil(Coordinate.cal_distance([0, 0], [self._rect.w, self._rect.h]) / 2)
        self.color = color

    def _pic_load(self, *args):
        return pygame.surface.Surface([1, 1], 0, 8)

    def __map_register(self):
        return CMap.register(self)
    
    def damage_settle(self):
        for dead_area in DAMap.iter_members():
            if dead_area.if_touched(self):
                self.health = 0
                break

    def blit(self):
        pygame.draw.circle(self._surface_blit_on, self.color, self.center, self.radius)
        if TEST_MODE:
            pygame.draw.rect(self._surface_blit_on, Color.black, self.rect, 2)


class TestMe(Character, EventMonitor):

    def __init__(self, *args, **kwargs):
        Character.__init__(self, *args, **kwargs)
        EventMonitor.__init__(self)
        self.mv_speed_x = 3
        self.mv_speed_y = 3
        self.mv_speed_x_h = 5
        self.mv_speed_y_h = 5
        self.SPEED_UP = False
        self.LEFT_MOVING = False
        self.RIGHT_MOVING = False
        self.UP_MOVING = False
        self.DOWN_MOVING = False

    def _get_mv_speed(self):
        if not self.SPEED_UP:
            return [self.mv_speed_x, self.mv_speed_y]
        else:
            return [self.mv_speed_x_h, self.mv_speed_y_h]

    def do_move(self):
        dx, dy = 0, 0
        mv_x, mv_y = self._get_mv_speed()
        if self.LEFT_MOVING:
            dx -= mv_x
        if self.RIGHT_MOVING:
            dx += mv_x
        if self.UP_MOVING:
            dy -= mv_y
        if self.DOWN_MOVING:
            dy += mv_y
        self.fix_center(dx, dy)
        Character.do_move(self)

    def move_left_switch(self, press_state):
        if press_state == PressState.PRESS:
            self.LEFT_MOVING = True
        elif press_state == PressState.RELEASE:
            self.LEFT_MOVING = False

    def move_right_switch(self, press_state):
        if press_state == PressState.PRESS:
            self.RIGHT_MOVING = True
        elif press_state == PressState.RELEASE:
            self.RIGHT_MOVING = False

    def move_up_switch(self, press_state):
        if press_state == PressState.PRESS:
            self.UP_MOVING = True
        elif press_state == PressState.RELEASE:
            self.UP_MOVING = False

    def move_down_switch(self, press_state):
        if press_state == PressState.PRESS:
            self.DOWN_MOVING = True
        elif press_state == PressState.RELEASE:
            self.DOWN_MOVING = False

    def attach_switch(self, press_state):
        pass

    def speed_switch(self, press_state):
        if press_state == PressState.PRESS:
            self.SPEED_UP = True
        elif press_state == PressState.RELEASE:
            self.SPEED_UP = False

    def l_click(self):
        pass

    def mouse_motion(self):
        pass

    def l_click_finish(self):
        pass
