"""
	Carl Lindquist
	Jan 12, 2016

	Mapbuilder

	An interactive shell program to create an AdventureMap
"""

import GamePrint
from Game import Structure, Room, Character
termWidth = GamePrint.lineWidth
descWidth = termWidth - 25

UP = 'w'
LEFT = 'a'
DOWN = 's'
RIGHT = 'd'

EXIT = 'exit'
NEW_ROOM = 'r'

INDENT = '  '

startSplash = """
  __  __             ____        _ _     _             
 |  \/  | __ _ _ __ | __ ) _   _(_) | __| | ___ _ __  
 | |\/| |/ _` | '_ \|  _ \| | | | | |/ _` |/ _ \ '__| 
 | |  | | (_| | |_) | |_) | |_| | | | (_| |  __/ |    
 |_|  |_|\__,_| .__/|____/ \__,_|_|_|\__,_|\___|_|    
              |_|                                      
    """
startText = """
	Welcome the the Map Builder for Adventure! Are you sick
	and tired of building maps with nasty 'arrays' and thinking about
	indices in your head? Well no more!
	"""

controls = ["""'wasd'   move in desired direction""",
	        """   'r'   create/edit room""",
	        """'exit'   exit mapbuilder"""
]


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


"""
[desc]	Prints a depiction of an Adventure map. Showing
		rooms, their locked/unlocked status, and the current
		room's characters/items

[structure] Structure to be printed
"""
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

"""
[desc]	Prints just the map for a given structure. Shows rooms
		regardless of visitation.

[structure] Structure to be printed
"""
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

"""
[desc]	Calls printStructure(). Then prints controls
		for navigating the MapBuilder

[structure] Structure to be printed
"""
def printNavigation(structure):
	printStructure(structure)
	print 'Navigation Controls:'.center(termWidth)
	print """ 'wasd' to move --- 'r' enter Room Editor""".center(termWidth)
	print """ 'exit' leave MapBuilder""".center(termWidth)
	print '+' * termWidth

"""
[desc]	Calls printStructure(). Then prints controls
		for editing the current room.

[structure] Structure to be printed
"""
def printRoomEditor(structure):
	printStructure(structure)
	print 'Room Editor Controls:'.center(termWidth)
	print """'[n]' name --- '[d]' description""".center(termWidth)
	print """'[i]' item editor --- '[c]' charater editor --- '[l]' lock/unlock""".center(termWidth)
	print """'[delete]' remove room --- '[exit]' exit to navigation""".center(termWidth)
	print '+' * termWidth

"""
[desc]	Calls printStructure(). Then prints controls
		for editing the current items in a room.

[structure] Structure to be printed
"""
def printItemEditor(structure):
	printStructure(structure)
	print 'Item Editor Controls:'.center(termWidth)
	print """'[add] Item' add item --- '[del] Item' delete item""".center(termWidth)
	print """'[exit]' exit to Room Editor""".center(termWidth)
	print '+' * termWidth

"""
[desc]	Calls printStructure(). Then prints controls
		for editing the current character in a room.

[structure] Structure to be printed
"""
def printCharacterEditor(structure):
	printStructure(structure)
	print 'Character Editor Controls:'.center(termWidth)
	print """'[name] Name' change name --- '[d] dialogue' change static dialogue""".center(termWidth)
	print """'[delete]' remove character --- '[exit]' exit to Room Editor""".center(termWidth)
	print '+' * termWidth


##------------------------------ Control Functions ------------------------------##

