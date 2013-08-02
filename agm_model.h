#pragma once

#include <stdio.h>

#include <agm_modelSymbols.h>
#include <agm_modelException.h>
#include <WorldModel.h>

#include <algorithm>

#include <agm_misc_functions.h>

class AGMModelEdge;
class AGMModelConverter;

class AGMModel
{
friend class AGMModelConverter;
public:
	typedef boost::shared_ptr<AGMModel> SPtr;

	AGMModel();
	~AGMModel();
	AGMModel(const AGMModel::SPtr &src);
	AGMModel(const AGMModel &src);
	AGMModel& operator=(const AGMModel &src);

	/// SET's
	void clear();
	int32_t insertSymbol(AGMModelSymbol::SPtr s);
	void resetLastId();

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


	float string2float(const std::string &s) const { return ::str2float(s); }


	/// PLANNING RELATED !!
	std::string generatePDDLProblem(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName="problemName") const;

	void setSymbols(std::vector<AGMModelSymbol::SPtr> s);
	void setEdges(std::vector<AGMModelEdge> e);

	
	std::vector<AGMModelSymbol::SPtr> symbols;
	std::vector<AGMModelEdge> edges;
private:	
	void setFrom(const AGMModel &src);

};
