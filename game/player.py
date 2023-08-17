def move(self, distance):
    self.position += distance
def attack():
    pass
class Player(object):
    def __init__(self):
        self.position: float = 0.
        self.hp:       int   = 10
        self.actions = move, attack

class Enemy(object):
    def __init__(self):
        self.position:  float = 10.
        self.hp:        int   = 3
        self.actions = move, attack