def forceMove(structure, input):
	r = structure.r
	c = structure.c
	if input == UP:
		if all(r==structure.rowCount-1 and structure.layout[r][col] == None for col in range(structure.colCount)):
			structure.layout.pop() #remove empty row when leaving
			structure.rowCount -= 1
		r -= 1
		if r < 0: #entering an empty row
			structure.layout.insert(0, [None for x in range(structure.colCount)])
			r = 0
			structure.rowCount += 1

	elif input == LEFT:
		if all(c==structure.colCount-1 and structure.layout[row][c] == None for row in range(structure.rowCount)):
			for row in range(structure.rowCount):
				structure.layout[row].pop()
			structure.colCount -= 1
		c -= 1
		if c < 0:
			for row in range(structure.rowCount):
				structure.layout[row].insert(0, None)
				c = 0
			structure.colCount += 1

	elif input == DOWN:
		if all(r==0 and structure.layout[r][col] == None for col in range(structure.colCount)):
			structure.layout.pop(0) #remove empty row when leaving
			structure.rowCount -= 1
			r = -1
		r += 1
		if r >= structure.rowCount:
			structure.layout.append([None for x in range(structure.colCount)])
			structure.rowCount += 1

	elif input == RIGHT:
		if all(c==0 and structure.layout[row][c] == None for row in range(structure.rowCount)):
			for row in range(structure.rowCount):
				structure.layout[row].pop(0)
			structure.colCount -= 1
			c = -1
		c += 1
		if c >= structure.colCount:
			for row in range(structure.rowCount):
				structure.layout[row].append(None)
			structure.colCount += 1	
	structure.r = r
	structure.c = c

def roomEditor(structure):
	room = structure.layout[structure.r][structure.c]
	ui = 'arb' #arbitrary init value
	while ui not in ['[exit]', '[exit']:
		if ui in ['[n]', '[d]', '[i]', '[c]', '[l]', 'arb'] and room == None:
			room = Room(' -- No Room Name -- ', ' -- No Description --', [], None)
			structure.layout[structure.r][structure.c] = room
		if ui == '[n]':
			room.name = raw_input("Enter a name: ")
		elif ui == '[d]':
			room.desc = raw_input("Enter a description, or add one in AdventureMap.txt: \n")
		elif ui == '[i]':
			itemEditor(structure)
		elif ui == '[c]':
			characterEditor(structure)
		elif ui == '[l]':
			room.locked = not room.locked
		elif ui == '[delete]':
			room = None

		structure.layout[structure.r][structure.c] = room
		printRoomEditor(structure)
		ui = raw_input()

def itemEditor(structure):
	printItemEditor(structure)
	ui = raw_input()
	items = structure.layout[structure.r][structure.c].items
	while ui != '[exit]':
		if ui[0:5] == '[add]':
			items.append(ui[6:])
		if ui[0:5] == '[del]':
			items.remove(ui[6:])

		structure.layout[structure.r][structure.c].items = items
		printItemEditor(structure)
		ui = raw_input()

def characterEditor(structure):
	c = structure.layout[structure.r][structure.c].character
	ui = 'arb' #arbitrary init value
	while ui not in ['[exit]', '[exit']:
		if c == None:
			c = Character(' -- No Character Name -- ', ' -- No Dialogue --')
			structure.layout[structure.r][structure.c].character = c
		if ui[0:6] == '[name]':
			c.name = ui[7:]
		elif ui[0:3] == '[d]':
			c.dialogue = ui[4:]
		elif ui == '[delete]':
			c = None
			structure.layout[structure.r][structure.c].character = c
			break

		structure.layout[structure.r][structure.c].character = c
		printCharacterEditor(structure)
		ui = raw_input()



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

def makeDescChunk(descChunk):
	desc = ['[description]']
	for l in descChunk:
		desc.append(INDENT +' '+l)
	desc.append('[end description]')
	return desc

def makeStructureChunk(structure):
	name = structure.name
	desc = structure.desc
	layout = structure.layout

	lines = ['']
	lines.append('[structure]')
	lines.append(INDENT + '[name] ' + name)
	lines.append(INDENT + '[desc]')
	for l in splitLines(descWidth, desc):
		lines.append((INDENT*2) + l)
	lines.append(INDENT + '[end desc]')
	for row in range(len(layout)):
		for col in range(len(layout[row])):
			if layout[row][col] != None:
				for l in makeRoomChunk(layout[row][col], row, col):
					lines.append(l)
	lines.append('[end structure]')
	return lines

def makeRoomChunk(room, row, col):
	lines = ['']
	lines.append(INDENT+'[room]')
	lines.append((INDENT*2)+'[name] ' + room.name)
	lines.append((INDENT*2)+'[location] %d %d' % (row, col))
	lines.append((INDENT*2)+'[desc]')
	for l in splitLines(descWidth, room.desc):
		lines.append((INDENT*3)+l)
	lines.append((INDENT*2)+'[end desc]')
	if room.items != []:
		lines.append((INDENT*2)+'[items]')
		for i in room.items:
			lines.append((INDENT*3)+i)
		lines.append((INDENT*2)+'[end items]')
	if room.character != None:
		for l in makeCharacterChunk(room.character):
					lines.append(l)
	if room.locked:
		lines.append((INDENT*2)+'[lock]')
	lines.append(INDENT+'[end room]')
	return lines

