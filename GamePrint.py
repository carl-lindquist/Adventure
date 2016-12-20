"""
	Carl Lindquist
	Dec 19, 2016

	Library to print the status of a game(currently called Adventure)
	to the terminal.
"""




def clearScreen():
	import os
	os.system('cls' if os.name == 'nt' else 'clear')

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

def printGame(structure, inventory):
	from Game import Inventory, Character, Room, Structure
	lineWidth = 70
	room = structure.curRoom()
	character = room.character


	print "-" * lineWidth

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

		for l in diaLines[len(inventory.items)+1:]:
			if (l):
				print " " * (inventory.width + 4) + l
	else:
		for l in invLines:
			print l
	print "-" * lineWidth





