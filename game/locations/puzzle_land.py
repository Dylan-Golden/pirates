from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.events import *
import random as r
from game.player import *

class Puzzle_Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "P land"
        self.symbol = 'P'
        self.visitable = True
        self.locations = {}
        self.locations["Beach"] = Beach(self)
        self.locations["Ruins"] = Ruins(self)
        self.locations["Maze"] = Maze(self)
        self.locations["Vault"] = Vault(self)
        self.locations["Tablet"] = Tablet(self)
        self.starting_location = self.locations["Beach"]

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach(location.SubLocation):
    def __init__ (self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations["Ruins"]
        if (verb == 'south'):
            announce ("you return to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations["Tablet"]
        if (verb == 'west'):
            announce ("Their doesnt seem to be anything of intrest that way.")
            
class Ruins(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Ruin"
        self.verbs['north'] = self
        self.verbs['south'] = self
   
        
        #self.event_chance = 100
        #self.events.append(skeletons.Skeletons())
        
    def enter(self): 
        announce ("you find and enter some old ruins.\nThere are some stairs that lead down to the north.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["Beach"]
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations["Maze"]
        
class Tablet(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Tablet"
        
    def enter(self):
        announce ("You arrive at a large stone tablet with some writing on it.")
        #Capital letters tell what directions to take in maze
        announce ("Apon closer inspection you see the the tablet says \nthose who wish to walk the path: Never Enter with Envy and Never Wince When the Need arises. ")
        announce ("Their doesnt seem to be anything else to do here.")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'west' or verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["Beach"]
    
    
    
class Maze(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Maze"
        self.maze_solution = ['north', 'east', 'east', 'north', 'west', 'west', 'north']
        self.user_solution = []
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self 
        self.verbs['west'] = self 
            
              
    def enter(self):
        announce("You head down the stairs and end up in a seemingy never ending labriynth. ")
        announce ("If you go north you will end up in the maze. ")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'north'):
            if self.user_solution != self.maze_solution:
                for i in range(0, len(self.maze_solution)):
                    user_dir = str(input("What direction would you like to go: "))
                    self.user_solution.append(user_dir)
                announce(f"{self.user_solution}")
                if (self.user_solution == self.maze_solution):
                    config.the_player.next_loc = self.main_location.locations["Vault"]
                else:
                    announce("after walking for a while you mysteriously find yourself back at the entrance of the labyrinth.")
                    self.user_solution = []
            else:
                config.the_player.next_loc = self.main_location.locations["Vault"]  
            
class Vault(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "Vault"
        self.vault_solution = ['fire', 'earth', 'water']
        self.player_solution = []
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.item_available = True
        self.best_sword =  items.Dark_Drinker()     
        self.already_visited = False
    def enter(self):
        announce("After a long trek through the maze, you find youself before a large door with three pedistals next to it.")
        
    def process_verb(self, verb, cmd_list, nouns):
        announce('go north to interat with the door or south to leave. ')
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations["Maze"]
        if (verb == 'north'):
            if self.already_visited == False:
                # FEW is supposed to lead players to realize the right combination needed to open the door Fire Earth Water
                announce ("You walk up to the door and appon closer inspection it reads:\nFEW have made it this far and even FEWer make it further, FEW realize that the truth lies right in their face. ")
                announce ("After reading the text you walk up to the pedistals and realize that the depression in them resembles that of the bottom of the Idols you have found.")
                for i in range(0, len(self.vault_solution)):
                    player_input = str(input("Which idol would you like to place down: "))
                    self.player_solution.append(player_input.lower())
                if (self.player_solution == self.vault_solution):
                    self.already_visited = True
                    announce ("As you place the last Idol you a loud clunking noise and the door slowley slides out of the way.")
                    Player.self.inventory.remove("Earth Idol")
                    Player.self.inventory.remove("Fire Idol")
                    Player.self.inventory.remove("Water Idol")
                    announce ("You enter the room the door was blocking and see and sword.")
                    announce ("You take the sword,  it feels overwhelmingly powerfull.")
                    item = self.best_sword
                    config.the_player.add_to_inventory([item])
            else:
                announce("you already have been here.")