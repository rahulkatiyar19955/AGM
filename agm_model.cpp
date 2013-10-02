#include "agm_model.h"

#include "agm_modelEdge.h"
#include <sstream>

#include <algorithm>
#include <list>

AGMModel::AGMModel()
{
	lastId = 0;
// 	printf("new model: (%p)\n", this);
}

AGMModel::~AGMModel()
{
// 	printf("delete model: (%p)\n", this);
	lastId = 0;
	symbols.clear();
	edges.clear();
}

AGMModel::AGMModel(const AGMModel::SPtr &src)
{
// 	printf("new model (sptr): (%p)\n", this);
	//printf("AGMModel::AGMModel(const AGMModel::SPtr &src)\n");
	setFrom(*src);
}

AGMModel::AGMModel(const AGMModel &src)
{
	//printf("AGMModel::AGMModel(const AGMModel &src)\n");
// 	printf("new model (&): (%p)\n", this);
	setFrom(src);
}

AGMModel &AGMModel::operator=(const AGMModel &src)
{
	//printf("AGMModel& AGMModel::operator=(const AGMModel &src)\n");
	setFrom(src);
	return *this;
}

void AGMModel::setFrom(const AGMModel &src)
{
	lastId = src.lastId;

	symbols.clear();
	for (uint32_t i=0; i<src.symbols.size(); ++i)
	{
		newSymbol(src.symbols[i]->identifier, src.symbols[i]->typeString(), src.symbols[i]->attributes);
	}

	edges.clear();
	for (uint32_t i=0; i<src.edges.size(); ++i)
	{
		AGMModelEdge edge(src.edges[i].symbolPair.first, src.edges[i].symbolPair.second, src.edges[i].linking);
		edges.push_back(edge);
	}
	
	resetLastId();
}

void AGMModel::resetLastId()
{
	int64_t maxId = 0;
	for (uint32_t i=0; i<symbols.size(); ++i)
	{
		if (symbols[i]->identifier >= maxId)
		{
			maxId = symbols[i]->identifier + 1;
		}
	}
	lastId = maxId;
}

void AGMModel::clear()
{
	lastId = 0;
	symbols.clear();
	edges.clear();
}


int32_t AGMModel::numberOfEdges() const
{
	return edges.size();
}

int32_t AGMModel::numberOfSymbols() const
{
	return symbols.size();
}


AGMModelSymbol::SPtr AGMModel::getSymbol(int32_t identif) const
{
	for (uint32_t i=0; i<symbols.size(); ++i)
	{
		if (symbols[i]->identifier == identif)
		{
			return symbols[i];
		}
	}
// 	printf("%d\n", __LINE__);
	throw "No such symbol";
}

int32_t AGMModel::getIdentifierByName(std::string name) const
{
	for (uint32_t i=0; i<symbols.size(); ++i)
	{
		if (symbols[i]->toString() == name)
		{
			return symbols[i]->identifier;
		}
	}
// 	printf("%d\n", __LINE__);
// 	throw "No such symbol";
	return -1;
}


int32_t AGMModel::insertSymbol(AGMModelSymbol::SPtr s)
{
	symbols.push_back(s);
	return (int)symbols.size();
}


int32_t AGMModel::indexOfSymbol(const AGMModelSymbol::SPtr &value, int32_t from) const
{
	for (uint32_t i=from; i<symbols.size(); ++i)
	{
		if (symbols[i] == value)
		{
			return i;
		}
	}
// 	fprintf(stderr, "AGMModel::indexOfSymbol: unknown symbol \"%s\"\n", value->symbolType.c_str());
// 	printf("%d\n", __LINE__);
	return -1;
}

int32_t AGMModel::indexOfFirstSymbolByValues(const AGMModelSymbol &value, int32_t from) const
{
	for (uint32_t i=from; i<symbols.size(); ++i)
	{
		AGMModelSymbol::SPtr p = symbols[i];
		AGMModelSymbol no_ptr = *(p.get());
		if (no_ptr == value)
		{
			return i;
		}
	}
// 	fprintf(stderr, "AGMModel::indexOfFirstSymbolByValues: no equal \"%s\"   %d\n", value.symbolType.c_str(), __LINE__);
// 	printf("%d\n", __LINE__);
	return -1;
}


int32_t AGMModel::indexOfFirstSymbolByType(const std::string &value, int32_t from) const
{
	for (uint32_t i=from; i<symbols.size(); ++i)
	{
		if (symbols[i]->symbolType == value)
		{
			return i;
		}
	}
// 	fprintf(stderr, "AGMModel::indexOfFirstSymbolByType: \"%s\", (%d)\n", value.c_str(), from);
// 	printf("%d\n", __LINE__);
	return -1;
}


