"""
	Carl Lindquist
	Jan 12, 2016

	Mapbuilder

	An interactive shell program to create an AdventureMap
"""

import printc
from Game import Structure, Room, Character
termWidth = 70

##------------------------------ Classes ------------------------------##





##------------------------------ Print Functions ------------------------------##

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

def printStructure(structure):
	clearScreen()
	print "=" * termWidth
	row = structure.r
	col = structure.c
	printMap(structure)
	print "-" * termWidth

	if structure.layout[row][col] != None:
		room = structure.layout[row][col]
		print ("[%s]" % room.name).center(termWidth)
		descLines = splitLines(termWidth - 4, room.desc)
		for l in descLines:
			if(l):
				print "  " + l
		if room.items != []:
			print "\nItems:"
			for i in room.items:
				if i:
					print " " + i
		if room.character != None:
			print "-" * termWidth
			character = room.character
			print ("[%s]" % character.name).center(termWidth)
			diaLines = splitLines(termWidth - 4, character.dialogue)
			for l in diaLines:
				if(l):
					print "  " + l
	else:
		print ("-- EMPTY --").center(termWidth)
	print "\n"
	print "=" * termWidth

def printMap(structure):
	layout = structure.layout
	minimap = [["   " for x in range(structure.colCount)] for y in range(structure.rowCount)]
	row = structure.r
	col = structure.c
	r = row
	c = col

	for row in range(len(layout)):
	 	for col in range(len(layout[row])):
	 		if layout[row][col] != None:
	 			minimap[row][col] = "[ ]" if layout[row][col].locked == False else "X X"
 			else:
 				minimap[row][col] = "   "

	if minimap[r][c] == "[ ]":
		minimap[r][c] = "[@]"
	elif minimap[r][c] == "X X":
		minimap[r][c] = "X@X"
	else:
		minimap[r][c] = " @ "

	for row in range(len(minimap)):
	 	line = ""
	 	for col in range(len(minimap[row])):
	 		line += minimap[row][col]
 		print line.center(termWidth)

##------------------------------ Control Functions ------------------------------##

def forceMove(structure, input):
	r = structure.r
	c = structure.c
	if input == 'w':
		r -= 1
		if r < 0:
			structure.layout.insert(0, [None for x in range(structure.colCount)])
			r = 0
			structure.rowCount += 1
	elif input == 'a':
		c -= 1
		if c < 0:
			for row in range(structure.rowCount):
				structure.layout[row].insert(0, None)
				c = 0
			structure.colCount += 1
	elif input == 's':
		r += 1
		if r >= structure.rowCount:
			structure.layout.append([None for x in range(structure.colCount)])
			structure.rowCount += 1
	elif input == 'd':
		c += 1
		if c >= structure.colCount:
			for row in range(structure.rowCount):
				structure.layout[row].append(None)
			structure.colCount += 1	
	structure.r = r
	structure.c = c


def chunkType(string):
	if len(string) == 0 or string[0] != '[' or string[len(string) - 1] != ']':
		return 'ERROR'
	return string[1:len(string) - 1]

def getChunk(lines):
	if lines[0][0] != '[':
		printc.red('ERROR -- Improper chunk passed.')
	ctype = chunkType(lines[0])
	tmp = 0
	while lines[tmp] != '[end ' + ctype + ']':
		tmp += 1
	return lines[1:tmp]

def makeStructureChunk(structure):
	name = structure.name
	desc = structure.desc
	layout = structure.layout

	lines = ['[structure]']
	lines.append('[name] ' + name)
	lines.append('[desc]')
	for l in splitLines(termWidth, desc):
		lines.append(l)
	lines.append('[end desc]')
	for row in range(len(layout)):
		for col in range(len(layout[row])):
			if layout[row][col] != None:
				for l in makeRoomChunk(layout[row][col], row, col):
					lines.append(l)
	lines.append('[end structure]')
	return lines

