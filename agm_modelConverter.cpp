#include <stdio.h>
#include <unistd.h>

#include <agm_modelConverter.h>
#include <agm_modelEdge.h>

void AGMModelConverter::fromInternalToIce(const AGMModel::SPtr &src, RoboCompWorldModel::GualzruWorld &dst)
{
	dst.nodes.clear();
	for (uint32_t i=0; i<src->symbols.size(); ++i)
	{
		RoboCompWorldModel::GualzruWorldNode node;
		node.nodeType = src->symbols[i]->symbolType;
		node.nodeIdentifier = src->symbols[i]->identifier;
		node.attributes = src->symbols[i]->attributes;
		dst.nodes.push_back(node);
	}

	dst.edges.clear();
	for (uint32_t i=0; i<src->edges.size(); ++i)
	{
		RoboCompWorldModel::GualzruWorldEdge edge;
		edge.a = src->edges[i].symbolPair.first;
		edge.b = src->edges[i].symbolPair.second;
		edge.edgeType = src->edges[i].linking;
		dst.edges.push_back(edge);
	}
}


void AGMModelConverter::fromIceToInternal(const RoboCompWorldModel::GualzruWorld &src, AGMModel::SPtr &dst)
{
	dst->symbols.clear();
	for (uint32_t i=0; i<src.nodes.size(); ++i)
	{
		AGMModelSymbol *symbolPtr = new AGMModelSymbol(dst.get(), src.nodes[i].nodeIdentifier, src.nodes[i].nodeType, src.nodes[i].attributes);
		dst->symbols.push_back(AGMModelSymbol::SPtr(symbolPtr));
	}

	dst->edges.clear();
	for (uint32_t i=0; i<src.edges.size(); ++i)
	{
		AGMModelEdge edge(src.edges[i].a, src.edges[i].b, src.edges[i].edgeType);
		dst->edges.push_back(edge);
	}

	dst->resetLastId();
}

void AGMModelConverter::fromInternalToIce(const AGMModelSymbol::SPtr &node, RoboCompWorldModel::GualzruWorldNode &dst)
{
	dst.nodeType = node->symbolType;
	dst.nodeIdentifier = node->identifier;
	dst.attributes = node->attributes;
}

void AGMModelConverter::fromIceToInternal(const RoboCompWorldModel::GualzruWorldNode &node, AGMModelSymbol::SPtr &dst)
{
	dst->symbolType = node.nodeType;
	dst->attributes = node.attributes;
	dst->identifier = node.nodeIdentifier;
}


bool AGMModelConverter::includeIceModificationInInternalModel(const RoboCompWorldModel::GualzruWorldNode &node, AGMModel::SPtr &world)
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


