#include "agm_modelEdge.h"
#include "agm_modelPrinter.h"


AGMModelEdge::AGMModelEdge()
{
	symbolPair = std::pair<int32_t, int32_t>(0, 0);
	linking = "-";
	attributes.clear();
}

AGMModelEdge::~AGMModelEdge()
{
	symbolPair = std::pair<int32_t, int32_t>(0, 0);
	linking = "-";
}

AGMModelEdge::AGMModelEdge(const AGMModelEdge &src)
{
	setFrom(src);
}

AGMModelEdge::AGMModelEdge(int32_t a, int32_t b, std::string linking_)
{
	/*std::map<std::string,std::string> atr;
	atr.clear();
	AGMModelEdge(a,b,linking_,atr);*/
	
	symbolPair = std::pair<int32_t, int32_t>(a, b);
	linking = linking_;
	
	
}

AGMModelEdge::AGMModelEdge(int32_t a, int32_t b, std::string linking_, std::map<std::string, std::string> atr)
{
	symbolPair = std::pair<int32_t, int32_t>(a, b);
	linking = linking_;
	attributes = atr;
}

AGMModelEdge& AGMModelEdge::operator=(const AGMModelEdge &src)
{
	this->setFrom(src);
	return *this;
}



void AGMModelEdge::setFrom(const AGMModelEdge &src)
{
	linking = src.linking;
	symbolPair = src.symbolPair;
}



std::string AGMModelEdge::toString(const AGMModel::SPtr &world) const
{
	return toString(world.get());
}



std::string AGMModelEdge::toString(const AGMModel *world) const
{
	std::ostringstream stringStream;
	std::string stringA, stringB;

	try
	{
		stringA = world->getSymbol(symbolPair.first)->toString();
	}
	catch (...)
	{
		printf("AGMModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.first);
		AGMModelPrinter::printWorld(world);
		exit(-1);
	}
	try
	{
		stringB = world->getSymbol(symbolPair.second)->toString();
	}
	catch (...)
	{
		printf("AGMModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.second);
		AGMModelPrinter::printWorld(world);
		exit(-1);
	}

	stringStream << linking << " " << stringA << " " << stringB;
	return stringStream.str();
}

void AGMModelEdge::setAttribute(std::string a, std::string v)
{
	attributes[a] = v;
}

std::string AGMModelEdge::getAttribute(std::string a)
{
	//return attributes[a];
	std::string s="";
	try{
		s= attributes.at(a);
	}
	catch (const std::out_of_range& oor) {
		std::cout << "Out of Range error: " << oor.what() << '\n';
	}
	return s; 
}



std::string AGMModelEdge::getLabel() const
{
	return linking;
}

std::pair<int32_t, int32_t> AGMModelEdge::getSymbolPair() const
{
	return symbolPair;
}

void AGMModelEdge::setLabel(std::string l)
{
	linking = l;
}


void AGMModelEdge::setSymbolPair(std::pair<int32_t, int32_t> p)
{
	symbolPair = p;
}

void AGMModelEdge::getStrings(const AGMModel::SPtr &world, std::string &label, std::string &a, std::string &b) const
{
	getStrings(world.get(), label, a, b);
}

void AGMModelEdge::getStrings(const AGMModel *world, std::string &label, std::string &a, std::string &b) const
{
	try
	{
		a = world->getSymbol(symbolPair.first)->toString();
	}
	catch (...)
	{
		printf("AGMModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.first);
		AGMModelPrinter::printWorld(world);
		exit(-1);
	}
	try
	{
		b = world->getSymbol(symbolPair.second)->toString();
	}
	catch (...)
	{
		printf("AGMModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.second);
		AGMModelPrinter::printWorld(world);
		exit(-1);
	}

	label = linking;
}
