#pragma once

#include <stdio.h>

#include <algorithm>
#include <boost/shared_ptr.hpp>
#include <boost/thread.hpp>

#include <agm_modelException.h>
#include <AGMWorldModel.h>

#include <agm_misc_functions.h>
#include <agm_modelSymbols.h>

class AGMModelEdge;
class AGMModelConverter;
class AGMModelSymbol;

class AGMModel
{
friend class AGMModelConverter;
friend class AGMModelSymbol;
public:
	typedef boost::shared_ptr<AGMModel> SPtr;

	AGMModel();
	~AGMModel();
	AGMModel(const AGMModel::SPtr &src);
	AGMModel(const AGMModel &src);
	AGMModel& operator=(const AGMModel &src);

	/// SET's
	void clear();
	bool removeSymbol(int32_t id);
	int32_t replaceIdentifierInEdges(int32_t a, int32_t b);

	AGMModelSymbol::SPtr newSymbol(std::string typ, int32_t id=-1)
	{
		AGMModelSymbol *s = new AGMModelSymbol(this, typ, id);
		return symbols[getIndexByIdentifier(s->identifier)];
	}
	AGMModelSymbol::SPtr newSymbol(int32_t identifier, std::string typ)
	{
		AGMModelSymbol *s = new AGMModelSymbol(this, identifier, typ);
		return symbols[getIndexByIdentifier(s->identifier)];
	}
	AGMModelSymbol::SPtr newSymbol(int32_t identifier, std::string typ, std::map<std::string, std::string> atr)
	{
		AGMModelSymbol *s = new AGMModelSymbol(this, identifier, typ, atr);
		return symbols[getIndexByIdentifier(s->identifier)];
	}

private:
	int32_t insertSymbol(AGMModelSymbol::SPtr s);
	int32_t insertSymbol(AGMModelSymbol *s) { return insertSymbol(AGMModelSymbol::SPtr(s)); }
	bool removeEdgesRelatedToSymbol(int32_t id);
public:
	std::string name;
	/// GET's
	AGMModelSymbol::SPtr getSymbol(int32_t identif) const;
	int32_t numberOfEdges() const;
	int32_t numberOfSymbols() const;
	int32_t indexOfSymbol(const AGMModelSymbol::SPtr &value, int32_t from=0) const;
	int32_t indexOfFirstSymbolByValues(const AGMModelSymbol &value, int32_t from=0) const;
	int32_t indexOfFirstSymbolByType(const std::string &value, int32_t from=0) const;
	std::vector<AGMModelSymbol::SPtr> getSymbols() const;
	std::vector<AGMModelEdge> getEdges() const;
	AGMModelSymbol::SPtr &symbol(uint32_t index);
	AGMModelEdge &edge(uint32_t index);

	int32_t getIdentifierByName(std::string name) const;
	int32_t getIdentifierByType(std::string type, int32_t i=0) const;
	int32_t getLinkedID(int32_t id, std::string linkname, int32_t i=0) const;
	int32_t getIndexByIdentifier(int32_t targetId) const;


	/// PLANNING RELATED !!
	std::string generatePDDLProblem(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName="problemName") const;

	void setSymbols(std::vector<AGMModelSymbol::SPtr> s);
	void setEdges(std::vector<AGMModelEdge> e);

	
	std::vector<AGMModelSymbol::SPtr> symbols;
	std::vector<AGMModelEdge> edges;
private:	
	void setFrom(const AGMModel &src);


/// ID
public:
	int32_t lastId;
	void resetLastId();
	int32_t getNewId();

};