def makeCharacterChunk(character):
	lines = [(INDENT*2)+'[character]']
	lines.append((INDENT*3)+'[name] '+ character.name)
	for l in splitLines(descWidth, character.dialogue):
		lines.append((INDENT*4)+l)
	lines.append((INDENT*2)+'[end character]')
	return lines

def writeChunk(chunk, file):
	for lines in chunk:
		file.write(lines + '\n')

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



def loadStructure():
	with open('AdventureMap.txt') as f:
		mapFile = f.readlines()
	mapFile = [x.strip() for x in mapFile] 

	count = 0
	for l in mapFile:
		if l == '[structure]':
			break
		count +=1
	strChunk = getChunk(mapFile[count:]) #isolate structure chunk

	layout = [[None for x in range(1)] for y in range(1)]
	structure = Structure('-- No Structure Name --', '', layout)
	structure.name = strChunk[0][7:]
	for l in getChunk(strChunk[1:]):
		structure.desc += " "+l
	
	count = 0
	for l in strChunk:
		if l == '[room]':
			loadRoom(structure, getChunk(strChunk[count:]))
		count += 1

	return structure

def loadRoom(structure, roomChunk):
	room = Room('', '', [], None)
	room.name = roomChunk[0][7:]
	r = ''
	c = ''
	for chars in roomChunk[1][11:]:
		r += chars
		if chars == ' ':
			break
	for chars in roomChunk[1][len(r)+11 :]:
		c += chars
	r = int(r)
	c = int(c)
	for l in getChunk(roomChunk[2:]):
		room.desc += " "+l
	if '[lock]' in roomChunk:
		room.locked = True
	count = 0
	for l in roomChunk:
		if l == '[character]':
			charChunk = getChunk(roomChunk[count:])
			room.character = loadCharacter(charChunk)
			break;
		elif l == '[items]':
			itemChunk = getChunk(roomChunk[count:])
			room.items.extend(itemChunk)
		count += 1
	expandStructure(structure, r, c)
	structure.layout[r][c] = room

def loadCharacter(charChunk):
	character = Character('', '')
	character.name = charChunk[0][7:]
	for l in charChunk[1:]:
		character.dialogue += " "+l
	return character

def expandStructure(structure, row, col):
	while structure.rowCount <= row:
		structure.layout.append([None for x in range(structure.colCount)])
		structure.rowCount += 1
	while structure.colCount <= col:
		for r in range(structure.rowCount):
			structure.layout[r].append(None)
		structure.colCount += 1


##------------------------------ Main Code ------------------------------##

def main():
	GamePrint.printStart(startSplash, startText, controls)
	print "\n\tPress 'enter' to begin editing:"
	raw_input()

	with open('AdventureMap.txt', 'r') as f:
		lines = f.readlines()
	lines = [x.strip() for x in lines] 

	if lines == [] or chunkType(lines[0]) != 'description':
		descChunk = ['-- insert description here --']
	else:
		descChunk = getChunk(lines[0:])
	if '[structure]' not in lines:
		print "No structure found, have fun building a map from scratch!"
		name = raw_input("\tEnter a name for your structure: ")
		layout = [[None for x in range(1)] for y in range(1)]
		structure = Structure(name, '-- insert description here --', layout)	
	else:
		structure = loadStructure()


	while(True):
		printNavigation(structure)
		ui = raw_input()
		if ui == EXIT:
			break
		elif ui in [UP, LEFT, DOWN, RIGHT]:
			forceMove(structure, ui)
		elif ui == NEW_ROOM:
			roomEditor(structure)


	outfile = open("AdventureMap.txt", "w+")
	writeChunk(makeDescChunk(descChunk), outfile)
	writeChunk(makeStructureChunk(structure), outfile)
	outfile.close()
	



if __name__ == "__main__":
	main()





