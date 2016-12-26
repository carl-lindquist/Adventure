"""
	Carl Lindquist
	Dec 19, 2016

	## Include this file in the same directory as Game.py and Adventure.py ##
	
	A library containing all the print methods to display the state of an
	"Adventure" game to the terminal.
"""


lineWidth = 60 #Designer Parameter to set up terminal width

def clearScreen():
	import os
	os.system('cls' if os.name == 'nt' else 'clear')

"""
[desc]	Splits text into lines up to a specified length

[length] Maximum line length
[text] Text to be split

[ret]	List of strings
"""
def splitLines(length, text):
	words = text.split()
	lines = [""]
	lNum = 0

	for w in words:
		if (len(lines[lNum]) + len(w) + 1 <= length):
			lines[lNum] += " "+w
		else:
			lines.append("")
			lNum += 1
			lines[lNum] += " "+w

	while(len(lines) <10): #guarantees enough lines for printGame
		lines.append("")

	return lines


"""
[desc]	Prints text in lines up to length. Also removes whitespace/newlines

[length] Maximum line length
[text] Text to be printed

"""
def formattedPrint(length, text):
	if (text):
		lines = splitLines(length, text)
		for l in lines:
			if l:
				print " " + l


"""
[desc]	Complex print function to display the current state of an 
		"Adventure" game.

[args]	Structure and Inventory to gather information about the
		current game-state from
"""
def printGame(structure, inventory):
	clearScreen()
	from Game import Inventory, Character, Room, Structure

	room = structure.curRoom()
	character = room.character


	print "=" * lineWidth
	printMinimap(structure)
	print "-" * lineWidth + '\n'

	descLines = splitLines(lineWidth - 15, room.desc)
	[up, left, down, right] = structure.availableMoves()
	if (room.visited):
		print " ----------- " + ("[%s]" % room.name).center(lineWidth - 13)
	else:
		print " ----------- " + ("{{%s}}" % room.name).center(lineWidth - 13)
	print "|    |%s|    |  " %up + descLines[0]
	print "| |%s|   |%s| |  " %(left, right) + descLines[1]
	print "|    |%s|    |  " %down + descLines[2]
	print " -----------   " + descLines[3]
	for l in descLines[4:]:
		if(l):
			print " "*15 + l
	print ""


	invLines = inventory.printLines()
	if(character != None):
		dialogue = character.dialogue
		diaLines = splitLines(lineWidth - inventory.width - 5, dialogue)

		print invLines[0] + "   " + character.name + ":"

		lNum = 0
		for l in invLines[1:]:
			print l + "  " + diaLines[lNum]
			lNum += 1

		for l in diaLines[len(inventory.items) + 2:]:
			if (l):
				print " " * (inventory.width + 4) + l
	else:
		for l in invLines:
			print l
	print "=" * lineWidth




def printMinimap(structure):
	layout = structure.layout
	minimap = [["   " for x in range(structure.colCount)] for y in range(structure.rowCount)]
	r = structure.r
	c = structure.c

	#TEMPORARY REMASKING, availableMoves will be changed next commit
	[up, left, down, right] = structure.availableMoves()
	if up == 'W':
		minimap[r-1][c] = ' ^ '
	elif up == 'X':
		minimap[r-1][c] = ' X '

	if left == 'A':
		minimap[r][c-1] = ' < '
	elif left == 'X':
		minimap[r][c-1] = ' X '

	if down == 'S':
		minimap[r+1][c] = ' v '
	elif down == 'X':
		minimap[r+1][c] = ' X '

	if right == 'D':
		minimap[r][c+1] = ' > '
	elif right == 'X':
		minimap[r][c+1] = ' X '


	for row in range(len(layout)):
	 	for col in range(len(layout[row])):
	 		if layout[row][col] != None and layout[row][col].visited:
	 			minimap[row][col] = "[ ]"

	minimap[r][c] = "[@]"

	for row in range(len(minimap)):
	 	line = ""
	 	for col in range(len(minimap[row])):
	 		line += minimap[row][col]
 		print line.center(lineWidth)


def printWin(text):
	print "" 
	print "-" * lineWidth
	print """
    __   __                           _         _ 
    \ \ / /                          (_)       | |
     \ V /   ___   _   _   __      __ _  _ __  | |
      \ /   / _ \ | | | |  \ \ /\ / /| || '_ \ | |
      | |  | (_) || |_| |   \ V  V / | || | | ||_|
      \_/   \___/  \__,_|    \_/\_/  |_||_| |_|(_)
	"""
	print ""
	formattedPrint(lineWidth - 20, text)
	print ""

def printLose(text):
	print "" 
	print "-" * lineWidth
	print """
    __   __                  _                    _ 
    \ \ / /                 | |                  | |
     \ V /   ___   _   _    | |  ___   ___   ___ | |
      \ /   / _ \ | | | |   | | / _ \ / __| / _ \| |
      | |  | (_) || |_| |   | || (_) |\__ \|  __/|_|
      \_/   \___/  \__,_|   |_| \___/ |___/ \___|(_)                                         
	"""
	print ""
	formattedPrint(lineWidth - 20, text)
	print ""

def printStart(title, text):
	clearScreen()
	print title

	print "-" * lineWidth
	print ""
	formattedPrint(lineWidth - 20, text)
	print ""

	print "Controls:"
	print "        'wasd'   move in desired direction"
	print "  'use <item>'   use an item in your inventory"
	print "           'i'   interact with a character"
	print "        'info'   print the name of the current structure"
	
	print ""
	print ""











