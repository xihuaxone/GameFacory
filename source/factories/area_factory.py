from configs.config import Areas
from source.areas import BilliardHole
from source.base import Global
from source.factories.base import FactoryBase


class AreaFactory(FactoryBase):
    def __init__(self):
        FactoryBase.__init__(self)

    @staticmethod
    def produce(a_type, radius):
        if a_type == Areas.billiard_holes:
            middle_holes_radius = radius / 1.3
            scr_w, scr_h = Global.screen_size
            right_top = BilliardHole(
                [scr_w, 0], radius, 90, 180,
                [scr_w - radius, scr_w], [0, radius])

            right_bottom = BilliardHole(
                [scr_w, scr_h], radius, 180, 270,
                [scr_w - radius, scr_w], [scr_h - radius, scr_h])

            left_bottom = BilliardHole(
                [0, scr_h], radius, 270, 0,
                [0, radius], [scr_h - radius, scr_h])

            left_top = BilliardHole(
                [0, 0], radius, 0, 90, [0, radius], [0, radius])

            middle_top = BilliardHole(
                [scr_w / 2, 0], middle_holes_radius, 0, 180,
                [(scr_w - radius) / 2, (scr_w + radius) / 2],
                [0, radius])

            middle_bottom = BilliardHole(
                [scr_w / 2, scr_h], middle_holes_radius, 180, 0,
                [(scr_w - radius) / 2, (scr_w + radius) / 2],
                [scr_h - radius, scr_h])

            return right_top, right_bottom, left_bottom, left_top, middle_top, middle_bottom


AreaFct = AreaFactory()
