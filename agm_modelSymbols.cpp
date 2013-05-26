#include "agm_modelSymbols.h"
#include "agm_model.h"


int32_t AGMModelSymbol::lastId = 0;

boost::mutex AGMModelSymbol::mutex;

AGMModelSymbol::AGMModelSymbol()
{
	symbolType = "";
	identifier = AGMModelSymbol::getNewId();
}

AGMModelSymbol::AGMModelSymbol(int32_t identifier, std::string typ, std::map<std::string, std::string> atr)
{
	symbolType = typ;
	identifier = identifier;
	attributes = atr;
}



AGMModelSymbol::~AGMModelSymbol()
{
}

bool AGMModelSymbol::operator==(const AGMModelSymbol &p) const
{
	if (symbolType == p.symbolType)
		return true;
	return false;
}

std::string AGMModelSymbol::toString() const
{
	std::ostringstream stringStream;
	stringStream << symbolType << "_" << identifier;
	return stringStream.str();
}

std::string AGMModelSymbol::typeString() const
{
	std::ostringstream stringStream;
	stringStream << symbolType;
  return stringStream.str();
}
	
int32_t AGMModelSymbol::getNewId()
{
	int32_t ret;
	mutex.lock();
	ret = lastId;
	lastId++;
	mutex.unlock();
	return ret;
}

int32_t AGMModelSymbol::getLastId()
{
	int32_t ret;
	mutex.lock();
	ret = lastId;
	mutex.unlock();
	return ret;
}



