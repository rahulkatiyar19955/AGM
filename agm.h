#pragma once

#include <agm_behavior.h>
#include <agm_model.h>


class AGM
{
public:
	AGM(std::string pddlFile_, std::string agmbdFile_);
	void print();

	bool checkModel(AGMModel::SPtr model);
	bool proposeModel(AGMModel::SPtr model);
	bool updateModel(AGMModelSymbol);

	std::string pddlProblemForTarget(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName);


// private:
	std::string pddlFile;
	AGMBehaviorDescription table;
	AGMActionToBehaviorMap action2behavior;
	AGMModel currentModel;
	void loadFromFile(std::string pddlFile, std::string agmbdFile);
};


