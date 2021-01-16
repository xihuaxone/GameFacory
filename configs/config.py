from typing import List

CoordinateType = List[float or int]
CoordinateList = List[CoordinateType]


class Products(object):
    background = 'background'
    character = 'character'


class BackGrounds(object):
    lustful_demon = 'lustful_demon'


class Characters(object):
    awesome_demon = 'awesome_demon'


class CollideReaction(object):
    destroy = 'destroy'
    rebound = 'rebound'
    sticking = 'sticking'
    motionless = 'motionless'
    ignore = 'ignore'


FPS = 300
INIT_SCREEN_SIZE = (1920, 1080)

SPEED_COEFFICIENT = 1
FRAME_METRE_RATIO = 100

GRAVITY = 9.8
GRAVITY_COEFFICIENT = 1
GRAVITY_RESTITUTION_COEFFICIENT = 1.1

DEFAULT_FRICTION_COEFFICIENT = 1.5

TEST_MODE = True
FPS_WATCH = False


class Defense(object):
    INVINCIBLE = -99
    ONE_HIT_KILL = -1


C_SPEED = SPEED_COEFFICIENT
