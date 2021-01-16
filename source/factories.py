from configs.config import BackGrounds, CollideReaction, Characters
from source.background import Background
from source.character import Character


class BackGroundFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def produce(bg_type):
        if bg_type == BackGrounds.lustful_demon:
            return Background('../images/lustful_daemon_2.jpg')
        else:
            raise Exception('background %s not implemented.' % bg_type)


class CharacterFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def produce(c_type, scale_rate=1.0):
        if c_type == Characters.awesome_demon:
            return Character('../images/awesome_daemon.png', scale_rate, CollideReaction.rebound)
        else:
            raise Exception('character %s not implemented.' % c_type)