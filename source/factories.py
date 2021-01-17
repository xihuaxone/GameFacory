from source.areas import BilliardHole
from source.base import Global, DAMap
from configs.config import BackGrounds, CollideReaction, Characters, Areas
from source.background import Background
from source.character import Character, Billiard


class BackGroundFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def produce(bg_type):
        if bg_type == BackGrounds.lustful_demon:
            return Background('../images/lustful_daemon_2.jpg')
        else:
            raise Exception('background %s not implemented.' % bg_type)


class CharacterFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def produce(c_type, scale_rate=1.0):
        if c_type == Characters.awesome_demon:
            return Character('../images/awesome_daemon.png', scale_rate, CollideReaction.rebound)

        elif c_type == Characters.billiard:
            return Billiard('', scale_rate, CollideReaction.rebound)
        else:
            raise Exception('character %s not implemented.' % c_type)


class AreaFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def produce(a_type, radius):
        if a_type == Areas.billiard_holes:
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
                [scr_w / 2, 0], radius, 0, 180,
                [(scr_w - radius) / 2, (scr_w + radius) / 2],
                [0, radius])

            middle_bottom = BilliardHole(
                [scr_w / 2, scr_h], radius, 180, 0,
                [(scr_w - radius) / 2, (scr_w + radius) / 2],
                [scr_h - radius, scr_h])

            return right_top, right_bottom, left_bottom, left_top, middle_top, middle_bottom
