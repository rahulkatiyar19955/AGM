#include "agm_search.h"


AGMSearchPath::AGMSearchPath()
{
	result = AGMModel::SPtr(new AGMModel());
}


AGMSearchPath::AGMSearchPath(const AGMModel::SPtr &init)
{
	result = AGMModel::SPtr(new AGMModel(init));
}


void AGMSearchPath::includeExecution(const AGMRuleExecution &exec)
{
	path.push_back(exec);
}


void AGMSearchPath::print()
{
	uint32_t a = 0;
	for (std::list< AGMRuleExecution >::iterator iter=path.begin(); iter!=path.end(); iter++)
	{
		printf("%d --> ", a);
		iter->print();
		a++;
	}
}


bool AGMSearchPath::goalIsMet(const AGMModel::SPtr &goal)
{
	return AGMSearch::goalIsMet(result, goal);
}


void AGMSearchPath::clear()
{
	path.clear();
}




