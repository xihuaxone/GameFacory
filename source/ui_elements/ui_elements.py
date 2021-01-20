from source.base import PicBase, MenuMap


class UIBase(PicBase):
    def __init__(self, pic_path, scale_rate, *args, **kwargs):
        PicBase.__init__(self, pic_path, scale_rate, *args, **kwargs)


class MainMenu(UIBase):
    def __init__(self, pic_path, scale_rate):
        UIBase.__init__(self, pic_path, scale_rate, fit_screen=True, middle=True)
        self.e_id = MenuMap.register(self)
        # self._surface.set_alpha(50)  # 设置alpha通道值后疯狂掉帧；
