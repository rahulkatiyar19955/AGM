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

/*!
 * @brief Nodes --symbols-- of AGMModel graphs
 *
 * 
 * 
 */
class AGMModelSymbol
{
friend class AGMModel;
private:
	AGMModelSymbol(AGMModel *model, std::string typ, int32_t id=-1);
	AGMModelSymbol(AGMModel *model, int32_t identifier, std::string typ);
	AGMModelSymbol(AGMModel *model, int32_t identifier, std::string typ, std::map<std::string, std::string> atr);
	AGMModelSymbol(boost::shared_ptr<AGMModel> model, std::string typ, int32_t id=-1);
	AGMModelSymbol(boost::shared_ptr<AGMModel> model, int32_t identifier, std::string typ);
	AGMModelSymbol(boost::shared_ptr<AGMModel> model, int32_t identifier, std::string typ, std::map<std::string, std::string> atr);
public:
	~AGMModelSymbol();
private:
	void init(AGMModel *model, std::string typ, int32_t id=-1);
	void init(AGMModel *model, int32_t identifier, std::string typ);
	void init(AGMModel *model, int32_t identifier, std::string typ, std::map<std::string, std::string> atr);
public:	
	typedef boost::shared_ptr<AGMModelSymbol> SPtr;

	std::string toString() const;
	std::string typeString() const;
	std::string symboltype() const { return symbolType; }

	void setType(std::string t);
	void setIdentifier(int32_t t);
	void setAttribute(std::string a, std::string v);
	std::string getAttribute(std::string a);

	bool operator==(const AGMModelSymbol &p) const;

	std::string symbolType;
	int32_t identifier;
	std::map<std::string, std::string> attributes;

};



