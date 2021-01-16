import math

from configs.config import CoordinateType


class Coordinate(object):
    @staticmethod
    def sum(*coordinate_list: CoordinateType):
        x = y = 0
        for c in coordinate_list:
            x += c[0]
            y += c[1]

        return [x, y]

    @staticmethod
    def subtract(coordinate_a: CoordinateType, coordinate_b: CoordinateType):
        return [coordinate_a[0] - coordinate_b[0],
                coordinate_a[1] - coordinate_b[1]]

    @staticmethod
    def multiply(point: CoordinateType, k):
        return [point[0] * k, point[1] * k]

    @staticmethod
    def cal_distance(coordinate_a: CoordinateType, coordinate_b: CoordinateType):
        x0, y0 = coordinate_a
        x1, y1 = coordinate_b
        dx = x1 - x0
        dy = y1 - y0
        d = math.sqrt(dx**2 + dy**2)
        return d

    @staticmethod
    def get_foot_point(point: CoordinateType, line: CoordinateType):
        x0, y0 = point
        x1, y1 = line[0]
        x2, y2 = line[1]
        if x1 == x2 and y1 == y2:
            return [x1, y1]
        k = -((x1 - x0) * (x2 - x1) + (y1 - y0) * (y2 - y1)) / ((x2 - x1) ** 2 + (y2 - y1) ** 2)

        xn = k * (x2 - x1) + x1
        yn = k * (y2 - y1) + y1
        return [xn, yn]

    @staticmethod
    def data_stock_calculate(data: float, limit=(-1.0, 1.0)):
        if limit[0] < data < limit[1]:
            stock = data
            keep = 0
        else:
            stock, keep = math.modf(data)

        return int(keep), stock


class Formulas(object):
    @staticmethod
    def speed_after_collide(m1, m2, v1, v2, k_restitution):
        # 非弹性碰撞时，反弹初速度计算。恢复系数k_restitution;
        v1_new = (m1 * v1 + m2 * v2 - m2 * k_restitution * (v1 - v2)) / (m1 + m2)
        return v1_new

    @staticmethod
    def friction_acceleration_cal(k_friction, vertical_a):
        # 摩擦力引起的运动方向上的加速度：f_a = 摩擦力系数k_friction * 正压力的加速度vertical_a（水平面上即为引力常数9.8）;
        friction_acceleration = k_friction * vertical_a
        return friction_acceleration