def makeRoomChunk(room, row, col):
	lines = ['[room]', '[loc] %d|%d' % (row, col) ,'[name] ' + room.name]
	lines.append('[desc]')
	for l in splitLines(termWidth, room.desc):
		lines.append(l)
	lines.append('[end desc]')
	if room.items != []:
		lines.append('[items]')
		for i in room.items:
			lines.append(i)
		lines.append('[end items]')
	if room.character != None:
		for l in makeCharacterChunk(room.character):
					lines.append(l)
	lines.append('[end room]')
	return lines

def makeCharacterChunk(character):
	lines = ['[character]', '[name] '+ character.name]
	for l in splitLines(termWidth, character.dialogue):
		lines.append(l)
	lines.append('[end character]')
	return lines

def writeChunk(chunk, file):
	for lines in chunk:
		file.write(lines + '\n')


##------------------------------ Defaults ------------------------------##

dfltDescChunk = ["[desciription]", " -- insert description here --", "[end description]"]
#dfltStrChunk = ["[structure]", " -- insert description here --", "[end description]"]


dfltStrDesc = ' -- Enter a description using your text editor --'



##------------------------------ Main Code ------------------------------##

def main():
	import sys
	clearScreen()
	print ""
	formattedPrint (termWidth, """
		Welcome the the Map Builder for Adventure! Are you sick
		and tired of building maps with nasty 'arrays' and thinking about
		indices in your head? Well no more!
		""")

	printc.blue("\nPress 'enter' to begin editing:")
	raw_input()

	with open('AdventureMap.txt') as f:
		lines = f.readlines()
	lines = [x.strip('\n') for x in lines] 


	if chunkType(lines[0]) == 'ERROR':
		printc.red(' -- Enter a description using your text editor --')
		descChunk = dfltDescChunk
	else:
		descChunk = getChunk(lines[0:])

	if '[structure]' not in lines:
		printc.blue("No structure found, would you like to create one?")
		ui = raw_input("\n\t 'y' or 'n': ")
		if ui in ['yes', 'Yes', 'y', 'Y']:
			# name = raw_input("\tEnter a name: ")
			# layout = [[None for x in range(1)] for y in range(1)]
			# structure = Structure(name, dfltStrDesc, layout)

			structureRows = 5
			structureCols = 5
			layout = [[None for x in range(structureCols)] for y in range(structureRows)] 
			layout[0][3] = Room("Hallway", """
				End of the hall. There's a door to your left, but it's locked from
				the inside. A light shuffle comes from within.
				""", [], None)
			layout[0][0] = Room("Corner", 'This WAS zero|zero', [], None, 'lock')
			layout[4][4] = Room("Corner", 'This WAS four|four', [], None, 'lock')
			layout[1][3] = Room("Hallway", "", [], None)
			layout[2][3] = Room("Hallway", "", [], None)
			layout[3][3] = Room("Hallway", "", [], None)
			layout[2][2] = Room("Bedroom", """
				Two beds, side by side. Light shines in through two windows
				in front of you.
				""", [], Character("Sam", "Hey brother!"))
			layout[0][2] = Room("Master Bedroom", """
				A big bed sits in the middle of this well decorated room. Dressers
				and boxes abound. Ginger is curled up next to the bed.
				Your mom is snoozing peacefully after a horrendously challenging row. 
				""", ["Blue Mug"], Character("Mom", "(Sleepily) Make me a cup of tea?"), 'lock')
			layout[4][3] = Room("Living Room", """
				A grand old room with a fireplace. Large
				wooden beams cross over your head. A piano blocks a large 
				window. The fireplace looks workable. A dog stands
				guard by the door.
				""", ["Ripstick"], Character("Ginger", "Woof"))
			layout[1][4] = Room("Kitchen", """
				A small kitchen with blue tile countertops.
				""", ["Matches", "Knife"], None)
			structure = Structure("The House", "3516", layout)
			structure.r = 3
			structure.c = 2


			while(True):
				printStructure(structure)
				ui = raw_input()
				if ui == 'quit':
					break
				elif ui in ['w', 'a', 's', 'd']:
					forceMove(structure, ui)
				
		else:
			sys.exit()

	outfile = open("MAPP.txt", "w+")

	writeChunk(descChunk, outfile)
	writeChunk(makeStructureChunk(structure), outfile)
	







if __name__ == "__main__":
	main()
