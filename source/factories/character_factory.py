from configs.config import CollideReaction, Characters, Color
from source.character import Character
from source.characters.awesome_demon import TestMe
from source.characters.billiard import Billiard
from source.factories.base import FactoryBase


class CharacterFactory(FactoryBase):
    def __init__(self):
        FactoryBase.__init__(self)

    def produce(self, c_type, scale_rate=1.0, color=Color.white):
        if c_type == Characters.awesome_demon:
            return Character(self.full_path('awesome_daemon.png'), scale_rate, CollideReaction.rebound)

        elif c_type == Characters.billiard:
            return Billiard('', scale_rate, CollideReaction.rebound, color)

        elif c_type == Characters.test_me:
            return TestMe(self.full_path('awesome_daemon.png'), scale_rate, CollideReaction.rebound)

        else:
            raise Exception('character %s not implemented.' % c_type)


CFct = CharacterFactory()
