#include <stdio.h>
#include <unistd.h>

#include <agm_modelConverter.h>
#include <agm_modelEdge.h>

void AGMModelConverter::fromInternalToIce(const AGMModel::SPtr &src, RoboCompAGMWorldModel::World &dst)
{
	dst.nodes.clear();
	for (uint32_t i=0; i<src->symbols.size(); ++i)
	{
		RoboCompAGMWorldModel::Node node;
		node.nodeType = src->symbols[i]->symbolType;
		node.nodeIdentifier = src->symbols[i]->identifier;
		if (node.nodeIdentifier == -1)
		{
			fprintf(stderr, "Can't transform models containing nodes with invalid identifiers (type: %s).\n", node.nodeType.c_str());
			exit(-1);
		}
		node.attributes = src->symbols[i]->attributes;
		dst.nodes.push_back(node);
	}

	dst.edges.clear();
	for (uint32_t i=0; i<src->edges.size(); ++i)
	{
		RoboCompAGMWorldModel::Edge edge;
		edge.edgeType = src->edges[i].linking;
		edge.a = src->edges[i].symbolPair.first;
		if (edge.a == -1)
		{
			fprintf(stderr, "Can't transform models containing edges linking invalid identifiers (type: %s).\n", edge.edgeType.c_str());
			exit(-1);
		}
		edge.b = src->edges[i].symbolPair.second;
		if (edge.b == -1)
		{
			fprintf(stderr, "Can't transform models containing edges linking invalid identifiers (type: %s).\n", edge.edgeType.c_str());
			exit(-1);
		}
		dst.edges.push_back(edge);
	}
}


void AGMModelConverter::fromIceToInternal(const RoboCompAGMWorldModel::World &src, AGMModel::SPtr &dst)
{
	dst->symbols.clear();
	for (uint32_t i=0; i<src.nodes.size(); ++i)
	{
		dst->newSymbol(src.nodes[i].nodeIdentifier, src.nodes[i].nodeType, src.nodes[i].attributes);
		if (src.nodes[i].nodeIdentifier == -1)
		{
			fprintf(stderr, "Can't transform models containing nodes with invalid identifiers (type: %s).\n", src.nodes[i].nodeType.c_str());
			exit(-1);
		}
	}

	dst->edges.clear();
	for (uint32_t i=0; i<src.edges.size(); ++i)
	{
		AGMModelEdge edge(src.edges[i].a, src.edges[i].b, src.edges[i].edgeType);
		dst->edges.push_back(edge);
		if (src.edges[i].a == -1 or src.edges[i].b == -1)
		{
			fprintf(stderr, "Can't transform models containing nodes with invalid identifiers (type: %s).\n", src.edges[i].edgeType.c_str());
			exit(-1);
		}
	}

	dst->resetLastId();
}

void AGMModelConverter::fromInternalToIce(const AGMModelSymbol::SPtr &node, RoboCompAGMWorldModel::Node &dst)
{
	dst.nodeType = node->symbolType;
	dst.nodeIdentifier = node->identifier;
	dst.attributes = node->attributes;
}

void AGMModelConverter::fromInternalToIce(const AGMModelSymbol *node, RoboCompAGMWorldModel::Node &dst)
{
	dst.nodeType = node->symbolType;
	dst.nodeIdentifier = node->identifier;
	dst.attributes = node->attributes;
}

void AGMModelConverter::fromIceToInternal(const RoboCompAGMWorldModel::Node &node, AGMModelSymbol::SPtr &dst)
{
	dst->symbolType = node.nodeType;
	dst->attributes = node.attributes;
	dst->identifier = node.nodeIdentifier;
}


bool AGMModelConverter::includeIceModificationInInternalModel(const RoboCompAGMWorldModel::Node &node, AGMModel::SPtr &world)
{
	for (uint32_t i=0; i<world->symbols.size(); ++i)
	{
		if (node.nodeType == world->symbols[i]->symbolType and node.nodeIdentifier == world->symbols[i]->identifier)
		{
			std::map<std::string, std::string>::const_iterator iter;
			for (iter = node.attributes.begin(); iter!=node.attributes.end(); iter++)
			{
				world->symbols[i]->attributes[iter->first] = iter->second;
			}
			return true;
		}
	}
	return false;
}