std::string AGMModel::generatePDDLProblem(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName) const
{
	std::ostringstream stringStream;
	if (target->symbols.size() == 0) return "";

	/// H E A D E R
	stringStream << "(define (problem " << problemName << ")\n";
	stringStream << "\n";

	/// D O M A I N
	stringStream << "	(:domain " << domainName << ")\n";

	/// D E C L A R E   O B J E C T S
	stringStream << "	(:objects\n";
	std::list <std::string> originalObjects;
	// Symbols that are present in the original model
	for (uint32_t s=0; s<symbols.size(); ++s)
	{
		originalObjects.push_back(symbols[s]->toString());
		stringStream << "		" << symbols[s]->toString() << "\n";
	}

	// Symbols that are only in the target model (not in the original model)
	std::list <std::string> targetObjects;
	for (uint32_t s=0; s<target->symbols.size(); ++s)
	{
		bool found = false;
		for (std::list< std::string>::iterator it=originalObjects.begin(); it!=originalObjects.end(); ++it)
		{
			if (*it == target->symbols[s]->toString())
			{
				found = true;
				break;
			}
		}
		if (not found)
		{
			targetObjects.push_back(target->symbols[s]->toString());
			unknowns++;
// 			stringStream << "		" << target->symbols[s]->toString() << "\n";
		}
	}

	// Unknown symbols that allow us to include new stuff in the model
	for (int32_t u=0; u<unknowns; ++u)
	{
		stringStream << "		unknown_" << u << "\n";
	}
	stringStream << "	)\n";
	stringStream << "\n";

	/// I N I T I A L   W O R L D
	stringStream << "	(:init\n";
	// Initial cost
	stringStream << "		(= (total-cost) 0)\n";
	// Unknown temporary objects we are going to artificially inject
	if (unknowns>0)
		stringStream << "		(firstunknown unknown_0)\n";
	for (int32_t u=1; u<unknowns; ++u)
	{
		stringStream << "		(unknownorder unknown_" << u-1 << " unknown_" << u << ")\n";
	}
	// Known symbols type for the objects in the initial world
	for (uint32_t s=0; s<symbols.size(); ++s)
	{
		stringStream << "		(IS" << symbols[s]->typeString() << " " << symbols[s]->toString() << ")\n";
	}
	// Introduce edges themselves
	for (uint32_t e=0; e<edges.size(); ++e)
	{
		stringStream << "		(" << edges[e].toString(this) << ")\n";
	}
	stringStream << "	)\n";

	/// T A R G E T    W O R L D
	/// T A R G E T    W O R L D
	stringStream << "	\n";
	stringStream << "	(:goal\n";
	if (targetObjects.size()>0)
	{
		stringStream << "		(exists (";
		for (std::list< std::string>::iterator it=targetObjects.begin(); it!=targetObjects.end(); ++it)
		{
			stringStream << " ?" << *it;
		}
		stringStream << " )\n";
	}
	stringStream << "			(and\n";

	// Known symbols type for the objects in the target world
	for (uint32_t s=0; s<target->symbols.size(); ++s)
	{
		std::string kStr = " ";
		for (std::list< std::string>::iterator it=targetObjects.begin(); it!=targetObjects.end(); ++it)
		{
			if (target->symbols[s]->toString() == *it)
				kStr = " ?";
		}
		stringStream << "				(IS" << target->symbols[s]->typeString() << kStr << target->symbols[s]->toString() << ")\n";
	}
	for (uint32_t e=0; e<target->edges.size(); ++e)
	{
		std::string label, a, b, kStr;
		target->edges[e].getStrings(target, label, a, b);
		stringStream << "				(" << label;

		kStr = " ";
		for (std::list< std::string>::iterator it=targetObjects.begin(); it!=targetObjects.end(); ++it)
		{
			if (a == *it)
				kStr = " ?";
		}
		stringStream << kStr << a;

		kStr = " ";
		for (std::list< std::string>::iterator it=targetObjects.begin(); it!=targetObjects.end(); ++it)
		{
			if (b == *it)
				kStr = " ?";
		}
		stringStream << kStr << b;

		stringStream << ")\n";
	}

	stringStream << "			)\n";
	if (targetObjects.size()>0)
		stringStream << "		)\n";
	stringStream << "	)\n";
	stringStream << "\n";

	/// M E T R I C   D E F I N I T I O N
	stringStream << "	(:metric minimize (total-cost))\n";
	stringStream << "\n";
	stringStream << "\n";
	stringStream << ")\n";

//   stringStream << symbolType << "_" << identifier;
  return stringStream.str();
}

std::vector<AGMModelSymbol::SPtr> AGMModel::getSymbols() const
{
	return symbols;
}

std::vector<AGMModelEdge> AGMModel::getEdges() const
{
	return edges;
}

AGMModelSymbol::SPtr & AGMModel::symbol(uint32_t i)
{
	return symbols[i];
}


AGMModelEdge & AGMModel::edge(uint32_t i)
{
	return edges[i];
}

