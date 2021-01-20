import pygame

from source.base import PicBase, Global


class Background(PicBase):
    mass = 999999

    def __init__(self, pic_path):
        PicBase.__init__(self, pic_path, 1, True, True)

    # @staticmethod
    # def scale(surface_pic, *args, **kwargs):
    #     origin_width, origin_height = surface_pic.get_size()
    #     if origin_width / Global.screen_w > origin_height / Global.screen_h:
    #         scale_rate = Global.screen_w / origin_width
    #     else:
    #         scale_rate = Global.screen_h / origin_height
    #     return pygame.transform.scale(
    #         surface_pic,
    #         (int(origin_width * scale_rate),
    #          int(origin_height * scale_rate)))
