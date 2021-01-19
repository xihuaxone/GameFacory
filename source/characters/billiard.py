import math

import pygame

from configs.config import TEST_MODE, Color
from source.base import CMap, DAMap
from source.character import Character
from source.utils import Coordinate


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
