import sys, os, Ice
# Check that RoboComp has been correctly detected
ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	pass
if len(ROBOCOMP)<1:
	print 'ROBOCOMP environment variable not set! Exiting.'
	sys.exit()

preStr = "-I"+ROBOCOMP+"/Interfaces/ --all "+ROBOCOMP+"/Interfaces/"
Ice.loadSlice(preStr+"AGMWorldModel.ice")
import RoboCompAGMWorldModel

# AGM
sys.path.append('/usr/local/share/agm')
from AGGL import *

def fromInternalToIce(src):
	# Create new model
	dst = RoboCompAGMWorldModel.World([], [])
	# Copy indices
	for nodeSrc in src.nodes.values():
		nodeDst = RoboCompAGMWorldModel.Node()
		nodeDst.nodeType = nodeSrc.sType
		nodeDst.nodeIdentifier = int(nodeSrc.name)
		if nodeDst.nodeIdentifier == -1:
			print "Can't transform models containing nodes with invalid identifiers (type: " + nodeDst.nodeType + ").\n"
			sys.exit(-1)
		nodeDst.attributes = nodeSrc.attributes
		dst.nodes.append(nodeDst)
	# Copy links
	for srcLink in src.links:
		dstLink = RoboCompAGMWorldModel.Edge()
		dstLink.edgeType = srcLink.linkType
		dstLink.a = int(srcLink.a)
		if dstLink.a == -1:
			print "Can't transform models containing edges linking invalid identifiers (type: "+dstLink.edgeType+").\n"
			sys.exit(-1)
		dstLink.b = int(srcLink.b)
		if dstLink.b == -1:
			print "Can't transform models containing edges linking invalid identifiers (type: "+dstLink.edgeType+").\n"
			sys.exit(-1)
		dst.edges.append(dstLink)
	return dst


def fromIceToInternal_model(src):
	dst = AGMGraph()
	
	for srcNode in src.nodes:
		dst.addNode(0,0, str(srcNode.nodeIdentifier), srcNode.nodeType, srcNode.attributes)
		if srcNode.nodeIdentifier == -1:
			print "Can't transform models containing nodes with invalid identifiers (type: "+src.nodes[i].nodeType+").\n"
			sys.exit(-1)

	for srcLink in src.edges:
		edge = AGMLink(str(srcLink.a), str(srcLink.b), srcLink.edgeType)
		dst.links.append(edge)
		if srcLink.a == -1 or srcLink.b == -1:
			print "Can't transform models containing nodes with invalid identifiers (type: "+src.edges[i].edgeType+").\n"
			sys.exit(-1)
	
	return dst

def fromIceToInternal_node(node):
	return AGMSymbol(str(node.nodeIdentifier), node.nodeType, [0,0], node.attributes)


#bool AGMModelConverter::includeIceModificationInInternalModel(const RoboCompAGMWorldModel::Node &node, AGMModel::SPtr &world)
#{
	#for (uint32_t i=0; i<world->symbols.size(); ++i)
	#{
		#if (node.nodeType == world->symbols[i]->sType and node.nodeIdentifier == world->symbols[i]->identifier)
		#{
			#std::map<std::string, std::string>::const_iterator iter
			#for (iter = node.attributes.begin(); iter!=node.attributes.end(); iter++)
			#{
				#world->symbols[i]->attributes[iter->first] = iter->second
			#}
			#return true
		#}
	#}
	#return false
#}

#int32_t getIdFromString(char *sid, int32_t &lastVariableId, std::map <std::string, int32_t> &identifierMap)
#{
	#int32_t id
	#if ((sid[0] >= 'a' and sid[0] <= 'z') or (sid[0] >= 'A' and sid[0] <= 'Z'))
	#{
		#std::map <std::string, int32_t>::iterator iter = identifierMap.find(std::string(sid))
		#if (iter == identifierMap.end())
		#{
			#lastVariableId++
			#id = lastVariableId
			#identifierMap[std::string(sid)] = id
		#}
		#else
		#{
			#id = identifierMap[std::string(sid)]
		#}
	#}
	#else
	#{
		#id = atoi((char *)sid)
	#}
	#if (id<0)
	#{
		#fprintf(stderr, "AGMModels can't have negative identifiers (type: %s).\n", (char *)sid)
		#exit(-1)
	#}

	#return id
#}



