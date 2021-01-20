from configs.config import UIElements
from source.factories.base import FactoryBase
from source.ui_elements.ui_elements import MainMenu


class UIEleFactory(FactoryBase):
    def __init__(self):
        FactoryBase.__init__(self)

    def produce(self, e_type, scale_rate=1.0):
        if e_type == UIElements.main_menu:
            return MainMenu(self.full_path('lustful_daemon.jpg'), scale_rate)

        else:
            raise Exception('e_type %s not implemented.' % e_type)


UIFct = UIEleFactory()
