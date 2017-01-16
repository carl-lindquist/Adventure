"""
	Carl Lindquist
	Dec 19, 2016

	Adventure: "Escape from Home"

	## Include this file in the same directory as Game.py and GamePrint.py ##

	This file contains all the game logic for a specific game for the platform Adventure.
	Can be configured to be any game within the framework of Adventure.
	Must contain methods: gameInit(), tryItem(), and interact(). Each method defines
	the game logic to be executed by Game.py

"""


"""
[desc]	A vital initialization function which sets up the specific Adventure.
		Can and should be customized to create your own Adventure!
		Must include:
			imports for Game and GamePrint
			An inventory
			A structure
				assumes location [0][0]
			return [structure, inventory]

			Should include:
				setLocation() to a specific room
				Rooms, Characters, and Items
				A splash and start text to explain the adventure
					sent to printStart()


[ret]	Structure and Inventory as a tuple (in that order)
		This return is necessary for the game to run
"""
def gameInit():
	from Game import Inventory, Character, Room, Structure
	import GamePrint

	###-------------------- Designer Code Here --------------------###

	inventory = Inventory("Pockets", 5)
	# structure = Structure("The House", "3516", layout)
	from MapBuilder import loadStructure
	structure = loadStructure()
	structure.setLocation(2, 2)
	#structure.mapEnable = False

	startSplash = """
        _____ 
       |  ___| 
       | |__ ___  ___ __ _ _ __   ___ 
       |  __/ __|/ __/ _` | '_ \ / _ \ 
       | |__\__ \ (_| (_| | |_) |  __/ 
       \____/___/\___\__,_| .__/ \___| 
                          | | 
                          |_| 
    	"""
	startText = """
    	You are a young man named Carl, and you've been couped
    	up inside for the last three days writing code! The only way
    	out of this misery is to locate your mother's car keys. Of course
    	this is easier said than done. Good luck!
    	"""
	controls = ["""        'wasd'   move in desired direction""",
	            """  'use <item>'   use an item in your inventory""",
	            """           'i'   interact with a character""",
	            """        'info'   print the name of the current structure"""
	            ]
	GamePrint.printStart(startSplash, startText, controls)

	###-------------------- Designer Code Ends Here --------------------###

	structure.curRoom().visited = True
	return [structure, inventory]


"""
[desc]	Vital funciton which modifies the game's state based on ITEM USAGE.
		Designer should create an if-elif-else statement to describe the changes
		to be made to the game-state for any item used.
		Must include:
			imports for Game.py classes and GamePrint.py
			usageString, itemsAdded

		Should include:
			imports for gameWin() and gameLose()
			Changes to rooms and characters
				Use room.state changes for ordered item usage
			Changes to the player's inventory
			Printing of text

		May include:
			A winning or losing scenario (gameLose() or gameWin())

[args]	A Structure and an Inventory to work from and/or modify
"""
def tryItem(structure, inventory, item):
	from Game import Inventory, Character, Room, Structure
	from Game import gameWin, gameLose
	import GamePrint

	room = structure.curRoom()
	usageString = ""
	itemsAdded = []

	###-------------------- Designer Code Here --------------------###

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

	#Kitchen - Knife  Note: GAMEOVER
	elif (item == "Knife" and room.name == "Kitchen"):
		gameLose("""
			Oh no! You sliced up some havarti and 
		 	completely forgot about leaving! Instead of exploring, you stay at
		 	home all day pigging out...not so bad.
			""")

	###-------------------- Designer Code Ends Here --------------------###

	else:
		usageString += "Does nothing..."

	GamePrint.printGame(structure, inventory)
	if (itemsAdded != []):
		print "You obtain: "
		for i in itemsAdded:
			print "  "+i
		print ""

	print "Used %s:" % item
	GamePrint.formattedPrint(GamePrint.lineWidth - 20, usageString)


"""
[desc]	Vital funciton which modifies the game's state based on CHARACTER INTERACTION.
		Designer should create an if-elif-else statement to describe the changes
		to be made to the game-state for any character interactions. Note that
		these interactions can use and/or check for items in the inventory.
		Must include:
			imports for Game.py classes and GamePrint.py
			usageString, itemsAdded

		Should include:
			imports for gameWin() and gameLose()
			Changes to rooms and characters
				Use room.state changes for ordered item usage
			Changes to the player's inventory
			Printing of text

		May include:
			A winning or losing scenario (gameLose() or gameWin())

[args]	A Structure and an Inventory to work from and/or modify
"""
def interact(structure, inventory):
	from Game import Inventory, Character, Room, Structure
	from Game import gameWin, gameLose
	import GamePrint

	room = structure.curRoom()
	character = room.character
	usageString = ""
	itemsAdded = []
	lineWidth = GamePrint.lineWidth
	print ""

	###-------------------- Designer Code Here --------------------###

	if (character.name == "Mom" and room.name == "Living Room" and room.state == 2):
		room.state = 3
		print "Carl:"
		print "  Hey Mom, can I borrow the car keys?"
		print ":Mom".rjust(lineWidth)
		print "Sure, if you can find them.  ".rjust(lineWidth)
		userInput = raw_input()

		print "Carl:"
		print "  Actually I think they're right next to you :)"
		print ":Mom".rjust(lineWidth)
		print "Oh you're right, here you go!  ".rjust(lineWidth)
		itemsAdded.append("Prius Key")
		inventory.items.append("Prius Key")
		userInput = raw_input()

		gameWin("""
			By locating the Prius Keys you are now free to roam Los Angeles.
			Have fun!
			""")


	elif (character.name == "Mom" and room.name == "Master Bedroom"  
		and "Cup of Tea" in inventory.items):

		print "Carl:"
		print "  Here you go mom."
		print ":Mom".rjust(lineWidth)
		print "Thanks Bub, I needed a twenty.  ".rjust(lineWidth)
		print "\nYour mom leaves the room to sip tea elsewhere."
		userInput = raw_input()

		inventory.items.remove("Cup of Tea")
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

	###-------------------- Designer Code Ends Here --------------------###

		GamePrint.printGame(structure, inventory)
		if (itemsAdded != []):
			print "You obtain: "
			for i in itemsAdded:
				print "  "+i
			print ""





