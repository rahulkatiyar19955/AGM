#include "agm.h"
#include "agm_search.h"

AGMSearch::AGMSearch(const boost::shared_ptr<AGM> &agm_)
{
	//Initialization
	agm = AGM::SPtr(new AGM(agm_));
}

bool AGMSearch::go(const AGMModel::SPtr &current_, const AGMModel::SPtr &goal_, AGMSearchPath &result)
{
	// Initialize result
	current = AGMModel::SPtr(new AGMModel(current_));
	goal = AGMModel::SPtr(new AGMModel(goal_));
	nodesToExplore.push_back(AGMSearchPath(current));

	//Check goal
	if (goalIsMet(goal, current))
	{
		result = AGMSearchPath(current);
		return true;
	}

	//Main loop
	while (not nodesToExplore.empty())
	{
		//Expand best node
		AGMSearchPathList l;
		l = expandBestNodeAndRemoveItFromTheNodesToExplore();
		//Check if anyone of the expanded nodes meet goal's conditions and (if not)
		//include them in the "nodes to explore" list.
		for (AGMSearchPathList::iterator iter=l.begin(); iter!=l.end(); iter++)
		{
			if (iter->goalIsMet(goal))
			{
				printf("GOAL MET:\n");
				iter->print();
			}
			else
			{
				nodesToExplore.push_back(*iter);
			}
		}
	}
	
	AGMSearchPathList nodesToExplore;
	AGMModelExploredMemory exploredNodes;
	return false;
}


AGMSearchPathList AGMSearch::expandBestNodeAndRemoveItFromTheNodesToExplore()
{
	AGMSearchPathList ret;

	if (nodesToExplore.size() > 0)
	{
		// This should be an ordered list (in the meantime... it's ok)
		AGMSearchPath head = nodesToExplore.front();
		nodesToExplore.pop_front();

		for (uint32_t r=0; r<agm->size(); ++r)
		{
/*
			for (int32_t rL=0; rL<ruleL; ++rL)
			{
				for (int32_t rR=0; rR<ruleR; ++rR)
				{
				}
			}
*/
		}
	}
	return ret;
}


bool AGMSearch::goalIsMet(const AGMModel::SPtr &world, const AGMModel::SPtr &goal)
{
	// If the world is smaller than the goal we have certainly not achieved the goal
	// BUG ERROR FIX WARNING THIS WILL NOT HOLD WHEN USING POTENTIALLY EQUAL VARIABLES!
	// BUG ERROR FIX WARNING THIS WILL NOT HOLD WHEN USING POTENTIALLY EQUAL VARIABLES!
	// BUG ERROR FIX WARNING THIS WILL NOT HOLD WHEN USING POTENTIALLY EQUAL VARIABLES!
	if (goal->symbols.size()>world->symbols.size() or goal->symbols.size()>world->symbols.size() )
		return false;

	// In this part we generate possible matchings
	std::vector<int32_t> match;
	const int32_t goalSize  =  goal->symbols.size();
	const int32_t worldSize = world->symbols.size();
	match.resize(goalSize);
	try
	{
		while (1)
		{
			/// MATCH SUCCESS CODE BEGINS
			bool goodMatch = true;
			for (int32_t e=0; e<goalSize; e++)
			{
				if (goal->symbols[e]->symbolType != world->symbols[match[e]]->symbolType)
				{
					goodMatch = false;
					break;
				}
			}
			if (goodMatch)
			{
				for (int i=0; i<goalSize; i++)
				{
					for (int j=i+1; j<goalSize; j++)
					{
						if (match[i] == match[j])
						{
							if (not canBeEqual(goal, goal->symbols[i]->identifier, goal->symbols[j]->identifier))
							{
								i = j = goalSize + 1; // This breaks the loop as well
								goodMatch = false;
								break;
							}
						}
					}
				}

				if (goodMatch)
				{
					std::map<int, int> goalId2Index;
					for (int32_t  e=0; e< goalSize; e++)
						goalId2Index[ goal->symbols[e]->identifier] = e;
					for (uint32_t l1=0; l1<goal->edges.size(); l1++)
					{
						const int32_t id1G = goal->edges[l1].symbolPair.first;
						const int32_t id2G = goal->edges[l1].symbolPair.second;
						const int32_t id1W = world->symbols[match[goalId2Index[id1G]]]->identifier;
						const int32_t id2W = world->symbols[match[goalId2Index[id2G]]]->identifier;
						bool linkFound = false;
						for (uint32_t l2=0; l2<world->edges.size(); l2++)
						{
							if (world->edges[l2].symbolPair.first == id1W)
							{
								if (world->edges[l2].symbolPair.second == id2W)
								{
									if (world->edges[l2].linking == goal->edges[l1].linking)
									{
										linkFound = true;
										break;
									}
								}
							}
						}
						if (not linkFound)
						{
							printf("No link:   %d---[%s]--->%d\n", id1G, goal->edges[l1].linking.c_str(), id2G);
							goodMatch = false;
							break;
						}
					}
					if (goodMatch)
					{
						// Print match
						for (int32_t  e=0; e< goalSize; e++)
							printf("[%d-->%d] ", goal->symbols[e]->identifier, world->symbols[match[e]]->identifier);
						printf("\n");
						return true;
					}
					else
					{
					}
				}
			}
			/// MATCH SUCCESS CODE ENDS

			/// KEEP LOOKING FOR ANOTHER POSSIBLE MATCH
			// Increment match
			match[goalSize-1]+=1;
			// Propagate increment to higher numbers
			int32_t sum = 1;
			while (match[goalSize-sum] == worldSize)
			{
				match[goalSize-sum] = 0;
				sum+=1;
				if (sum > goalSize) { throw std::string("end"); }
				match[goalSize-sum]+=1;
			}
		}
	}
	catch (std::string e)
	{
		if (e != "end")
			std::cout << e << std::endl;
		// Goal wasn't met
		return false;
	}

	return false;
}
















