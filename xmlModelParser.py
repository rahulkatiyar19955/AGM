import libxml2

from AGGL import *


def graphFromXML(path):
	# Initialize empty graph
	nodes = dict()
	links = list()
	# Open XML
	try:
		file = open(path, 'r')
	except:
		print 'Can\'t open ' + path + '.'
		return AGMGraph(dict(), list())
	data = file.read()
	xmldoc = libxml2.parseDoc(data)
	root = xmldoc.children
	if root is not None:
		nodes, links = parseRoot(root, nodes, links)
	xmldoc.freeDoc()
	return AGMGraph(nodes, links)


def parseRoot(root, nodes, links):
	if root.type == "element" and root.name == "AGMModel":
		child = root.children
		while child is not None:
			if child.type == "element":
				if child.name == "symbol":
					nodes, links = parseSymbol(child, nodes, links)
				elif child.name == "link":
					nodes, links = parseLink(child, nodes, links)
				else:
					print "error: "+str(child.name)
			child = child.next
	return nodes, links


def parseSymbol(root, nodes, links):
	if root.type == "element" and root.name == "symbol":
		# props
		child = root.children
		idens = parseSingleValue(root,   'id')
		types = parseSingleValue(root, 'type')
		x = 0
		xs = parseSingleValue(root, 'x', False)
		if xs != None:
			x = int(xs)
		y = 0
		ys = parseSingleValue(root, 'y', False)
		if ys != None:
			y = int(ys)
		nodes[idens] = AGMSymbol(idens, types, [int(x), int(y)])
		# children
		while child is not None:
			if child.type == "element":
				if child.name == "attribute":
					#parseAttribute(child, component)
					pass
				else:
					print 'boooooooooo'
			child = child.next
	else:
		print 'parseSymbol with no symbol element'
	return nodes, links


def parseLink(root, nodes, links):
	if root.type == "element" and root.name == "link":
		# props
		child = root.children
		src = parseSingleValue(root, 'src')
		dst = parseSingleValue(root, 'dst')
		lab = parseSingleValue(root, 'label')
		links.append(AGMLink(src, dst, lab, True))
		# children
		while child is not None:
			if child.type == "element":
					print 'boooooooooo'
			child = child.next
	else:
		print 'parseLink with no link element'
	return nodes, links


def parseSingleValue(node, arg, doCheck=True):
	if not node.hasProp(arg) and doCheck: print 'WARNING: ' + arg + ' attribute expected'
	else:
		ret = node.prop(arg)
		node.unsetProp(arg)
		return ret

