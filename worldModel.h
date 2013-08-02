#pragma once

#include <stdio.h>

#include <worldModelSymbols.h>
#include <worldModelException.h>
#include <WorldModel.h>

#include <algorithm>

#include <agm_misc_functions.h>

class WorldModelEdge;
class WorldModelConverter;

class WorldModel
{
friend class WorldModelConverter;
public:
	typedef boost::shared_ptr<WorldModel> SPtr;

	WorldModel();
	~WorldModel();
	WorldModel(const WorldModel::SPtr &src);
	WorldModel(const WorldModel &src);
	WorldModel& operator=(const WorldModel &src);

	/// SET's
	void clear();
	int32_t insertSymbol(WorldModelSymbol::SPtr s);
	void resetLastId();

	/// GET's
	WorldModelSymbol::SPtr getSymbol(int32_t identif) const;
	int32_t numberOfEdges() const;
	int32_t numberOfSymbols() const;
	int32_t indexOfSymbol(const WorldModelSymbol::SPtr &value, int32_t from=0) const;
	int32_t indexOfFirstSymbolByValues(const WorldModelSymbol &value, int32_t from=0) const;
	int32_t indexOfFirstSymbolByType(const std::string &value, int32_t from=0) const;
	std::vector<WorldModelSymbol::SPtr> getSymbols() const;
	std::vector<WorldModelEdge> getEdges() const;
	WorldModelSymbol::SPtr &symbol(uint32_t index);
	WorldModelEdge &edge(uint32_t index);

	int32_t getIdentifierByName(std::string name) const;
	int32_t getIdentifierByType(std::string type, int32_t i=0) const;
	int32_t getLinkedID(int32_t id, std::string linkname, int32_t i=0) const;
	int32_t getIndexByIdentifier(int32_t targetId) const;



	/// PLANNING RELATED !!
	std::string generatePDDLProblem(const WorldModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName="problemName") const;

	void setSymbols(std::vector<AGMModelSymbol::SPtr> s);
	void setEdges(std::vector<AGMModelEdge> e);

	
	std::vector<WorldModelSymbol::SPtr> symbols;
	std::vector<WorldModelEdge> edges;
private:
	void setFrom(const WorldModel &src);

};
