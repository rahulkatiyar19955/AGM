#include "agm.h"

int main(int argc, char **argv)
{
	if (argc < 4)
	{
		printf("Usage %s grammarFile.aggl currentWorld.xml goalPattern.xml\n", argv[0]);
		return -1;
	}

	
	AGM *agm = new AGM(argv[1], "", "");	
	printf("\nAttributes read:\n");
	for (std::map<std::string, std::string>::iterator iter=agm->attributes.begin(); iter!=agm->attributes.end(); iter++)
	{
		printf("%s --> %s\n", iter->first.c_str(), iter->second.c_str());
	}

	printf("\nRules read:\n");
	for (uint32_t ruleNumber=0; ruleNumber<agm->size(); ++ruleNumber)
	{
		printf("Rule[%d]:\n", ruleNumber);
		agm->rule(ruleNumber).print();
	}

	AGMModel::SPtr world(new AGMModel());
	AGMModelConverter::fromXMLToInternal(argv[2], world);
	AGMModel::SPtr goal(new AGMModel());
	AGMModelConverter::fromXMLToInternal(argv[3], goal);

	printf("Goal met: %d\n", AGMSearch::goalIsMet(world, goal));

	return 0;
}

