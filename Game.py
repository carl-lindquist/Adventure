#Python Game shell

import GamePrint, Adventure

class Character(object):

	def __init__(self, name, dialogue):
		self.name = name
		self.dialogue = dialogue

class Inventory(object):

	def __init__(self, name, size):
		self.name = name
		self.maxSize = size
		self.items = []
		self.width = 0

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
		for i in self.items:
			if (len(i) > self.width - 4):
				self.width = len(i) + 4

		lines = []
		lines.append("/"+self.name.center(self.width)+"\\")
		lines.append("|"+"-"*(self.width)+"|")
		for i in self.items:
			lines.append("|  "+i.ljust(self.width - 2)+"|")
		lines.append("\\"+ "_" * (self.width) + "/")
		return lines


class Room(object):

	def __init__(self, name, description, items, character):
		self.name = name
		self.desc = description
		self.items = items
		self.character = character
		self.visited = False
		self.state = 0
		self.locked = False


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
			attRow = self.r - 1
			attCol = self.c

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

		self.curRoom().visited = True
		if (self.__isValidRoom(attRow, attCol)):
				self.setLocation(attRow, attCol)
				return self.layout[self.r][self.c]
		else:
			return None



#Init
[structure, inventory] = Adventure.gameInit()
raw_input("Press 'Enter' to begin: ")
GamePrint.printGame(structure, inventory)
cRoom = structure.curRoom()


#The Game
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
	elif (userInput == 'i'):
		Adventure.interact(structure, inventory)
	else:
		print "Bad input"

















