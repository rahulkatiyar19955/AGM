#pragma once

// #include <agm_behavior.h>
#include <agm_model.h>
#include <agm_modelSymbols.h>
#include <agm_modelEdge.h>
#include <agm_modelConverter.h>
#include <agm_search.h>
#include <agm_rule.h>


bool parseAGGL(const char *path, AGM *agm, std::vector <AGGLRule> *rules);

class AGM
{
friend class AGMSearch;
public:
	typedef boost::shared_ptr<AGM> SPtr;
	AGM(const AGM::SPtr &src);
	AGM(std::string agglfile, std::string pddlFileFull_, std::string pddlFilePartial_);
	void print();

	//* 
	bool checkModel(AGMModel::SPtr model);
	bool proposeModel(AGMModel::SPtr model);
	bool updateModel(AGMModelSymbol);

	std::string pddlProblemForTarget(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName);

// private:
	std::string pddlFileFull, pddlFilePartial;
	std::string fullPDDLContent, partialPDDLContent;
	AGMModel currentModel;
	void loadFromFile(std::string pddlFileFull_, std::string pddlFilePartial_);

	AGGLRule &rule(int);
	uint32_t size() { return rules.size(); }
	
	void addAttribute(std::string key, std::string value);
	void addAttribute(const char *key, const char *value);
	void addAttribute(std::string key, int value);
	void addAttribute(const char *key, int value);
	std::map<std::string, std::string> attributes;
private:
	void readFileToString(std::string &file, std::string &content);
	std::vector <AGGLRule> rules;
};


