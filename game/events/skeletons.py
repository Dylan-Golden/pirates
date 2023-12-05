import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class Skeletons(event.Event):
    
    def __init__(self):
        self.name = "Skeleton ambush"
    
    def process(self,world):
        result = {}
        result["message"] = "The skeltons are defeated."
        monsters = []
        min = 6
        uplim = 10
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.Skeleton("Skeleton "+str(n)))
            n += 1
        announce ("The crew was ambushed by a group of skeletons.")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
