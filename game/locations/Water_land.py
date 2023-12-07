from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
import random as r


class MyIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = 'Florida'
        self.symbol = 'F'
        self.visitable = True
        self.locations = {}
        self.locations["Beach"] = Beach(self)
        self.locations["Hotspring"] = Hotspring(self)
        self.locations["Swamp Village"] = Swamp_Village(self)
        self.locations["Ship Wreck"] = Wrecked_Ship(self)
        self.locations["Fountain"] = Fountain(self)
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
  
        
class Hotspring(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Hotspring"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        self.event_chance = 40
        self.events.append(merfolk.Merfolks())
        
    def enter(self):
        announce ("After drudging through swamp you find a nice hotspring with some patways off to the side.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'north'):
            announce ("You see a fountain with some strange looking people around it..")
            choice = str(input("Are you sure you want to go thier?(y/n) "))
            if choice == 'n':
                announce ("You head back to the hotspring.")
            elif choice == 'y':
                config.the_player.next_loc = self.main_location.locations["Fountain"]
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["Beach"]
        if (verb == 'east'):
            announce ('A stream of lava is blocking the way.')
        if (verb == 'west'):
            announce ("you force your party through the intense heat and end up near a burnt down city.")
            config.the_player.next_loc = self.main_location.locations["Swamp Village"]
        
    
class Swamp_Village(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Swamp Village"
        self.verbs['east'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['west'] = self
        #player more likely to get a spear
        self.possible_items = [items.Flintlock(), items.Spear(), items.Cutlass(),  'Nothing', 'Nothing']
        self.city_item = self.possible_items[r.randint(0, 5)]
        self.item_available = True
        self.medicine_available = True
        
        self.event_chance = 60
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(skeletons.Skeletons())
        
        
    def enter(self):
        announce ("You enter a swamp village, it is very unpleasent and smelly.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'east'):
            announce ('You leave and head back to the hotspring.')
            config.the_player.next_loc = self.main_location.locations["Hotspring"]
        if (verb == 'west' and self.item_available == True):
            if self.city_item != 'Nothing':
                announce (f"You go to a large hut{self.city_item.name}")
                char_take = str(input("What do you want to do: "))
                if char_take == 'leave':
                    announce ("You exit the hut.")
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
              config.the_player.next_loc = self.main_location.locations["Ship Wreck"]
        if (verb == 'south'):
            if self.medicine_available == True:
                announce ('you search a small hut and find some medicine.')
                config.the_player.ship.medicine += 1
                self.medicine_available = False
            else:
                announce ('their is nothing their')
            
            
            
                
                
class Wrecked_Ship(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Ship Wreck"
        self.verbs['north'] = self
        self.verbs['south'] = self
        
        self.temple_item = Water_Idol()
        self.item_available = True
        
        self.event_chance = 60
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(skeletons.Skeletons())
        
    def enter(self):
        announce ("You enter and wrecked ship and see a oen room to the north")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce ("You leave the ship and got back to the village.")
            config.the_player.next_loc = self.main_location.locations["Swamp Village"]
        if (verb == 'north'):
            if self.item_available == True:
                announce ("you enter the the room and see a small idol statue sitting in a treasure chest.")
                choice = str(input("What do you want to do: "))
                if choice == 'take':
                    announce ("You take the idol of the pedestal....\nNothing happend.")
                    announce ("After taking the idol you inspect and notice a water drop symbol on it.")
                    config.the_player.add_to_inventory([self.temple_item])
                    self.item_available = False
            else:
                announce ('Their is nothing else left here.')
            
        
class Fountain(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Fountan"
        self.verbs['north'] = self
        self.verbs['south'] = self
        
        
        self.event_chance = 100
        self.events.append(merfolk.Merfolks())
        
        self.verbs['take'] = self
        self.fountain_loot = items.Spear()
        
    def enter(self):
        announce ("you approach the Fountain ")
        if self.fountain_loot != None:
            announce ('You spot something in the fountain.')
        
        
    def process_verb(self, verb, cmd_list, nouns):
        self.event_chance = 0
        at_least_one = False
        item = self.fountain_loot
        if (verb == 'take'):
            if self.fountain_loot == None or at_least_one == True:
                announce ("their is nothing to take.")
            else:
                announce ("you obtained a spear and also find some medicine.")
                config.the_player.add_to_inventory([item])
                config.the_player.ship.medicine += 3
                self.fountain_loot = None
                config.the_player.go = True
                at_least_one = True
                
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["Volcano"]
    
class Water_Idol(items.Item):
     def __init__(self):
        super().__init__("Water Idol", 1000)