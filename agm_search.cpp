#include "agm_search.h"

AGMSearch::AGMSearch(const AGMModel::SPtr &current_, const AGMModel::SPtr &goal_)
{
	/// Initialization
	current = AGMModel::SPtr(new AGMModel(current_));
	goal = AGMModel::SPtr(new AGMModel(goal_));
	nodesToExplore.push_back(AGMSearchPath(current));

	/// Main loop
	while (not nodesToExplore.empty())
	{
		/// Expand best node
		try
		{
			AGMSearchPathList l = generateSearchFromBestNode();
		}
		catch (...)
		{
			printf("We should print here the target model\n");
			qFatal("We got to the target model!");
		}

		for (AGMSearchPathList::iterator iter=l.begin(); iter!=l.end(); iter++)
		{
		}
	}
	
	struct AGMRuleExecutionDescriptor
	{
		std::string ruleName;
		std::map< std::string, int32_t> symbolMapping;
	};
	struct AGMSearchPath
	{
		std::list< AGMRuleExecutionDescriptor > path;
		AGMModel::SPtr result;
	};
	// Model list
	typedef std::list<AGMSearchPath> AGMSearchPathList;
	// Mapping "integer ==> pathList" (used for storing the explored nodes)
	typedef std::map<int, AGMSearchPathList> AGMMapIntegerSearchPath;
	// Mapping "integer ==> integer2modelMap" (used for storing the explored nodes)
	typedef std::map<int, AGMMapIntegerSearchPath> AGMModelExploredMemory;



public:
	AGMSearch(const AGMModel::SPtr &current_, const AGMModel::SPtr &goal_);

private:
	AGMModel::SPtr current, goal;
	
	AGMSearchPathList nodesToExplore;
	AGMModelExploredMemory exploredNodes;
	AGMSearchPath result;

}

