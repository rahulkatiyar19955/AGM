#include "agm_behavior.h"


class AGM
{
public:
	AGM(std::string pddlFile, std::string agmbdFile);
	void print();

// 	checkModel
// 	updateModel
// 	acceptModel
	
private:
	AGMBehaviorDescription table;
	void loadFromFile(std::string pddlFile, std::string agmbdFile);
};


