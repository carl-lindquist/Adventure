"""
	Carl Lindquist
	Oct 17, 2017

	A chunk is a silly little block of text which can contain class
	information in a text file for simulating persistent memory. Sort of
	like a very generic config file.

	Chunks can contain any number of subchunks.

"""

import re
chunk_pattern = re.compile("\[(?!~)(.*?)\]")
chunk_end_pattern = re.compile("\[~(.*?)\]")
data_pattern = re.compile("{(?!~)(.*?)}")
data_end_pattern = re.compile(("{~(.*?)}"))


class Chunk(object):

	# I should contain a dictionary of members to access by string
	# that way anybody can ask for implementation specific things real easy
	tab = "   "

	def __init__(self, stream=None, file=None):
		self.data = {}
		self.subchunks = []
		self.type = type

		if file != None:
			with open(file) as f:
				stream = f.readlines()
				stream = [l.rstrip() for l in stream]

		try:
			self.type = chunk_pattern.search(stream[0]).group(1)
		except IndexError as e1:
			raise "Improperly formatted chunk stream while parsing chunk type."
		except AttributeError as e2:
			print "Warning:: Called with type set to none, and there was no name to parse."

		self.lines_consumed = self._load_chunks(stream[1:]) # start processing after type line


	def _tree(self):
		l = []
		l.append("%s[%s] \n" % ('='*len(self.tab), self.type)) # print my type

		for key, value in self.data.items(): # print my data
			l.append( self.tab + "| %s: %s\n" % (key, value) )

		# these guys don't end with a newline because they already have them recursively
		for c in self.subchunks:
			l.append( self.tab + "|\n" ) # just a spacer
			for i in c._tree():
				l.append("%s|" % self.tab + i) # append the subchunks

		return l


	def __str__(self):
		return''.join(self._tree())


	def _load_data(self, stream):
		data_re = data_pattern.search(stream[0])
		self.data[data_re.group(1)] = "" # store the name
		i = 1
		while i < len(stream) and data_end_pattern.search(stream[i]) == None: # fill out this data member
			self.data[data_re.group(1)] += stream[i].lstrip()
			i += 1

		return i


	def _load_chunks(self, stream):
		i = 0
		while (i < len(stream)):
			chunk_re = chunk_pattern.search(stream[i])
			data_re = data_pattern.search(stream[i])
			chunk_end_re = chunk_end_pattern.search(stream[i])

			if data_re != None: # you found a new data member
				i += self._load_data(stream[i:]) + 1
				continue # re-initialize pattern recognizers at new i

			if chunk_re != None: # you found a new chunk
				self.subchunks.append(Chunk(stream=stream[i:])) # add to your subchunks
				i += self.subchunks[-1].lines_consumed + 1 # add the number of lines that subchunk consumed

				continue

			if chunk_end_re != None and chunk_end_re.group(1) == self.type: # you found the end of your chunk
				return i + 1 # return the number of lines you consumed

			if chunk_end_re != None and chunk_end_re.group(1) != self.type: # you found the end of another chunk
				print "Warning:: Improper Format. Found chunk end \'%s\' while parsing \'[%s]\'." % (stream[i].strip(), self.type)
				return i
				
			i += 1

		return i


"""
[structure]
  {name} Insane Temple
  {desc}
     -- insert description here --
  {/desc}

  [room]
    [name] So this is a great place
    [location] 0 0
    [desc]
       -- No Description --
    [/desc]
  [/room]

  [room]
    [name] The Start
    [location] 1 0
    [desc]
       -- No Description --
    [/desc]
  [/room]
[/structure]


"""


"""
[structure]
	{name}
		Carl
	{foo}
		bare bear beer bar bore bore 
		score scar scare
	[room]
		[character]
			someshit


"""


	





