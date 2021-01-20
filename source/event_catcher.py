import pygame

from configs.config import PressState, UIElements
from source.base import UIMap
from source.factories.ui_ele_factory import UIFct


class WindowEventMonitor(object):
    RUNNING = True
    main_menu_id = None

    def __init__(self):
        pass

    @classmethod
    def call_menu(cls):
        menu = UIFct.produce(UIElements.main_menu)
        cls.main_menu_id = menu.e_id

    @classmethod
    def close_menu(cls):
        UIMap.drop_if_exists(cls.main_menu_id)

    @classmethod
    def menu_switch(cls):
        cls.RUNNING = not cls.RUNNING
        if not cls.RUNNING:
            cls.call_menu()
        else:
            cls.close_menu()

    @classmethod
    def event_monitor(cls, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cls.menu_switch()


class EventMonitor(object):
    def __init__(self):
        pass

    def catch_mouse_event(self, event, e_type):
        if e_type == pygame.MOUSEBUTTONDOWN:
            self.l_click(event.pos)

        elif e_type == pygame.MOUSEMOTION:
            self.mouse_motion(event.pos)

        elif e_type == pygame.MOUSEBUTTONUP:
            self.l_click_finish(event.pos)

    def catch_keyboard_event(self, event, e_type):
        if (e_type == pygame.KEYDOWN) or (e_type == pygame.KEYUP):
            if e_type == pygame.KEYDOWN:
                press_state = PressState.PRESS
            else:
                press_state = PressState.RELEASE
            key = event.key
            if key == pygame.K_SPACE:
                self.attach_switch(press_state)
            if key == pygame.K_w:
                self.move_up_switch(press_state)
            if key == pygame.K_s:
                self.move_down_switch(press_state)
            if key == pygame.K_a:
                self.move_left_switch(press_state)
            if key == pygame.K_d:
                self.move_right_switch(press_state)

            if key == pygame.K_LSHIFT:
                self.speed_switch(press_state)

    def event_monitor(self, event):
        self.catch_mouse_event(event, event.type)
        self.catch_keyboard_event(event, event.type)

    def move_left_switch(self, press_state):
        raise NotImplementedError

    def move_right_switch(self, press_state):
        raise NotImplementedError

    def move_up_switch(self, press_state):
        raise NotImplementedError

    def move_down_switch(self, press_state):
        raise NotImplementedError

    def attach_switch(self, press_state):
        raise NotImplementedError

    def speed_switch(self, press_state):
        raise NotImplementedError

    def l_click(self, pos):
        raise NotImplementedError

    def mouse_motion(self, pos):
        raise NotImplementedError

    def l_click_finish(self, pos):
        raise NotImplementedError
