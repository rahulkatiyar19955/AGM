#ifndef WORLDMODELSYMBOLS_H
#define WORLDMODELSYMBOLS_H

#include <stdint.h>

#include <string>
#include <vector>
#include <map>
#include <utility>

#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>

class AGMModel;
class AGMModelConverter;

class AGMModelSymbol
{
	
public:
	AGMModelSymbol();
	AGMModelSymbol(int32_t identifier, std::string typ, std::map<std::string, std::string> atr);
	~AGMModelSymbol();
	
	typedef boost::shared_ptr<AGMModelSymbol> SPtr;

	std::string symbolType;
	int32_t identifier;
	std::map<std::string, std::string> attributes;

	std::string toString() const;
	std::string typeString() const;
	std::string symboltype() { return ""; }

	bool operator==(const AGMModelSymbol &p) const;
private:
	static int32_t lastId;
	static boost::mutex mutex;
protected:
	static int32_t getNewId();
public:
	static int32_t getLastId();
	static void resetIDs() { AGMModelSymbol::lastId = 0; }
	static void setLastID(int32_t last) { AGMModelSymbol::lastId = last; }
};




#endif
