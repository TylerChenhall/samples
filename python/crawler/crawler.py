import urllib.request
from html.parser import HTMLParser

#Parses a search page and stores new links relevant to the search
class MySearchPageParser(HTMLParser):
	def __init__(self, todo, processed):
		HTMLParser.__init__(self)
		self.todo = todo
		self.processed = processed
	
	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			url = ''
			for x in attrs:
				if (x[0] == 'href'):
					url = x[1]
					
			if( ('/search/' in url or '/info/' in url) and (url not in processed) and (url not in todo) ):
				todo.append(url)

	def handle_endtag(self, tag):
		pass
	def handle_data(self, data):
		pass
		
#Parses an info page, collects and stores information
#The logic implemented in this code represents specific strategies identified for capturing the desired information.  It is very specific to the current layout of the directory html pages right now
class MyInfoPageParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.name = ''
		self.nRecord = False
		self.major= ''
		self.mRecord = False
		self.email= ''
		self.eRecord = False
		self.address=''
		self.aRecord = False
		self.phone=''
		self.pRecord = False
		
	def handle_starttag(self, tag, attrs):
		if (tag == 'noscript'): #The only noscript tag is before the email address
			self.eRecord = True
		elif (tag == 'h1'):
			self.nRecord = True
		elif (tag == 'a'):
			self.aRecord = False
			if ('tel' in attrs[0][1] and self.address != ''):
				self.pRecord = True
			#TODO: check if it is the tel tag
	def handle_endtag(self, tag):
		if (tag == 'h1'):
			self.nRecord = False
			parts = self.name.split(', ')
			self.name = parts[1] + ' ' + parts[0]
		elif (tag == 'div'):
			self.aRecord = False
	def handle_data(self, data):
		if (self.eRecord):
			self.email = data.replace(' (at) ', '@').replace(' (dot) ','.')
			self.eRecord = False
		elif (self.nRecord):
			self.name = self.name + data
		elif (self.mRecord):
			self.major = data
			self.mRecord = False	
		elif (self.aRecord):
			self.address = self.address + data + ' '
		elif (self.pRecord):
			self.phone = data
			self.pRecord = False
		elif ('Major:' in data):
			self.mRecord = True
		elif ('In-Session Address' in data):
			self.aRecord = True

#Process a single search or info url
def process(url):
	todo.remove(url)
	processed.append(url)
	#print('http://info.iastate.edu' + url)
	#print(url)
	if ('http://info.iastate.edu' not in url):
		url = 'http://info.iastate.edu' + url
	
	wpage = urllib.request.urlopen(url)
	
	if ('search' in url):
		parser = MySearchPageParser(todo, processed)
		parser.feed(wpage.read().decode("utf-8")) #The decode statement converts from bytes to string
		parser.close()
	else:
		parser = MyInfoPageParser()
		parser.feed(wpage.read().decode("utf-8"))
		parser.close()
		ppl_info[parser.name] = {'Name':parser.name, 'Major':parser.major, 'Email':parser.email, 'Address':parser.address, 'Phone #':parser.phone}




#
# A simple web crawler for the Iowa State Student Directory
#
# Currently, it just creates a dictionary of people entries, printing the length
#
print('Begin Query')

# Decide the search query
query = input('Enter a query: ')
query = query.strip().replace(" ","+") #Trim whitespace around the string and turn interior spaces to +
# TODO: replace space characters with + signs

ppl_info = {}
processed = []
todo = []

# Download the first page for the query
page = urllib.request.urlopen('http://info.iastate.edu/individuals/search/' + query)

todo.append( page.geturl() )
while( len(todo) != 0 ):
	process(todo[-1])
	
print('End Query')
print('Number of Entries Collected: ' + str(len(ppl_info)))
#print(ppl_info)

		
