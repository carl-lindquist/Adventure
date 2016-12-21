"""
	<YOUR NAME>
	<DATE>

	Adventure: <YOUR ADVENTURE TITLE HERE>

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

	###-------------------- Add Designer Code Here --------------------###

	#Array to become a structure
	structureRows = #< SPECIFY STRUCTURE LENGTH >#
	structureCols = #< SPECIFY STRUCTURE WIDTH >#
	#Indexing is: layout[row][column]
	layout = [[None for x in range(structureCols)] for y in range(structureRows)] 
	
	"""
		<ADD SOME CHANGES TO LAYOUT HERE>
	"""
	
	startSplash = """
    	<YOUR START SPLASH HERE>
    	I recommend:
    	http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
    	"""
	startText = """
    	<YOUR START TEXT HERE>
    	"""
	GamePrint.printStart(startSplash, startText) #optional start screen

	###-------------------- Designer Code Ends Here --------------------###

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

	###-------------------- Add Designer Code Here --------------------###

	"""
		<ADD SOME ITEM USAGE EVENTS HERE>
	"""

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
	lineWidth = 65
	print ""

	###-------------------- Add Designer Code Here --------------------###

	"""
		<ADD SOME CHARACTER INTERACTIONS HERE
	"""

	###-------------------- Designer Code Ends Here --------------------###

		GamePrint.printGame(structure, inventory)
		if (itemsAdded != []):
			print "You obtain: "
			for i in itemsAdded:
				print "  "+i
			print ""





