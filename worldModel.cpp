#include "worldModel.h"

#include "worldModelEdge.h"

#include <algorithm>
#include <list>

float str2float(const std::string &s)
{
	if (s.size()<=0)
	{
		printf("dkeiodeji\n");
		WORLDMODELEXCEPTION("dekiehdiwohffhew 3423\n");
	}

	float ret;
	std::string str = s;
	replace(str.begin(), str.end(), ',', '.');
	std::istringstream istr(str);
	istr.imbue(std::locale("C"));
	istr >> ret;
	return ret;
}

WorldModel::WorldModel()
{
}

WorldModel::~WorldModel()
{
	symbols.clear();
	edges.clear();
}

WorldModel::WorldModel(const WorldModel::SPtr &src)
{
// 	printf("WorldModel::WorldModel(const WorldModel::SPtr &src)\n");
	setFrom(*src);
}

WorldModel::WorldModel(const WorldModel &src)
{
// 	printf("WorldModel::WorldModel(const WorldModel &src)\n");
	setFrom(src);
}

WorldModel& WorldModel::operator=(const WorldModel &src)
{
// 	printf("WorldModel& WorldModel::operator=(const WorldModel &src)\n");
	setFrom(src);
	return *this;
}

void WorldModel::setFrom(const WorldModel &src)
{
	symbols.clear();
	for (uint32_t i=0; i<src.symbols.size(); ++i)
	{
		WorldModelSymbol::SPtr symbolPtr;
		symbolPtr = WorldModelSymbol::SPtr(new WorldModelSymbol());
		symbolPtr->symbolType = src.symbols[i]->symbolType;
		symbolPtr->identifier = src.symbols[i]->identifier;
		symbolPtr->attributes = src.symbols[i]->attributes;
		symbols.push_back(symbolPtr);
	}

	edges.clear();
	for (uint32_t i=0; i<src.edges.size(); ++i)
	{
		WorldModelEdge edge(src.edges[i].symbolPair.first, src.edges[i].symbolPair.second, src.edges[i].linking);
		edges.push_back(edge);
	}
}


void WorldModel::resetLastId()
{
	int64_t maxId = -1;
	for (uint32_t i=0; i<symbols.size(); ++i)
	{
		if (symbols[i]->identifier >= maxId)
		{
			maxId = symbols[i]->identifier + 1;
		}
	}
	WorldModelSymbol::setLastID(maxId);
}

void WorldModel::clear()
{
		symbols.clear();
		edges.clear();
}


int32_t WorldModel::numberOfEdges() const
{
	return edges.size();
}

int32_t WorldModel::numberOfSymbols() const
{
	return symbols.size();
}


WorldModelSymbol::SPtr WorldModel::getSymbol(int32_t identif) const
{
	for (uint32_t i=0; i<symbols.size(); ++i)
	{
		if (symbols[i]->identifier == identif)
		{
			return symbols[i];
		}
	}
	printf("%d\n", __LINE__);
	throw "No such symbol";
}

int32_t WorldModel::getIdentifierByName(std::string name) const
{
	for (uint32_t i=0; i<symbols.size(); ++i)
	{
		if (symbols[i]->toString() == name)
		{
			return symbols[i]->identifier;
		}
	}
	printf("%d\n", __LINE__);
	throw "No such symbol";
}


int32_t WorldModel::insertSymbol(WorldModelSymbol::SPtr s)
{
	symbols.push_back(s);
	return (int)symbols.size();
}


int32_t WorldModel::indexOfSymbol(const WorldModelSymbol::SPtr &value, int32_t from) const
{
	for (uint32_t i=from; i<symbols.size(); ++i)
	{
		if (symbols[i] == value)
		{
			return i;
		}
	}
	fprintf(stderr, "WorldModel::indexOfSymbol: unknown symbol \"%s\"\n", value->symbolType.c_str());
	printf("%d\n", __LINE__);
	return -1;
}

