import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class Merfolks(event.Event):
    
    def __init__(self):
        self.name = "Merfolk attack"
    
    def process(self,world):
        result = {}
        result["message"] = "The merfolk are defeated."
        monsters = []
        min = 3
        uplim = 7
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.Merfolk("Merfolk "+str(n)))
            n += 1
        announce ("The crew was attacked by a group of angry merfolk.")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result