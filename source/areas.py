import pygame
import pygame.gfxdraw
from source.base import Global, DAMap
from configs.config import CoordinateType, Color


class AreaBase(object):
    def __init__(self):
        self._surface_blit_on = Global.screen

    def __map_register(self):
        pass


class DeadArea(AreaBase):
    def __init__(self):
        AreaBase.__init__(self)
        self.a_id = self.__map_register()

    def if_touched(self, character):
        raise NotImplementedError

    def __map_register(self):
        return DAMap.register(self)


class BilliardHole(DeadArea):
    def __init__(self, center: CoordinateType, radius, start_angle: int, stop_angle: int, touch_range_x, touch_range_y):
        DeadArea.__init__(self)
        self.angle = [start_angle, stop_angle]
        self.radius = radius
        self._center = center
        self.touch_range_x = touch_range_x
        self.touch_range_y = touch_range_y

    def if_touched(self, character):
        x_touched = self.touch_range_x[1] >= character.center[0] >= self.touch_range_x[0]
        y_touched = self.touch_range_y[1] >= character.center[1] >= self.touch_range_y[0]
        if x_touched and y_touched:
            return True
        else:
            return False

    def blit(self):
        x, y = self._center
        pygame.gfxdraw.pie(self._surface_blit_on, int(x), int(y), int(self.radius),
                           self.angle[0], self.angle[1], Color.black)
        pygame.gfxdraw.filled_circle(self._surface_blit_on, int(x), int(y), int(self.radius), Color.black)
