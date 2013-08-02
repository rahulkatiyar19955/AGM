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
	~WorldModelSymbol();
	
	typedef boost::shared_ptr<WorldModelSymbol> SPtr;

	std::string symbolType;
	int32_t identifier;
	std::map<std::string, std::string> attributes;

	std::string toString() const;
	std::string typeString() const;
	std::string symboltype() { return symbolType; };

	bool operator==(const WorldModelSymbol &p) const;
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