int32_t WorldModel::indexOfFirstSymbolByValues(const WorldModelSymbol &value, int32_t from) const
{
	for (uint32_t i=from; i<symbols.size(); ++i)
	{
		WorldModelSymbol::SPtr p = symbols[i];
		WorldModelSymbol no_ptr = *(p.get());
		if (no_ptr == value)
		{
			return i;
		}
	}
	fprintf(stderr, "WorldModel::indexOfFirstSymbolByValues: no equal \"%s\"   %d\n", value.symbolType.c_str(), __LINE__);
	printf("%d\n", __LINE__);
	return -1;
}


int32_t WorldModel::indexOfFirstSymbolByType(const std::string &value, int32_t from) const
{
	for (uint32_t i=from; i<symbols.size(); ++i)
	{
		if (symbols[i]->symbolType == value)
		{
			return i;
		}
	}
	fprintf(stderr, "WorldModel::indexOfFirstSymbolByType: \"%s\", (%d)\n", value.c_str(), from);
	printf("%d\n", __LINE__);
	return -1;
}


std::string WorldModel::generatePDDLProblem(const WorldModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName) const
{
	std::ostringstream stringStream;

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

	/// M E T R I C   D E F I N I T I O N
	stringStream << "	(:metric minimize (total-cost))\n";
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
		stringStream << "		(is" << symbols[s]->typeString() << " " << symbols[s]->toString() << ")\n";
	}
	// Introduce edges themselves
	for (uint32_t e=0; e<edges.size(); ++e)
	{
		stringStream << "		(" << edges[e].toString(this) << ")\n";
	}
	stringStream << "	)\n";

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
		stringStream << "				(is" << target->symbols[s]->typeString() << kStr << target->symbols[s]->toString() << ")\n";
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
	stringStream << "\n";
	stringStream << ")\n";

//   stringStream << symbolType << "_" << identifier;
  return stringStream.str();
}

std::vector<WorldModelSymbol::SPtr> WorldModel::getSymbols() const
{
	return symbols;
}

std::vector<WorldModelEdge> WorldModel::getEdges() const
{
	return edges;
}

WorldModelSymbol::SPtr & WorldModel::symbol(uint32_t i)
{
	return symbols[i];
}


WorldModelEdge & WorldModel::edge(uint32_t i)
{
	return edges[i];
}

int32_t WorldModel::getIdentifierByType(std::string type, int32_t times) const
{
	printf("getIdentifierByType: %s, %d\n", type.c_str(), times);
	int32_t ret = -1;
	uint32_t idx = 0;
	for (int32_t time=0; time<=times; ++time)
	{
		printf("taaaim %d of %d\n", (int)time, (int)times);
		for ( ; idx<symbols.size(); ++idx)
		{
			printf("idx:%d   veo(%s)\n", (int32_t)idx, symbols[idx]->symbolType.c_str());
			if (symbols[idx]->symbolType == type)
			{
				if (time==times) { printf("indice será %d\n", (int32_t)idx); ret = idx;  }
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
		printf("devolvemos [%d].id ---> _%d_\n", ret, symbols[ret]->identifier);
		printf("%s %d\n", __FILE__, __LINE__);
		return symbols[ret]->identifier;
	}
	return -1;
}


int32_t WorldModel::getLinkedID(int32_t id, std::string linkname, int32_t i) const
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
			WORLDMODELEXCEPTION("Trying to get the identifier of a node linked to a given one");
		}
	}
	if (ret != -1)
		return edges[ret].symbolPair.second;
	printf("%d\n", __LINE__);
	return -1;
}


int32_t WorldModel::getIndexByIdentifier(int32_t targetId) const
{
	for (uint32_t idx=0; idx<symbols.size(); ++idx)
	{
		if (symbols[idx]->identifier == targetId)
		{
			return idx;
		}
	}
	printf("Exception: %d\n", targetId);
	WORLDMODELEXCEPTION("Trying to get the index of a node given it's identifier");
}





