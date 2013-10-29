#pragma once

#include <agm_behavior.h>
#include <agm_model.h>
#include <agm_modelSymbols.h>
#include <agm_modelEdge.h>
#include <agm_modelConverter.h>
#include <agm_search.h>


class AGGLRule
{
public:
	// LHS
	std::vector<AGMModelSymbol::SPtr> lhsSymbols;
	std::vector<AGMModelEdge> lhsLinks;
	// Effect
	std::vector<AGMModelSymbol::SPtr> symbolsToCreate;
	std::vector<AGMModelSymbol::SPtr> symbolsToRemove;
	std::vector<AGMModelEdge> linksToAdd;
	std::vector<AGMModelEdge> linksToRemove;
};

class AGM
{
friend class AGMSearch;
public:
	typedef boost::shared_ptr<AGM> SPtr;
	AGM(const AGM::SPtr &src);
	AGM(std::string pddlFileFull_, std::string pddlFilePartial_);
	void print();

	bool checkModel(AGMModel::SPtr model);
	bool proposeModel(AGMModel::SPtr model);
	bool updateModel(AGMModelSymbol);

	std::string pddlProblemForTarget(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName);

// private:
	std::string pddlFileFull, pddlFilePartial;
	std::string fullPDDLContent, partialPDDLContent;
	AGMModel currentModel;
	void loadFromFile(std::string pddlFileFull_, std::string pddlFilePartial_);

	const AGGLRule &rule(int);
	uint32_t size() { return rules.size(); }
private:
	void readFileToString(std::string &file, std::string &content);
	std::vector <AGGLRule> rules;
};


