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

	layout[0][2] = Room("Master Bedroom", """
		A big bed sits in the middle of this well decorated room. Dressers
		and boxes abound. Ginger is curled up next to the bed.
		Your mom is snoozing peacefully after a horrendously challenging row. 
		""", ["Blue Mug"], Character("Mom", "(Sleepily) Make me a cup of tea?"))
	layout[0][2].locked = True

	layout[0][3] = Room("Hallway", """
		End of the hall. There's a door to your left, but it's locked from
		the inside. A light shuffle comes from within.
		""", [], None)
	layout[1][3] = Room("Hallway", "", [], None)
	layout[2][3] = Room("Hallway", "", [], None)
	layout[3][3] = Room("Hallway", "", [], None)


	layout[4][3] = Room("Living Room", """
		A grand old room with a fireplace. Large
		wooden beams cross over your head. A piano blocks a large 
		window. The fireplace looks workable. A dog stands
		guard by the door.
		""", ["Ripstick"], Character("Ginger", "Rrraow"))

	layout[1][4] = Room("Kitchen", """
	A small kitchen with blue tile countertops.
	""",
	["Matches", "Knife"], None)

	inventory = Inventory("Pockets", 5)
	structure = Structure("The House", "3516", layout)
	structure.setLocation(2, 2)
	return [structure, inventory]


"""
	A set of conditionals to change the game. This method of doing things
	is really bad. User Should change this to modify the Game's logic

"""
def tryItem(structure, inventory, item):
	from Game import Inventory, Character, Room, Structure
	import GamePrint

	room = structure.curRoom()
	usageString = ""
	itemsAdded = []

	#Living Room - Books state 1   Note: Use multiple states for multiItem rooms
	if (item == "Books" and room.name == "Living Room" and room.state == 0):
		room.state = 1
		inventory.items.remove(item)
		room.character.dialogue = "(staring at you)"
		room.desc = """
		A grand old room with a fireplace. Large wooden beams cross
		over your head. A piano blocks a large window. A dog looks at 
		you confusedly. The fireplace is stocked with cheesy novels.
		"""
		usageString += "You've filled the fireplace with awful books."

	#Living Room - Matches state 2
	elif (item == "Matches" and room.name == "Living Room" and room.state == 1):
		room.state = 2
		inventory.items.remove(item)
		room.character = None
		structure.layout[0][2].locked = False
		structure.layout[0][3].desc = """
		End of the hall. The door to your left is slightly ajar!
		Your hear snuffling noises inside.
		"""
		room.desc = """
		A grand old room with a raging fireplace. Large wooden beams cross
		over your head. A piano blocks a large window. The dog seems to have
		left due to all the smoke.
		"""
		usageString += """Ginger skulks out of the room due to all the new smoke.
		 					You hear a door open somewhere.
	 					"""

	#Bedroom - Ripstick state 1
	elif (item == "Ripstick" and room.name == "Bedroom" and room.state == 0):
		room.state = 1
		inventory.items.remove(item)
		inventory.items.append("Books")
		itemsAdded.append ("Books")
		room.character = None
		room.desc = """
		Two beds, side by side. Light shines in through two windows
		in front of you. Now that Sam has left, you notice all the terrible books
		that were hiding behind him.
		"""
		usageString += "Sam takes the Ripstick to cruise around the house." 

	#Kitchen - Blue Mug    Note: Some usages don't require a room state change
	elif (item == "Blue Mug" and room.name == "Kitchen"):
		inventory.items.remove(item)
		inventory.items.append("Cup of Tea")
		itemsAdded.append("Cup of Tea")
		usageString += "You make a strong cup of black tea."

	#Master Bedroom - Cup of Tea
	elif (item == "Cup of Tea" and room.name == "Master Bedroom"):
		inventory.items.remove(item)
		room.desc = """
		A big bed sits in the middle of this well decorated room. Dressers
		and boxes abound.
		"""
		room.character = None
		structure.layout[4][3].character = Character("Mom", "(Reading silently)") 
		structure.layout[4][3].desc = """
		A grand old room with a raging fireplace. Large wooden beams cross
		over your head. A piano blocks a large window. Your mom is sipping tea
		on the couch while reading ... GQ?
		"""
		usageString += "Your mom leaves the room to sip tea elsewhere."


	else:
		usageString += "Does nothing..."

	GamePrint.printGame(structure, inventory)
	if (itemsAdded != []):
		print "You obtain: "
		for i in itemsAdded:
			print "  "+i
		print ""

	print "Used %s:" % item
	usageLines = GamePrint.splitLines(50, usageString)
	for l in usageLines:
		if l:
			print "  " + l































