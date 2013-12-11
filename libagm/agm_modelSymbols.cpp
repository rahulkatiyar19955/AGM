#include "agm_modelSymbols.h"
#include "agm_model.h"

AGMModelSymbol::AGMModelSymbol(AGMModel *model, std::string typ, int32_t id) { init(model, typ, id); }
AGMModelSymbol::AGMModelSymbol(AGMModel *model, int32_t identifier, std::string typ) { init(model, identifier, typ); }
AGMModelSymbol::AGMModelSymbol(AGMModel *model, int32_t identifier, std::string typ, std::map<std::string, std::string> atr) { init(model, identifier, typ, atr); }
AGMModelSymbol::AGMModelSymbol(AGMModel::SPtr model, std::string typ, int32_t id) { init(model.get(), typ, id); }
AGMModelSymbol::AGMModelSymbol(AGMModel::SPtr model, int32_t identifier, std::string typ) { init(model.get(), identifier, typ); }
AGMModelSymbol::AGMModelSymbol(AGMModel::SPtr model, int32_t identifier, std::string typ, std::map<std::string, std::string> atr) { init(model.get(), identifier, typ, atr); }

void AGMModelSymbol::init(AGMModel *model, std::string typ, int32_t id)
{
	if (model == NULL)
	{
		fprintf(stdout, "AGMModelSymbol::init: error: MODEL NULL!!\n");
		exit(-1);
	}

	symbolType = typ;
	if (id==-1)
	{
		identifier = model->getNewId();
	}
	else
		identifier = id;

	model->insertSymbol(this);

// 	printf("new symbol: %s [%d] (%p)\n", symbolType.c_str(), identifier, this);
}

void AGMModelSymbol::init(AGMModel *model, int32_t id, std::string typ)
{
	if (model == NULL)
	{
		fprintf(stdout, "AGMModelSymbol::init: error: MODEL NULL!!\n");
		exit(-1);
	}

	identifier = id;
	symbolType = typ;

	model->insertSymbol(this);

// 	printf("new symbol: %s [%d] (%p)\n", symbolType.c_str(), identifier, this);
}

void AGMModelSymbol::init(AGMModel *model, int32_t id, std::string typ, std::map<std::string, std::string> atr)
{
	if (model == NULL)
	{
		fprintf(stdout, "AGMModelSymbol::init: error: MODEL NULL!!\n");
		exit(-1);
	}

	identifier = id;
	symbolType = typ;
	attributes = atr;

	if (model != NULL)
		model->insertSymbol(this);

// 	printf("new symbol: %s [%d] (%p)\n", symbolType.c_str(), identifier, this);
}



AGMModelSymbol::~AGMModelSymbol()
{
// 	printf("delete symbol: %s [%d] (%p)\n", symbolType.c_str(), identifier, this);
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
	


void AGMModelSymbol::setType(std::string t)
{
	symbolType = t;
}


void AGMModelSymbol::setIdentifier(int32_t t)
{
	identifier = t;
}

void AGMModelSymbol::setAttribute(std::string a, std::string v)
{
	attributes[a] = v;
}

std::string AGMModelSymbol::getAttribute(std::string a)
{
	return attributes[a];
}


