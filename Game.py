"""
	Carl Lindquist
	Dec 18, 2016

	## Include this file in the same directory as Adventure.py and GamePrint.py ##

	Main code to run an "Adventure Game". This file should not be modified unless
	you're adding new features to the game. Include in the same directory an
	'Adventure.py' file, where Adventure.py will contain the game 
	logic for a specific adventure: character names, rooms, interactions, etc.
	Checkout README for more info.

"""

import GamePrint, Adventure

##------------------------------ Funcitons ------------------------------##

def gameWin(text):
	GamePrint.printWin(text)
	import sys
	sys.exit()

def gameLose(text):
	GamePrint.printLose(text)
	import sys
	sys.exit()

##------------------------------ Classes ------------------------------##

"""
	Game characters used for:
		character text
		interactions
"""
class Character(object):

	def __init__(self, name, dialogue):
		self.name = name
		self.dialogue = dialogue

"""
	Variably sized inventory to hold items
"""
class Inventory(object):

	def __init__(self, name, size):
		self.name = name
		self.maxSize = size
		self.items = []
		self.width = 0 #Printng width


	def addItems(self, room):
		itemsAdded = []
		for i in room.items:
			if len(self.items) < self.maxSize:
				self.items.append(i)
				itemsAdded.append(i)
		for i in itemsAdded:
			room.items.remove(i)
		return itemsAdded


	def removeItem(self, item):
		self.items.remove(item)


	def printLines(self):
		self.width = len(self.name) + 4
		for i in self.items: #expand print width for largest item
			if (len(i) > self.width - 4):
				self.width = len(i) + 4 

		lines = []
		lines.append("/"+self.name.center(self.width)+"\\")
		lines.append("|"+"-"*(self.width)+"|")
		for i in self.items:
			lines.append("|  "+i.ljust(self.width - 2)+"|")
		lines.append("\\"+ "_" * (self.width) + "/")
		return lines

"""
	Rooms can hold:
		description
		items
		characters
		can be locked or unlocked (*lock arg)
"""
class Room(object):

	def __init__(self, name, description, items, character, *lock):
		self.name = name
		self.desc = description
		self.items = items
		self.character = character
		self.visited = False
		self.state = 0
		self.locked = True if lock else False 


"""
	Structures hold a "2-D array" of Rooms
	Their names and descriptions are unused currently, but
	allows implementation for multiple in-game structures in the future
"""
class Structure(object):

	def __init__(self, name, description, layout):
		self.name = name
		self.desc = description
		self.layout = layout
		self.r = 0
		self.c = 0

		self.rowCount = 0
		self.colCount = 0
		for x in layout:
			self.rowCount += 1

		for x in layout[0]:
			self.colCount += 1

	def curRoom(self):
		return self.layout[self.r][self.c]

	def availableMoves(self):
		r = self.r
		c = self.c
		up, left, down, right = ' ', ' ', ' ', ' '
		if (self.__isValidRoom(r-1, c)):
			up = "W"
		elif(self.__isLockedRoom(r-1, c)):
			up = "X"
		if (self.__isValidRoom(r, c-1)):
			left = "A"
		elif(self.__isLockedRoom(r, c-1)):
			left = "X"
		if (self.__isValidRoom(r+1, c)):
			down = "S"
		elif(self.__isLockedRoom(r+1, c)):
			down = "X"
		if (self.__isValidRoom(r, c+1)):
			right = "D"
		elif(self.__isLockedRoom(r, c+1)):
			right = "X"
		return [up, left, down, right]


	def setLocation(self, row, column):
		self.r = row
		self.c = column

	def __isValidRoom(self, row, col):
		if ((0 <= row < self.rowCount) and (0 <= col < self.colCount) and
			 self.layout[row][col] != None and
			 not self.layout[row][col].locked):
			return True
		return False

	def __isLockedRoom(self, row, col):
		if ((0 <= row < self.rowCount) and (0 <= col < self.colCount) and
			 self.layout[row][col] != None and self.layout[row][col].locked):
			return True
		return False

	def attemptMove(self, direction):
		if (direction == 'w'):
			attRow = self.r - 1 #attempted row
			attCol = self.c #attempted col

		elif (direction == 'a'):
			attRow = self.r
			attCol = self.c - 1

		elif (direction == 's'):
			attRow = self.r + 1
			attCol = self.c

		elif (direction == 'd'):
			attRow = self.r
			attCol = self.c + 1
		elif (direction == ""):
			attRow = self.r
			attCol = self.c
		else:
			print "Bad attemptMove() input"
			return None

		self.curRoom().visited = True #Mark room being left as visited
		if (self.__isValidRoom(attRow, attCol)):
				self.setLocation(attRow, attCol)
				self.curRoom().visited = True #THIS MAKES THE MINIMAP WORK
				return self.layout[self.r][self.c] #unused
		else:
			return None



##------------------------------ Game Code ------------------------------##

#Game Initialization
[structure, inventory] = Adventure.gameInit()
raw_input("Press 'Enter' to begin: ")
GamePrint.printGame(structure, inventory)
cRoom = structure.curRoom()


#Adventure Begins!
while True:
	userInput = raw_input()
	if (userInput in ['w', 'a', 's', 'd', ""]):
		structure.attemptMove(userInput)
		cRoom = structure.curRoom()
		if (cRoom.items != []):
			itemsAdded = inventory.addItems(cRoom)
			GamePrint.printGame(structure, inventory)
			print "You obtain: "
			for i in itemsAdded:
				print "  "+i
		else:
			GamePrint.printGame(structure, inventory)
	elif (userInput == 'info' ):
		print "Currently in \"%s\"." % structure.name
		print structure.desc
	elif (userInput[:3] == 'use' or userInput[:3] == 'Use' and userInput[4:]):
		if (userInput[4:] in inventory.items):
			Adventure.tryItem(structure, inventory, userInput[4:])
		else:
			print "No %s in inventory" % userInput[4:]
	elif (userInput == 'i' and cRoom.character != None):
		Adventure.interact(structure, inventory)

# EOF