#Python Game


def clearScreen():
	import os
	os.system('cls' if os.name == 'nt' else 'clear')


class Character(object):

	def __init__(self, name, dialogue):
		self.name = name
		self.dialogue = dialogue


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

	def printRoom(self):
		lineWidth = 68

		r = self.r
		c = self.c
		up, down, left, right = ' ', ' ', ' ', ' '
		if (self.__isValidRoom(r-1, c)):
			up = "W"
		if (self.__isValidRoom(r, c-1)):
			left = "A"
		if (self.__isValidRoom(r+1, c)):
			down = "S"
		if (self.__isValidRoom(r, c+1)):
			right = "D"

		print "-" * lineWidth
		if (self.curRoom().visited):
			print " ----------- " + ("[%s]" % self.curRoom().name).center(lineWidth - 13)
		else:
			print " ----------- " + ("{%s}" % self.curRoom().name).center(lineWidth - 13)
		if (self.curRoom().desc != None):
			print "|    |%s|    |  " %up + self.curRoom().desc[0]
			print "| |%s|   |%s| |  " %(left, right) + self.curRoom().desc[1]
			print "|    |%s|    |  " %down + self.curRoom().desc[2]
		else:
			print "|    |%s|    |  " %up
			print "| |%s|   |%s| |  " %(left, right)
			print "|    |%s|    |  " %down
		print " ----------- "
		print "-" * lineWidth

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

		clearScreen()
		self.curRoom().visited = True
		if (self.__isValidRoom(attRow, attCol)):
				self.setLocation(attRow, attCol)
				return self.layout[self.r][self.c]
		else:
			return None
	

# the Init

building = [[None for x in range(5)] for y in range(5)] 

sam = Character("Sam", "  Hey brother")

r = Room("Bedroom", [
		 "Two beds side by side.",
		 "",
		 ""],
		 None, sam)

building[2][2] = r

building[0][3] = Room("Hallway", None, None, None)
building[1][3] = Room("Hallway", None, None, None)
building[2][3] = Room("Hallway", None, None, None)
building[3][3] = Room("Hallway", None, None, None)

ginger = Character("Ginger", "  Rrraow")

building[4][3] = Room("Living Room", [
 					  "A grand room with a fireplace.",
 					  "",
 					  ""],
 					  ["Ripstick"],
 					   ginger)

building[1][4] = Room("Kitchen", [
 					  "A small kitchen with blue tile countertops.",
 					  "",
 					  ""],
 					  ["Matches"],
 					   None)

inventory = []


home = Structure("House", "3516", building)

home.setLocation(2, 2)


#The Game
clearScreen()
while True:
	cRoom = home.curRoom()
	home.printRoom()

	if (cRoom.character != None):
		print "|%s|" % cRoom.character.name
		print cRoom.character.dialogue

	if (cRoom.items != None):
		print "You obtain:"
		for i in cRoom.items:
			print "  " + i
		inventory += cRoom.items

	#print "Direction (wasd): "
	input = 0
	while (True):
		input = raw_input()
		if (input in ['w', 'a', 's', 'd']):
			home.attemptMove(input)
			break
		elif (input == 'info' ):
			print "Currently in a %s." % cRoom.name
		else:
			print "Pick another way: "















