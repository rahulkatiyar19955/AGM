import xmllib, string, sys

sys.path.append('/opt/robocomp/share')
from AGGL import *

class AGMWorldModelParser(xmllib.XMLParser):
	def __init__(self, path):
		xmllib.XMLParser.__init__(self)
		self.world = False
		self.currentSymbol = None

		self.nodes = dict()
		self.links = list()

		filehandle = open(path, 'r')
		data = filehandle.read()
		filehandle.close()
		self.feed(data)

	def handle_data(self, data):
		pass

	def start_AGMModel(self, attrs):
		if not self.world:
			self.world = True
		else:
			print 'errorrr'
			sys.exit(-1)

	def end_AGMModel(self):
		if self.world:
			self.world = False
		else:
			print 'errorrr'
			sys.exit(-1)

	def start_symbol(self, attrs):
		ids = attrs['id']
		self.currentSymbol = ids
		x = ''
		if 'x' in attrs: x = attrs['x']
		y = ''
		if 'y' in attrs: y = attrs['y']
		self.nodes[ids] = AGMSymbol(ids, attrs['type'], [x, y])

	def end_symbol(self):
		self.currentSymbol = None

	def start_link(self, attrs):
		src = attrs['src']
		dst = attrs['dst']
		if not src in self.nodes:
			print 'No node', src
			sys.exit(-1)
		if not dst in self.nodes:
			print 'No node', dst
			sys.exit(-1)
		self.links.append(AGMLink(src, dst, attrs['label'], True))

	def end_link(self):
		pass

	def start_attribute(self, attrs):
		pass

	def end_attribute(self):
		pass

def graphFromXML(path):
	try:
		parser = AGMWorldModelParser(path)
		parser.close()
		return AGMGraph(parser.nodes, parser.links)
	except:
		print 'Can\'t open ' + path + '.'
		return AGMGraph(dict(), list())


