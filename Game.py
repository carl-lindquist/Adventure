#Python Game

import GamePrint

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

	def addItems(self, items):
		for i in items:
			if len(self.items) < self.maxSize:
				self.items.append(i)

	def removeItem(self, item):
		self.items.remove(item)


	def printLines(self):
		self.width = len(self.name) + 4
		for i in self.items:
			if (len(i) > self.width):
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
		if (self.__isValidRoom(r, c-1)):
			left = "A"
		if (self.__isValidRoom(r+1, c)):
			down = "S"
		if (self.__isValidRoom(r, c+1)):
			right = "D"
		return [up, left, down, right]


	def setLocation(self, row, column):
		self.r = row
		self.c = column

	def __isValidRoom(self, row, col):
		if ((0 <= row < self.rowCount) and (0 <= col < self.colCount) and
			 self.layout[row][col] != None):
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
		else:
			print "Bad attemptMove() input"
			return None

		GamePrint.clearScreen()
		self.curRoom().visited = True
		if (self.__isValidRoom(attRow, attCol)):
				self.setLocation(attRow, attCol)
				return self.layout[self.r][self.c]
		else:
			return None





# the Init

building = [[None for x in range(5)] for y in range(5)] 

sam = Character("Sam", "  Hey brother")

building[2][2] = Room("Bedroom", """
	Two beds, side by side. Light shines in through two windows
	in front of you.
""", None, sam)

building[0][3] = Room("Hallway", "", ["Gargantuan Orangutan"], Character("Gargantuan Orangutan", "Gigantopithicus"))
building[1][3] = Room("Hallway", "", None, None)
building[2][3] = Room("Hallway", "", None, None)
building[3][3] = Room("Hallway", "", None, None)

ginger = Character("Ginger", "  Rrraow")

building[4][3] = Room("Living Room", """
	A grand old room with a fireplace. Large
	wooden beams cross over your head. A piano stands by 
	a window. The fireplace looks used...recently.
""", ["Ripstick"], ginger)

building[1][4] = Room("Kitchen", """
	A small kitchen with blue tile countertops.
""",
	["Matches"], None)

inventory = Inventory("Satchel", 5)


home = Structure("The House", "3516", building)

home.setLocation(2, 2)
cRoom = home.curRoom()



#The Game
GamePrint.clearScreen()
while True:

	GamePrint.printGame(home, inventory)

	if (cRoom.items != None and not cRoom.visited):
 		print "You obtain:"
		for i in cRoom.items:
			print "  " + i


	while (True):
		input = raw_input()
		if (input in ['w', 'a', 's', 'd']):
			home.attemptMove(input)
			cRoom = home.curRoom()
			if (cRoom.items != None and not cRoom.visited):
				inventory.addItems(cRoom.items)
			break
		elif (input == 'info' ):
			print "Currently in %s." % home.name
			print home.desc
			print "Inventory: " + str(inventory)
		else:
			print "Pick another way: "















