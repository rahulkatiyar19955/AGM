#pragma once

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
	AGMModelSymbol(std::string typ);
	AGMModelSymbol(int32_t identifier, std::string typ);
	AGMModelSymbol(int32_t identifier, std::string typ, std::map<std::string, std::string> atr);
	~AGMModelSymbol();
	
	typedef boost::shared_ptr<AGMModelSymbol> SPtr;

	std::string toString() const;

	std::string typeString() const;
	std::string symboltype() const;
	void setType(std::string t);
	
	
	void setIdentifier(int32_t t);
	void setAttribute(std::string a, std::string v);
	std::string getAttribute(std::string a);

	bool operator==(const AGMModelSymbol &p) const;






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
	static void resetIDs() { AGMModelSymbol::lastId = 0; }
	static void setLastID(int32_t last) { AGMModelSymbol::lastId = last; }
};



