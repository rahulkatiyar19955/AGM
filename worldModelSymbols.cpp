#include "worldModelSymbols.h"
#include "worldModel.h"


int32_t WorldModelSymbol::lastId = 0;

boost::mutex WorldModelSymbol::mutex;

WorldModelSymbol::WorldModelSymbol()
{
	symbolType = "";
	identifier = WorldModelSymbol::getNewId();
}

WorldModelSymbol::WorldModelSymbol(std::string ntype, int32_t id)
{
	symbolType = ntype;
	if (id == -1)
		identifier = WorldModelSymbol::getNewId();
	else
		identifier = id;
}


WorldModelSymbol::~WorldModelSymbol()
{
}

bool WorldModelSymbol::operator==(const WorldModelSymbol &p) const
{
	if (symbolType == p.symbolType)
		return true;
	return false;
}

std::string WorldModelSymbol::toString() const
{
	std::ostringstream stringStream;
	stringStream << symbolType << "_" << identifier;
	return stringStream.str();
}

std::string WorldModelSymbol::typeString() const
{
	std::ostringstream stringStream;
	stringStream << symbolType;
  return stringStream.str();
}
	
int32_t WorldModelSymbol::getNewId()
{
	int32_t ret;
	mutex.lock();
	ret = lastId;
	lastId++;
	mutex.unlock();
	return ret;
}

int32_t WorldModelSymbol::getLastId()
{
	int32_t ret;
	mutex.lock();
	ret = lastId;
	mutex.unlock();
	return ret;
}



