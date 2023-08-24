from gene import Gene

class Epigene(object):
    def __init__(self, parent: Gene, expression: float = 0.5):
        # the gene this epigene affects
        self.parent: Gene = parent
        # to what degree the epigene affects the parent gene.
        # plug into a sigmoid curve, probably
        self.expression: float = expression

    def receive_signal(self, delta: float = 0.5):
        pass

    def __str__(self):
        return "Epigene for " + str(self.parent)