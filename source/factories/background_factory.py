from configs.config import BackGrounds
from source.background import Background
from source.factories.base import FactoryBase


class BackGroundFactory(FactoryBase):
    def __init__(self):
        FactoryBase.__init__(self)

    def produce(self, bg_type):
        if bg_type == BackGrounds.lustful_demon:
            return Background(self.full_path('lustful_daemon_2.jpg'))
        else:
            raise Exception('background %s not implemented.' % bg_type)


BGFct = BackGroundFactory()
