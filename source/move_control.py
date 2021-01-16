from copy import copy
from typing import List

from configs.config import *
from source.background import Background
from source.base import Global, CollideReaction, Clock, CMap
from source.utils import Coordinate, Formulas


class BorderCollideReact(object):

    @staticmethod
    def collide_detect(left, right, top, bottom, speed):
        x_collide = False
        y_collide = False
        scr_w, scr_h = Global.screen_size
        if (left <= 0 and speed[0] <= 0) or (right >= scr_w and speed[0] >= 0):
            x_collide = True

        if (top <= 0 and speed[1] <= 0) or (bottom >= scr_h and speed[1] >= 0):
            y_collide = True

        return x_collide, y_collide

    @classmethod
    def rebound(cls, move_obj):
        rect = getattr(move_obj, '_rect')
        speed = move_obj.speed

        x_collide, y_collide = cls.collide_detect(
            rect.left, rect.right, rect.top, rect.bottom, speed)
        if x_collide:
            move_obj.reverse_x()
        if y_collide:
            if move_obj.rect.top <= 0 and move_obj.speed[1] <= 0:
                move_obj.reverse_y()
            else:
                move_obj.gravity_speed_fix()
                move_obj.friction_speed_fix()

        return x_collide, y_collide

    @classmethod
    def motionless(cls, move_obj):
        rect = getattr(move_obj, '_pic_obj').rect
        speed = getattr(move_obj, '_speed')

        x_collide, y_collide = cls.collide_detect(
            rect.left, rect.right, rect.top, rect.bottom, speed)
        if x_collide or y_collide:
            speed[0], speed[1] = 0, 0

    @classmethod
    def destroy(cls, move_obj):
        rect = getattr(move_obj, '_pic_obj').rect
        speed = getattr(move_obj, '_speed')

        x_collide, y_collide = cls.collide_detect(
            rect.left, rect.right, rect.top, rect.bottom, speed)
        if x_collide or y_collide:
            move_obj.destroy()


class MoveObj(object):
    def __init__(self):
        self._speed = [0, 0]
        self.mv_stock_x = 0
        self.mv_stock_y = 0
        self.speed_stock_x = 0
        self.speed_stock_y = 0
        self.border_collied_react = CollideReaction.ignore

    @property
    def speed(self):
        return self._speed

    def update_speed(self, speed: List[float or int]):
        self.update_speed_x(speed[0])
        self.update_speed_y(speed[1])

    def update_speed_x(self, x: float or int):
        if isinstance(x, int):
            self._speed[0] = x
            return
        keep, stock = Coordinate.data_stock_calculate(x)
        self._speed[0] = keep
        self.speed_stock_x += stock

    def update_speed_y(self, y: float or int):
        if isinstance(y, int):
            self._speed[1] = y
            return
        keep, stock = Coordinate.data_stock_calculate(y)
        self._speed[1] = keep
        self.speed_stock_y += stock

    def fix_speed(self, speed_delta):
        speed_delta = Coordinate.sum(speed_delta, [self.speed_stock_x, self.speed_stock_y])
        speed_delta[0], self.speed_stock_x = Coordinate.data_stock_calculate(speed_delta[0])
        speed_delta[1], self.speed_stock_y = Coordinate.data_stock_calculate(speed_delta[1])

        fixed_speed = Coordinate.sum(self._speed, speed_delta)
        self.update_speed(fixed_speed)

    def reverse_x(self):
        self._speed[0] = - self._speed[0]

    def reverse_y(self):
        self._speed[1] = - self._speed[1]

    def rebound(self, by_speed):
        if (self._speed[0] > 0 > by_speed[0]) or (self._speed[0] < 0 < by_speed[0]):
            self.reverse_x()

        if (self._speed[1] > 0 > by_speed[1]) or (self._speed[1] < 0 < by_speed[1]):
            self.reverse_y()

    def feedback(self, by_speed, by_center):
        def cal_new_speed(p_center_me, speed_vec_me, p_center_other):
            p_speed_me = Coordinate.sum(p_center_me, speed_vec_me)
            p_foot = Coordinate.get_foot_point(p_speed_me, [p_center_me, p_center_other])
            tan_speed = Coordinate.subtract(p_speed_me, p_foot)
            normal_speed = Coordinate.subtract(p_foot, p_center_me)
            return tan_speed, normal_speed

        speed_me = copy(self._speed)
        p_me = getattr(self, 'center')
        speed_other = by_speed
        p_other = by_center

        remain_speed, _ = cal_new_speed(p_me, speed_me, p_other)
        _, gain_speed = cal_new_speed(p_other, speed_other, p_me)
        new_speed = Coordinate.sum(remain_speed, gain_speed)
        self.update_speed(new_speed)

    def _border_collide_check(self):
        if self.border_collied_react == CollideReaction.ignore:
            return False, False
        elif self.border_collied_react == CollideReaction.rebound:
            return BorderCollideReact.rebound(self)
        elif self.border_collied_react == CollideReaction.motionless:
            return BorderCollideReact.motionless(self)
        elif self.border_collied_react == CollideReaction.destroy:
            return BorderCollideReact.destroy(self)

    def _calculate_trends_step(self):
        spf = Clock.get_trend_spf()
        trends_step = Coordinate.multiply(self._speed, spf)

        trends_step = Coordinate.sum(trends_step, [self.mv_stock_x, self.mv_stock_y])
        trends_step[0], self.mv_stock_x = Coordinate.data_stock_calculate(trends_step[0])
        trends_step[1], self.mv_stock_y = Coordinate.data_stock_calculate(trends_step[1])

        trends_step = Coordinate.multiply(trends_step, C_SPEED)

        return trends_step


