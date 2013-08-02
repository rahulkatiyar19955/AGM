#include "worldModelEdge.h"
#include "worldModelPrinter.h"

WorldModelEdge::WorldModelEdge()
{
	symbolPair = std::pair<int32_t, int32_t>(0, 0);
	linking = "-";
}

WorldModelEdge::WorldModelEdge(const WorldModelEdge &src)
{
	setFrom(src);
}

WorldModelEdge::WorldModelEdge(int32_t a, int32_t b, std::string linking_)
{
	symbolPair = std::pair<int32_t, int32_t>(a, b);
	linking = linking_;
}

WorldModelEdge::~WorldModelEdge()
{
	symbolPair = std::pair<int32_t, int32_t>(0, 0);
	linking = "-";
}

WorldModelEdge& WorldModelEdge::operator=(const WorldModelEdge &src)
{
	this->setFrom(src);
	return *this;
}

void WorldModelEdge::setFrom(const WorldModelEdge &src)
{
	linking = src.linking;
	symbolPair = src.symbolPair;
}



std::string WorldModelEdge::toString(const WorldModel::SPtr &world) const
{
	return toString(world.get());
}


std::string WorldModelEdge::toString(const WorldModel *world) const
{
	std::ostringstream stringStream;
	std::string stringA, stringB;

	try
	{
		stringA = world->getSymbol(symbolPair.first)->toString();
	}
	catch (...)
	{
		printf("WorldModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.first);
		WorldModelPrinter::printWorld(world);
		exit(-1);
	}
	try
	{
		stringB = world->getSymbol(symbolPair.second)->toString();
	}
	catch (...)
	{
		printf("WorldModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.second);
		WorldModelPrinter::printWorld(world);
		exit(-1);
	}

	stringStream << linking << " " << stringA << " " << stringB;
	return stringStream.str();
}

void WorldModelEdge::getStrings(const WorldModel::SPtr &world, std::string &label, std::string &a, std::string &b) const
{
	getStrings(world.get(), label, a, b);
}

void WorldModelEdge::getStrings(const WorldModel *world, std::string &label, std::string &a, std::string &b) const
{
	try
	{
		a = world->getSymbol(symbolPair.first)->toString();
	}
	catch (...)
	{
		printf("WorldModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.first);
		WorldModelPrinter::printWorld(world);
		exit(-1);
	}
	try
	{
		b = world->getSymbol(symbolPair.second)->toString();
	}
	catch (...)
	{
		printf("WorldModel error: it probably lacks of a node with %d as identifier!!!\n", symbolPair.second);
		WorldModelPrinter::printWorld(world);
		exit(-1);
	}

	label = linking;
}



