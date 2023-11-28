from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
import random as r

class MyIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = 'New york'
        self.symbol = 'N'
        self.visitable = True
        self.locations = {}
        self.locations["Beach"] = Beach(self)
        self.locations["Jungle"] = Jungle(self)
        self.locations["City"] = City(self)
        self.locations["Temple"] = Temple(self)
        self.locations["Cave"] = Cave(self)
        self.starting_location = self.locations["Beach"]
        
    def enter(self, ship):
        announce("Arrived at an island.")
    
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.locatin.enter()
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
            config.the_player.next_loc = self.main_location.locations["Jungle"]
        if (verb == 'east' or verb == 'west'):
            announce (f"you look {verb} the shoreline doesnt seem to end, you dont think it will be worth exploring.")
  
        
class Jungle(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Jungle"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        self.event_chance = 40
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        
    def enter(self):
        announce ("You enter the jungle on what seems to be a path.\n You keep going until you reach what seems to be a split going east and west.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'north'):
            announce ('The jungle is too thick for you to go that way.')
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.location["Beach"]
        if (verb == 'east'):
            announce ("You see a dark cave with some extremly strong looking enemys.")
            choice = str(input("Are you sure you want to go thier?(y/n)"))
            if choice == 'n':
                announce ("You head back to the split in the path.")
            elif choice == 'y':
                config.the_player.next_loc = self.main_location.location["Cave"]
            else: 
                announce ("I dont understand what you are saying.")
        if (verb == 'west'):
            announce ("you push through the foliage until you end up in a big clearing and see what seems to be an old abandoned city")
            config.the_player.next_loc = self.main_location.location["City"]
        
    
class City(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "City"
        self.verbs['east'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['west'] = self
        self.possible_items = ['Cutlass', 'Flintlock', 'Mace', 'Nothing']
        self.rand_item = self.possible_items[r.randint(0, 4)]
        
        self.event_chance = 60
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())
        
        
    def enter(self):
        announce ("You eneter the city, you see a large Temple to the north and some empty shops around you.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'east'):
            announce ('You eave the city and headback to the jungle crossroads')
            config.the_player.next_loc = self.main_location.location["Jungle"]
        if (verb == 'west'):
            city_item = self.rand_item
            if city_item != 'Nothing':
                announce (f"You enter a shop and see a {city_item}")
                char_take = str(input("What do you want to do: "))
                if char_take == 'leave':
                    announce ("You leave the building.")
                elif char_take == 'take':   
                    pass     
            else: 
                announce ("You eneter a shop and see nothing of intrest.  You leave.")
            
           # char_take = str(input("What do you want to do: "))
           # if char_take == 'leave':
           #     announce ("You leave the building.")
          #  elif char_take == 'take':
                
                
class Temple(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Temple"
        self.verbs['north'] = self
        self.verbs['south'] = self
        
        self.event_chance = 60
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())
        
    def enter(self):
        announce ("You enter the temple. There is one room to the north.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce ("You leave the temple and head back to the city.")
            config.the_player.next_loc = self.main_location.location["City"]
        if (verb == 'north'):
            #make the player believe something bad will happen if they take it
            announce ("you eneter the the room and see a small idol statue sitting on an ominous pedastill.")
        else:
            announce ("What did you say?")
            
        
class Cave(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Cave"
        self.verbs['leave'] = self
        
        self.event_chance = 100
        
    def enter(self):
        announce ("you enter the cave and are ambused by skeltons!")
    
    # need to add skeleton encounter for players to fight here