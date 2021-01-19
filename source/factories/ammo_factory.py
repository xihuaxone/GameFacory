from configs.config import AmmoTypes, CollideReaction
from source.ammos.ball import Ball
from source.factories.base import FactoryBase


class AmmoFactory(FactoryBase):
    def __init__(self):
        FactoryBase.__init__(self)

    @staticmethod
    def produce(ammo_type, scale_rate, color, center, speed):
        if ammo_type == AmmoTypes.ball:
            return Ball('', scale_rate, CollideReaction.rebound, color, center, speed)
        else:
            raise Exception('ammo_type %s not implemented.' % ammo_type)


AmmoFct = AmmoFactory()
