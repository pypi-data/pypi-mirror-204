from . import render
# from . import phisics

class GameEngine:
    def __init__(self, size, tp):
        self.rend = render.GraphicsEngine(size=size)
        self.tp = tp(self.rend, self)
        self.rend.defDr = self.tp.render

    def run(self):
        self.tp.start()
        while True:
            self.tp.update()
            self.rend.update()