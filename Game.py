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
		lineWidth = 69 #width of text box
		words = self.curRoom().desc.split()
		descLines = []
		lNum = 0

		for l in range(10): #max number of descriptions lines (limited for style)
			descLines.append("")

		for w in words:
			if (len(descLines[lNum]) + len(w) + 1 <= lineWidth - 15):
				descLines[lNum] += " "+w
			else:
				lNum += 1
				descLines[lNum] += " "+w

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
			print " ----------- " + ("{{%s}}" % self.curRoom().name).center(lineWidth - 13)
		print "|    |%s|    |  " %up + descLines[0]
		print "| |%s|   |%s| |  " %(left, right) + descLines[1]
		print "|    |%s|    |  " %down + descLines[2]
		print " -----------   " + descLines[3]
		for l in descLines[4:]:
			if(l):
				print " "*15 + l
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

building[2][2] = Room("Bedroom", """
	Two beds, side by side. Light shines in through two windows
	in front of you.
""", None, sam)

building[0][3] = Room("Hallway", "", None, None)
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

inventory = []


home = Structure("The House", "3516", building)

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
			print "Currently in %s." % home.name
			print home.desc
		else:
			print "Pick another way: "















