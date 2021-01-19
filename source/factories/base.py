import os


class FactoryBase(object):
    def __init__(self):
        self.pic_path = '../images/'

    def full_path(self, name):
        return os.path.join(self.pic_path, name)
