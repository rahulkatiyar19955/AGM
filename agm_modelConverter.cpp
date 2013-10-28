#include <stdio.h>
#include <unistd.h>

#include <agm_modelConverter.h>
#include <agm_modelEdge.h>

#include <libxml2/libxml/parser.h>
#include <libxml2/libxml/tree.h>

#ifdef ROBOCOMP_SUPPORT
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

#endif

void AGMModelConverter::fromXMLToInternal(const std::string path, AGMModel::SPtr &dst)
{
	// Empty the model
	dst->symbols.clear();
	dst->edges.clear();

	xmlDocPtr doc;
	if ((doc = xmlParseFile(path.c_str())) == NULL)
	{
		fprintf(stderr,"Document not parsed successfully. \n");
		return;
	}
	xmlNodePtr cur;
	if ((cur = xmlDocGetRootElement(doc)) == NULL)
	{
		fprintf(stderr,"empty document\n");
		xmlFreeDoc(doc);
		return;
	}
	if (xmlStrcmp(cur->name, (const xmlChar *) "AGMModel"))
	{
		fprintf(stderr,"document of the wrong type, root node != AGMModel");
		xmlFreeDoc(doc);
		return;
	}



	for(cur=cur->xmlChildrenNode; cur!=NULL; cur=cur->next)
	{
		if ((xmlStrcmp(cur->name, (const xmlChar *)"text")))
		{
			if ((!xmlStrcmp(cur->name, (const xmlChar *)"symbol")))
			{
				// Read ID and type
				xmlChar *stype = xmlGetProp(cur, (const xmlChar *)"type");
				xmlChar *sid = xmlGetProp(cur, (const xmlChar *)"id");
				int32_t id = atoi((char *)sid);
				if (id<0)
				{
					fprintf(stderr, "AGMModels can't have negative identifiers (type: %s).\n", (char *)stype);
					exit(-1);
				}

				// Read attributes
				std::map<std::string, std::string> attrMap;
				for (xmlNodePtr cur2=cur->xmlChildrenNode; cur2!=NULL; cur2=cur2->next)
				{
					if ((!xmlStrcmp(cur2->name, (const xmlChar *)"attribute")))
					{
						xmlChar *skey = xmlGetProp(cur2, (const xmlChar *)"key");
						if (skey == NULL) { printf("An atribute of %s lacks of attribute 'key'.\n", (char *)cur->name); exit(-1); }
						xmlChar *svalue = xmlGetProp(cur2, (const xmlChar *)"value");
						if (svalue == NULL) { printf("An atribute of %s lacks of attribute 'value'.\n", (char *)cur->name); exit(-1); }
						attrMap[std::string((char *)skey)] = std::string((char *)svalue);
						xmlFree(skey);
						xmlFree(svalue);
					}
					else if ((!xmlStrcmp(cur->name, (const xmlChar *)"text")))
					{
						printf("%s has invalid child %s\n", cur->name, cur2->name);
						exit(-1);
					}
				}

				dst->newSymbol(id, std::string((char*)stype), attrMap);

				xmlFree(sid);
				xmlFree(stype);
			}
			else if ((!xmlStrcmp(cur->name, (const xmlChar *)"link")))
			{
				xmlChar *srcn = xmlGetProp(cur, (const xmlChar *)"src");
				if (srcn == NULL) { printf("Link %s lacks of attribute 'src'.\n", (char *)cur->name); exit(-1); }
				xmlChar *dstn = xmlGetProp(cur, (const xmlChar *)"dst");
				if (dstn == NULL) { printf("Link %s lacks of attribute 'dst'.\n", (char *)cur->name); exit(-1); }
				xmlChar *label = xmlGetProp(cur, (const xmlChar *)"label");
				if (label == NULL) { printf("Link %s lacks of attribute 'label'.\n", (char *)cur->name); exit(-1); }
				
				AGMModelEdge edge(atoi((char *)srcn), atoi((char *)dstn), (char *)label);
				if (edge.symbolPair.first == -1 or edge.symbolPair.second == -1)
				{
					fprintf(stderr, "Can't create models with invalid identifiers (type: %s).\n", edge.linking.c_str());
					exit(-1);
				}
				dst->edges.push_back(edge);
				xmlFree(srcn);
				xmlFree(dstn);
			}
			else
			{
				printf("??? %s\n", cur->name);
			}
		}
	}


	dst->resetLastId();
	//checks
	
}



