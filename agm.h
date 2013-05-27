#include "agm_behavior.h"
#include "agm_model.h"


class AGM
{
public:
	AGM(std::string pddlFile_, std::string agmbdFile_);
	void print();

	bool checkModel(AGMModel::SPtr model);
// 	updateModel
// 	acceptModel
	
private:
	std::string pddlFile;
	AGMBehaviorDescription table;
	AGMModel currentModel;
	void loadFromFile(std::string pddlFile, std::string agmbdFile);
};