int32_t AGMModel::getIdentifierByType(std::string type, int32_t times) const
{
	printf("getIdentifierByType: %s, %d\n", type.c_str(), times);
	int32_t ret = -1;
	uint32_t idx = 0;
	for (int32_t time=0; time<=times; ++time)
	{
		for ( ; idx<symbols.size(); ++idx)
		{
			if (symbols[idx]->symbolType == type)
			{
				if (time==times) { /*printf("indice será %d\n", (int32_t)idx);*/ ret = idx;  }
				break;
			}
		}
		if (idx>=symbols.size())
		{
			return -1;
		}
	}
	if (ret != -1)
	{
// 		printf("devolvemos [%d].id ---> _%d_\n", ret, symbols[ret]->identifier);
// 		printf("%s %d\n", __FILE__, __LINE__);
		return symbols[ret]->identifier;
	}
	return -1;
}


int32_t AGMModel::getLinkedID(int32_t id, std::string linkname, int32_t i) const
{
	int64_t ret = -1;
	uint32_t idx = 0;
	for (int32_t time=0; time<=i; ++time)
	{
		for ( ; idx<edges.size(); ++idx)
		{
			if (edges[idx].symbolPair.first == id and linkname == edges[idx].linking)
			{
				if (time==i) ret = idx;
				break;
			}
		}
		if (idx>=symbols.size())
		{
			printf("Exception: %d, %s, %d\n", id, linkname.c_str(), i);
			return -1;
// 			AGMMODELEXCEPTION("Trying to get the identifier of a node linked to a given one");
		}
	}
	if (ret != -1)
		return edges[ret].symbolPair.second;
// 	printf("%d\n", __LINE__);
	return -1;
}



int32_t AGMModel::getIndexByIdentifier(int32_t targetId) const
{
	for (uint32_t idx=0; idx<symbols.size(); ++idx)
	{
		if (symbols[idx]->identifier == targetId)
		{
			return idx;
		}
	}
	
	std::ostringstream s;
	s << "Exception: " << targetId;
	return -1;
// 	AGMMODELEXCEPTION(s.str()+std::string(" Trying to get the index of a node given it's identifier"));
}


bool AGMModel::removeSymbol(int32_t id)
{
	removeEdgesRelatedToSymbol(id);
	int32_t index = getIndexByIdentifier(id);
	if (index >= 0)
	{
		symbols.erase(symbols.begin() + index);
		return true;
	}
	return false;
}

int32_t AGMModel::replaceIdentifierInEdges(int32_t a, int32_t b)
{
	int32_t ret = 0;
	for (uint32_t edge=0; edge < edges.size(); ++edge)
	{
		if (edges[edge].symbolPair.first == a)
		{
			edges[edge].symbolPair.first = b;
			ret++;
		}
		if (edges[edge].symbolPair.second == a)
		{
			edges[edge].symbolPair.second = b;
			ret++;
		}
	}
	return ret;
}

bool AGMModel::removeEdgesRelatedToSymbol(int32_t id)
{
	bool any = false;
	for (int p=0; p<numberOfEdges(); p++)
	{
		if (edges[p].symbolPair.first == id or edges[p].symbolPair.second == id)
		{
			edges.erase(edges.begin() + p);
			any = true;
		}
	}
	return any;
}


void AGMModel::setSymbols(std::vector<AGMModelSymbol::SPtr> s)
{
	symbols = s;
}

void AGMModel::setEdges(std::vector<AGMModelEdge> e)
{
	edges = e;
}


int32_t AGMModel::getNewId()
{
	int32_t ret;
	ret = lastId;
	lastId++;
	return ret;
}


bool AGMModel::addEdgeByIdentifiers(int32_t a, int32_t b, const std::string &edgeName)
{
	// Nodes must exist.
	if (a < 0 or b < 0)
	{
		AGMMODELEXCEPTION("Trying to link invalid identifiers");;
	}

	// Check the edge doesn't already exists
	for (uint32_t i=0; i<edges.size(); i++)
	{
		if (edges[i].symbolPair.first == a)
		{
			if (edges[i].symbolPair.second == b)
			{
				if (edges[i].getLabel() == edgeName)
				{
					return false;
				}
			}
		}
	}
	AGMModelEdge edge(a, b, edgeName);
	edges.push_back(edge);
	return true;
}


bool AGMModel::removeEdgeByIdentifiers(int32_t a, int32_t b, const std::string &edgeName)
{
	// Nodes must exist.
	if (a < 0 or b < 0)
	{
		AGMMODELEXCEPTION("Trying to un-link using invalid identifiers");;
	}

	// Check the edge doesn't already exists
	for (uint32_t i=0; i<edges.size(); i++)
	{
		if (edges[i].symbolPair.first == a)
		{
			if (edges[i].symbolPair.second == b)
			{
				if (edges[i].getLabel() == edgeName)
				{
					edges.erase(edges.begin() + i);
					return true;
				}
			}
		}
	}
	return false;
}

