#pragma once

#include <stdint.h>

#include <string>
#include <vector>
#include <map>
#include <utility>

#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>

class WorldModel;
class WorldModelConverter;

class WorldModelSymbol
{
	
public:
	WorldModelSymbol();
	WorldModelSymbol(std::string ntype, int32_t id=-1);
	WorldModelSymbol(int32_t identifier, std::string typ);
	WorldModelSymbol(int32_t identifier, std::string typ, std::map<std::string, std::string> atr);
	~WorldModelSymbol();
	
	typedef boost::shared_ptr<WorldModelSymbol> SPtr;

	std::string toString() const;
	std::string typeString() const;
	std::string symboltype() { return symbolType; };

	void setType(std::string t);
	void setIdentifier(int32_t t);
	void setAttribute(std::string a, std::string v);
	std::string getAttribute(std::string a);

	bool operator==(const WorldModelSymbol &p) const;

	std::string symbolType;
	int32_t identifier;
	std::map<std::string, std::string> attributes;

private:
	static int32_t lastId;
	static boost::mutex mutex;
protected:
	static int32_t getNewId();
public:
	static int32_t getLastId();
	static void resetIDs() { WorldModelSymbol::lastId = 0; }
	static void setLastID(int32_t last) { WorldModelSymbol::lastId = last; }
};



