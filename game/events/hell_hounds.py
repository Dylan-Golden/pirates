import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class Hell_Hounds(event.Event):
    
    def __init__(self):
        self.name = "Hell Hound attack"
    
    def process(self,world):
        result = {}
        result["message"] = "The Hell Hounds have been vanquished."
        monsters = []
        min = 2
        uplim = 4
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.Hell_Hound("Hell Hound "+str(n)))
            n += 1
        announce ("The crew has fallen pray to a group of Hell Hounds")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result