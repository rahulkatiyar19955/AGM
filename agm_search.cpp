// #include "agm_search.h"
// 
// AGMSearch::AGMSearch(const AGMModel::SPtr &current_, const AGMModel::SPtr &goal_)
// {
// 	/// Initialization
// 	current = AGMModel::SPtr(new AGMModel(current_));
// 	goal = AGMModel::SPtr(new AGMModel(goal_));
// 	nodesToExplore.push_back(AGMSearchPath(current));
// 
// 	/// Check goal
// 	if (goalIsMet(goal, current))
// 	{
// 		printf("0\n");
// 		throw "We are already there!";
// 	}
// 	
// 	/// Main loop
// 	while (not nodesToExplore.empty())
// 	{
// 		/// Expand best node
// 		try
// 		{
// 			AGMSearchPathList l = expandBestNode();
// 		}
// 		catch (...)
// 		{
// 			printf("We should print here the target model\n");
// 			qFatal("We got to the target model!");
// 		}
// 
// 		for (AGMSearchPathList::iterator iter=l.begin(); iter!=l.end(); iter++)
// 		{
// 		}
// 	}
// 	
// 	AGMSearchPathList nodesToExplore;
// 	AGMModelExploredMemory exploredNodes;
// 	AGMSearchPath result;
// 
// }
// 
// 
// AGMSearchPathList AGMSearch::expandBestNode()
// {
// 	AGMSearch head = nodesToExplore.pop();
// 
// 	for (int32_t r=0; r<reglas; ++r)
// 	{
// 		for (int32_t rL=0; rL<ruleL; ++rL)
// 		{
// 			for (int32_t rR=0; rR<ruleR; ++rR)
// 			{
// 			}
// 	}
// }
// 
