"""
	Carl Lindquist
	Dec 19, 2016

	Adventure: "Test Game"

	This file contains all the game logic for a specific game for the platform Adventure
	Can be configured to be any game within the framework of Adventure.
	Must contain methods: gameInit(), as well as a dictionary describing
	rooms changed states depending on items used.
	tryItem() changes one room into the other.
	
"""



def gameInit():
	from Game import Inventory, Character, Room, Structure

	layout = [[None for x in range(5)] for y in range(5)] 

	layout[2][2] = Room("Bedroom", """
		Two beds, side by side. Light shines in through two windows
		in front of you.
		""", [], Character("Sam", "Hey brother!"))

	layout[0][3] = Room("Hallway", "", ["Gargantuan Orangutan"], 
		Character("Gargantuan Orangutan", "I am the Gigantopithicus"))
	layout[1][3] = Room("Hallway", "", [], None)
	layout[2][3] = Room("Hallway", "", [], None)
	layout[3][3] = Room("Hallway", "", [], None)


	layout[4][3] = Room("Living Room", """
		A grand old room with a fireplace. Large
		wooden beams cross over your head. A piano stands by 
		a window. The fireplace looks used...recently.
		""", ["Ripstick"], Character("Ginger", "  Rrraow"))

	layout[1][4] = Room("Kitchen", """
	A small kitchen with blue tile countertops.
	""",
	["Matches", "Knife"], None)

	inventory = Inventory("Satchel", 5)
	structure = Structure("The House", "3516", layout)
	structure.setLocation(2, 2)
	return [structure, inventory]











