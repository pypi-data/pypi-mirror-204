from .recorder import Recorder
from .stimulator import Stimulator


class Rsa(Stimulator, Recorder):
    def __init__(self):   
        Stimulator.__init__(self)
        Recorder.__init__(self)