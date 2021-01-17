from typing import List

CoordinateType = List[float or int]
CoordinateList = List[CoordinateType]


class Products(object):
    background = 'background'
    character = 'character'
    area = 'area'


class BackGrounds(object):
    lustful_demon = 'lustful_demon'


class Characters(object):
    awesome_demon = 'awesome_demon'
    billiard = 'billiard'


class Areas(object):
    billiard_holes = 'billiard_holes'


class CollideReaction(object):
    destroy = 'destroy'  # 碰撞即销毁
    rebound = 'rebound'  # 反弹
    sticking = 'sticking'  # 粘附在被撞物体表面
    motionless = 'motionless'  # 静止
    ignore = 'ignore'  # 忽略碰撞（穿过）


FPS = 300  # 锁帧
INIT_SCREEN_SIZE = (1920, 1080)

SPEED_COEFFICIENT = 1  # 速度修正系数
FRAME_METRE_RATIO = 100  # 像素/米 的比例关系

GRAVITY = 9.8  # 重力加速度常量g
GRAVITY_COEFFICIENT = 0  # 重力加速度修正系数
GRAVITY_RESTITUTION_COEFFICIENT = 0.8  # 非完全弹性碰撞的恢复系数

DEFAULT_FRICTION_COEFFICIENT = 1  # 默认的动摩擦因数，所有实现摩擦反馈的对象，都默认采用该值

TEST_MODE = True  # 测试模式，会显示图形对象的rect矩形边，以及碰撞检测的圆形边缘
FPS_WATCH = False  # 监控帧率


class Color(object):
    black = (0, 0, 0)
    white = (255, 255, 255)


class Defense(object):
    INVINCIBLE = -99
    ONE_HIT_KILL = -1


C_SPEED = SPEED_COEFFICIENT
FMR = FRAME_METRE_RATIO
