from configs.config import PressState, AmmoTypes, Color
from source.character import Character
from source.event_catcher import EventMonitor
from source.factories.ammo_factory import AmmoFct
from source.utils import Coordinate


class TestMe(Character, EventMonitor):

    def __init__(self, *args, **kwargs):
        Character.__init__(self, *args, **kwargs)
        EventMonitor.__init__(self)
        self.mv_speed_x = 500
        self.mv_speed_y = 500
        self.mv_speed_x_h = 800
        self.mv_speed_y_h = 800
        self._stress_speed = [0, 0]
        self.SPEED_UP = False
        self.LEFT_MOVING = False
        self.RIGHT_MOVING = False
        self.UP_MOVING = False
        self.DOWN_MOVING = False
        self.mouse_pos = [[0, 0], [0, 0], [0, 0]]
        self._shoot_speed = 5000

    @property
    def speed(self):
        return self._stress_speed

    def set_speed_x(self, x):
        self._stress_speed[0] = x

    def set_speed_y(self, y):
        self._stress_speed[1] = y

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
        self.update_speed([dx, dy])
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

    def shoot(self):
        ball_radius = 10
        _unit_v = Coordinate.cal_unit_vertex(self.center, self.mouse_pos[2])
        center = Coordinate.sum(Coordinate.multiply(_unit_v, (self.radius + ball_radius) * 1.1), self.center)
        speed = Coordinate.multiply(_unit_v, self._shoot_speed)

        AmmoFct.produce(AmmoTypes.ball, ball_radius, Color.black, center, speed)

    def l_click(self, pos):
        self.mouse_pos[0] = pos

    def mouse_motion(self, pos):
        self.mouse_pos[1] = pos

    def l_click_finish(self, pos):
        self.mouse_pos[2] = pos
        self.shoot()
