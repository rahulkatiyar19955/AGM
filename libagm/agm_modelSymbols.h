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
class AGMModelEdge;
class AGMModelSymbol;

/*!
	* @brief Iterator class for accessing the edges of a particular symbol.
	*
	* 
	* 
	*/
class edgeIterator
{
public:
	/// Constructor
	edgeIterator(AGMModel *m, AGMModelSymbol *s);

	/// Copy constructor
	edgeIterator(edgeIterator &iter);

	/// Access to the begin of the list.
	static edgeIterator begin(AGMModel *m, AGMModelSymbol *s);

	/// Access to an unaccessible element of the list.
	static edgeIterator end(AGMModel *m, AGMModelSymbol *s);

	/// Comparison operator
	bool operator==(const edgeIterator &rhs);

	/// Not-equal operator
	bool operator!=(const edgeIterator &rhs);

	/// Increment
	edgeIterator operator++();

	/// Parametrized increment
	edgeIterator operator++(int32_t times);

	/// Get referenced edge.
	AGMModelEdge operator*();

	/// Get referenced edge.
	AGMModelEdge operator->();

private:
	int32_t index;
	AGMModel *modelRef;
	AGMModelSymbol *symRef;
};

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

// 	edgeIterator edgesBegin(AGMModel *m) { return edgeIterator::begin(m, this); }
// 	edgeIterator edgesEnd(AGMModel *m) { return edgeIterator::end(m, this); }

	bool operator==(const AGMModelSymbol &p) const;

	std::string symbolType;
	int32_t identifier;
	std::map<std::string, std::string> attributes;

};



