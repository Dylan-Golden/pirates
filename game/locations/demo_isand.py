from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *

#Demo Island inherits from loction (demo island is a location)
class DemoIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        #object oriented handling . Super() refers to the parent class (location in this case)
        #so this runs the initializer of location
        self.name = 'd_island'
        self.symbol = 'I' #symbol for map
        self.visitable = True #marks island as place pirates can go ashore
        self.location = {} #dictionary of sub-locations on the island
        self.locations["beach"] = Beach(self)
        self.locations["Trees"] = Trees(self)
        #wher do the pirates start
        self.starting_location = self.locations["Beach"]
        
    def enter(self, ship):
        #what to do when the ship visits this location on the map
        announce("arrived at an island")
        
    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.locatin.enter()
        super().visit()
        
#sub-locations (Beach and Trees)
class Beach(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Beach"
        #the verbs dict was set up by the super() init
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
    
    def enter(self):
        announce ("you arrive at the beach. your ship is at anchor to the south.")
    #more complex actions should have dedicated functions to handle them
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("you return to your ship")
            #boilerplate code that stops the visit
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north"):
           config.the_player.next_loc = self.main_location.locations["Trees"]
            #text will be printed by "enter" in trees()
        if (verb == "east" or verb == "west"): 
            announce ("you walk all the way around the beach.")
        
        

class Trees(location.SubLocation):   
    def __init__(self, main_location):
        super().__init__(main_location) 
        self.name = "Trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        #add treasure
        self.verbs["take"] = self
        self.item_in_tree = Saber()
        self.item_in_clothes = items.Flintlock()
        
        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())
        
    def enter (self):
        description = "you walk into the small forest in the island"
        if self.item_in_tree != None:
            description = description + " you see a " + self.item_in_tree.name + " stuck in a tree."
        if self.item_in_clothes != None:
            description = description + " you see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the floor"
        announce(description)
    def process_verb(self, verb, cmd_list, nouns):
        if (verb in ["north", "south", "east", "west"]):
            config.the_player.next_loc = self.main_location.location["Beach"]
        if (verb == "take"):
            if (self.item_in_tree == None and self.item_in_clothes == None):
                announce ("you dont see anything to take.")
            #user just typed "take"
            elif (len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False
                i = self.item_in_tree
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce ("you take the " + i.name + " from the trees.")
                    config.the_player.add_to_inventory(i)
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                    
                i = self.item_in_clothes
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == "all"):
                    announce ("you take the " + i.name + " from the pile of clothes.")
                    config.the_player.add_to_inventory(i)
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                    
            if not at_least_one:
                #the player tries to type something that is not there
                announce ("you don't see one of those around")
            
class Saber(items.Item):
    def __init__(self):
        super().__init__("saber", 5)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"
        

        