class Gravity(object):

    @staticmethod
    def speed_fix_vertex():
        t = 1 / FPS
        delta_v = Global.gravity * t
        delta_y = delta_v * FRAME_METRE_RATIO
        return 0, delta_y


class GravityObj(MoveObj):
    def __init__(self):
        MoveObj.__init__(self)
        self.k_restitution = GRAVITY_RESTITUTION_COEFFICIENT
        self.mass = 50000

    def gravity_speed_fix(self):
        v_y = Formulas.speed_after_collide(
            self.mass, Background.mass,
            self.speed[1] / FRAME_METRE_RATIO, 0,
            self.k_restitution)
        delta_speed_y = v_y * FRAME_METRE_RATIO
        self.update_speed_y(delta_speed_y)


class FrictionObj(GravityObj):
    def __init__(self):
        GravityObj.__init__(self)
        self.k_friction = DEFAULT_FRICTION_COEFFICIENT

    def friction_speed_fix(self):
        a_f = Formulas.friction_acceleration_cal(self.k_friction, Global.gravity)
        t = Clock.get_trend_spf()
        available_t = t if self.speed[1] == 0 else t / 3
        dv_x = a_f * available_t
        dx = dv_x * FRAME_METRE_RATIO
        if abs(dx) > abs(self.speed[0]):
            dx = - self.speed[0]
        else:
            dx = - dx if self.speed[0] > 0 else 0 if self.speed[0] == 0 else dx
        self.fix_speed([dx, 0])


class Collide(object):
    @staticmethod
    def cal_circle_pierce_fix_vertex(center_1: CoordinateType, center_2: CoordinateType, r1, r2):
        # 两个圆相交时，圆心连线为d，d上被两个圆共享的线段部分为c，k为c占d长度的百分比;
        fix_vertex = Coordinate.subtract(center_1, center_2)
        d = Coordinate.cal_distance(center_2, center_1)
        if d == 0:
            return [max(r1, r2), 0]

        k = (r1 + r2 - d) / d
        fix_vertex = Coordinate.multiply(fix_vertex, k)
        return fix_vertex
