import math

from configs.config import CoordinateType, CoordinateList


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

    @classmethod
    def cal_vertex_len(cls, c: CoordinateType):
        d = math.sqrt(c[0] ** 2 + c[1] ** 2)
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

    @classmethod
    def decompose_vertex(cls, v_decompose: CoordinateList, v_base: CoordinateList):
        """
        :param v_decompose: 待分解的矢量, [point_a, point_t]；
        :param v_base: 分解的基准矢量，即 v_decompose会向该矢量线上投影, [point_a, point_b]；
        :return: 法线向量normal_vertex, 切线向量tan_vertex; (原点a)
        """
        a, b = v_base
        a_1, t = v_decompose
        if a[0] != a_1[0] or a[1] != a_1[1]:
            raise Exception('vertexes not satisfied, '
                            'can not get base point.')
        foot = cls.get_foot_point(t, [a, b])
        normal_vertex = cls.subtract(t, foot)
        tan_vertex = cls.subtract(foot, a)
        return normal_vertex, tan_vertex

    @classmethod
    def vertex_rorate(cls, c_vertex: CoordinateList, angle: int):
        pass
        # TODO 根据给定矢量（原点坐标， 顶点坐标），计算旋转一定角度后得到的新矢量；

    @classmethod
    def cal_unit_vertex(cls, c1: CoordinateType, c2: CoordinateType):
        """
        :param c1: 矢量原点坐标
        :param c2: 矢量顶点坐标
        :return: 该矢量的单元矢量（即把该矢量长度缩短为1，方向不变，得到的新矢量）；
        """
        v = cls.subtract(c2, c1)
        _d = cls.cal_vertex_len(v)
        _k = 1 / _d if _d else 0
        unit_v = Coordinate.multiply(v, _k)
        return unit_v


class Formulas(object):
    @staticmethod
    def speed_after_collide(m1, m2, v1, v2, k_restitution):
        # 非弹性碰撞时，反弹初速度计算。恢复系数k_restitution;
        v1_new = (m1 * v1 + m2 * v2 - m2 * k_restitution * (v1 - v2)) / (m1 + m2)
        return v1_new

    @staticmethod
    def speed_vertex_after_collide(m1, m2, v1, v2, k_restitution):
        # 非弹性碰撞时，反弹初速度计算。恢复系数k_restitution;
        m1_x_v1 = Coordinate.multiply(v1, m1)
        m2_x_v2 = Coordinate.multiply(v1, m1)
        v1_m_v2 = Coordinate.subtract(v1, v2)
        (m1 + m2)

        temp_1 = Coordinate.sum(m1_x_v1, m2_x_v2)
        temp_2 = Coordinate.multiply(v1_m_v2, m2 * k_restitution)
        temp_3 = (Coordinate.subtract(temp_1, temp_2))
        v1_new = Coordinate.multiply(temp_3, 1 / (m1 + m2))
        return v1_new

    @staticmethod
    def friction_acceleration_cal(k_friction, vertical_a):
        # 摩擦力引起的运动方向上的加速度：f_a = 摩擦力系数k_friction * 正压力的加速度vertical_a（水平面上即为引力常数9.8）;
        friction_acceleration = k_friction * vertical_a
        return friction_acceleration
