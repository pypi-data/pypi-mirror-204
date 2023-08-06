from . import render
from . import model
from . import colliders
from . import phisics
from . import vidSys
from . import createNewGame

class GameEngine:
    def __init__(self, tp, size=None):
        self.rend = render.GraphicsEngine(size)
        self.tp = tp(self.rend, self)
        self.rend.defDr = self.tp.render
        self.rend.defEv = self.tp.ge
        self.on = True

    def run(self):
        self.tp.start()
        while self.on:
            self.rend.update()

#try: except: pass