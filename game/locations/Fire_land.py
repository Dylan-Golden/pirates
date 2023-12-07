from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
import random as r


class MyIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = 'Texas'
        self.symbol = 'T'
        self.visitable = True
        self.locations = {}
        self.locations["Beach"] = Beach(self)
        self.locations["Volcano"] = Volcano(self)
        self.locations["Burnt_city"] = Burnt_City(self)
        self.locations["Temple"] = Temple(self)
        self.locations["Obelisk"] = Obelisk(self)
        self.starting_location = self.locations["Beach"]
        
    def enter(self, ship):
        announce("Arrived at an island.")
    
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        
        
#Sub-locations        
class Beach(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        self.event_chance = 30
        self.events.append(seagull.Seagull())
    
    def enter(self):
        announce ("you arrive at the beach. your ship is at anchor to the south.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce ("you return to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations["Volcano"]
        if (verb == 'east' or verb == 'west'):
            announce (f"you look {verb} the shoreline doesnt seem to end, you dont think it will be worth exploring.")
  
        
class Volcano(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Volcano"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
    def enter(self):
        announce ("You head to the only recognizable landmark, that being the base of a large volcano and see some narrow pathways leading somewhere.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'north'):
            announce ("You see a large obelisk being guarded by some strong enemies.")
            choice = str(input("Are you sure you want to go thier?(y/n) "))
            if choice == 'n':
                announce ("You head back to the split in the path.")
            elif choice == 'y':
                config.the_player.next_loc = self.main_location.locations["Obelisk"]
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["Beach"]
        if (verb == 'east'):
            announce ('A stream of lava is blocking the way.')
        if (verb == 'west'):
            announce ("you force your party through the intense heat and end up near a burnt down city.")
            config.the_player.next_loc = self.main_location.locations["Burnt_City"]
        
    
class Burnt_City(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Burnt_City"
        self.verbs['east'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['west'] = self
        #player more likely to get a spear
        self.possible_items = [items.Flintlock(), items.Spear(), items.Spear(), items.Mace(),  'Nothing']
        self.city_item = self.possible_items[r.randint(0, 5)]
        self.item_available = True
        self.medicine_available = True
        
        self.event_chance = 60
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(skeletons.Skeletons())
        
        
    def enter(self):
        announce ("You enter the burnt down city and are surround by piles of ember and remains of what resemble buildings.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'east'):
            announce ('You leave and head back to the base of the Volcano.')
            config.the_player.next_loc = self.main_location.locations["Volcano"]
        if (verb == 'west' and self.item_available == True):
            if self.city_item != 'Nothing':
                announce (f"You go to a large pile of rubble and see a {self.city_item.name}")
                char_take = str(input("What do you want to do: "))
                if char_take == 'leave':
                    announce ("You leave the rubble behind.")
                elif char_take == 'take':   
                    config.the_player.add_to_inventory([self.city_item])   
                    self.item_available = False
                    announce (f'You take the {self.city_item}  and leave.')
            else: 
                announce ("You eneter a shop and see nothing of intrest.  You leave.")
                self.item_available = False
        elif (verb == 'west' and self.item_available == False):
            announce ("you already checked here.")
        if (verb == 'north'):
              config.the_player.next_loc = self.main_location.locations["Temple"]
        if (verb == 'south'):
            if self.medicine_available == True:
                announce ('you search through a pile of embers and find some medicine')
                config.the_player.ship.medicine += 1
                self.medicine_available = False
            else:
                announce ('their is nothing their')
            
            
            
                
                
class Temple(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Temple"
        self.verbs['north'] = self
        self.verbs['south'] = self
        
        self.temple_item = Fire_Idol()
        self.item_available = True
        
        self.event_chance = 60
        self.events.append(hell_hounds.Hell_Hounds())
        self.events.append(skeletons.Skeletons())
        
    def enter(self):
        announce ("You enter the temple. There is one room to the north.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce ("You leave the temple and head back to the city.")
            config.the_player.next_loc = self.main_location.locations["Burnt_City"]
        if (verb == 'north'):
            if self.item_available == True:
                #make the player believe something bad will happen if they take it
                announce ("you enter the the room and see a small idol statue sitting on an ominous pedastill.")
                choice = str(input("What do you want to do: "))
                if choice == 'take':
                    announce ("You take the idol of the pedestal....\nNothing happend.")
                    announce ("After taking the idol you inspect and notice a firey looking symbol on it.")
                    config.the_player.add_to_inventory([self.temple_item])
                    self.item_available = False
            else:
                announce ('Their is nothing else left here.')
            
        
class Obelisk(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Obelisk"
        self.verbs['north'] = self
        self.verbs['south'] = self
        
        
        self.event_chance = 100
        self.events.append(hell_hounds.Hell_Hounds())
        
        self.verbs['take'] = self
        self.Obelisk_loot = items.Spear()
        
    def enter(self):
        announce ("you approach the Obelisk ")
        if self.Obelisk_loot != None:
            announce ('You spot something at the base of the Obelisk!')
        
        
    def process_verb(self, verb, cmd_list, nouns):
        self.event_chance = 0
        at_least_one = False
        item = self.Obelisk_loot
        if (verb == 'take'):
            if self.Obelisk_loot == None or at_least_one == True:
                announce ("their is nothing to take.")
            else:
                announce ("you obtained a spear.")
                config.the_player.add_to_inventory([item])
                self.Obelisk_loot = None
                config.the_player.go = True
                at_least_one = True
                
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["Volcano"]
    
class Fire_Idol(items.Item):
     def __init__(self):
        super().__init__("Fire Idol", 1000)