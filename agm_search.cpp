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

		const int32_t headSize = head.result->symbols.size();

		/// Generate each possible matching for every possible rule
		for (uint32_t ruleNumber=0; ruleNumber<agm->size(); ++ruleNumber)
		{
			std::vector<int32_t> world2rule;
			std::vector<int32_t> rule2world;
			const int32_t lhsSize = agm->rules[ruleNumber].lhsSymbolsNames.size();
			world2rule.resize(lhsSize);
			rule2world.resize(lhsSize);
			for (int32_t p=0; p<lhsSize; p++)
			{
				if (p<lhsSize-1) world2rule[p] = 0;
				else world2rule[p] = -1;
			}
			try
			{
				while (1)
				{
					// Increment match to a possible compatible changes (it ensures that SOME of the symbols match types)
					int32_t sum = 1;
					while (1)
					{
						world2rule[lhsSize-sum] += 1;
						if (world2rule[lhsSize-sum] >= headSize) // If we to the last element of the first number, break
							break;
						if (agm->rules[ruleNumber].lhsSymbolsTypes[lhsSize-sum] == head.result->symbols[world2rule[lhsSize-sum]]->symbolType) // If the type is valid, break
							break;
					}
					while (world2rule[lhsSize-sum] == headSize) // If we got to the last element of the first number continue with the ones on the left
					{
						world2rule[lhsSize-sum] = 0; // Aquí nos podríamos asegurar de que el 0 es un buen matching, pero ya demasiado complicado es el código...
						sum += 1;
						if (sum > lhsSize) { throw std::string("end"); }
						world2rule[lhsSize-sum]+=1;
					}
					bool goodMatch = true;
					for (int32_t e=0; e<lhsSize; e++) {
						if (agm->rules[ruleNumber].lhsSymbolsTypes[e] != head.result->symbols[world2rule[e]]->symbolType) {
							goodMatch = false;
							break;
						}
					}
					if (not goodMatch) continue;
					for (int32_t i=0; i<lhsSize; i++)
					{
						rule2world[world2rule[i]] = i;
					}
					/// RULE TRIGGERING CODE BEGINS
					// 0 Here we have a symbol->symbol match (of the symbols in the LHS)
					// 1 Verify that we have all the links specified in the LHS
					// 2 Append symbols to create
					// 3 Remove symbols to delete
					// 4 Append links to create
					// 5 Remove links to delete
					// 6 Create a new path by appending the new rule triggering to the current path
					// 7 Append the created path to the list
					// There we go...
					// for (int32_t e=0; e<lhsSize; e++)
					// 	agm->rules[ruleNumber].lhsSymbolsTypes[e] == head.result->symbols[match[e]]->symbolType

					// 1 Verify that we have all the links specified in the LHS

					// 2 Append symbols to create

					// 3 Remove symbols to delete

					// 4 Append links to create

					// 5 Remove links to delete

					// 6 Create a new path by appending the new rule triggering to the current path

					// 7 Append the created path to the list

					/// MATCH SUCCESS CODE ENDS
				}
			}
			catch (std::string e)
			{
				if (e != "end")
					std::cout << e << std::endl;
			}
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
	for (int32_t p=0; p<goalSize; p++)
	{
		if (p<goalSize-1)
			match[p] = 0;
		else
			match[p] = -1;
	}
	try
	{
		while (1)
		{
			// Increment match to a possible compatible changes (it ensures that SOME of the symbols match types)
			int32_t sum = 1;
			while (1)
			{
				match[goalSize-sum] += 1;
				if (match[goalSize-sum] >= worldSize) // If we to the last element of the first number, break
					break;
				if (goal->symbols[goalSize-sum]->symbolType == world->symbols[match[goalSize-sum]]->symbolType) // If the type is valid, break
					break;
			}
			while (match[goalSize-sum] == worldSize) // If we got to the last element of the first number continue with the ones on the left
			{
				match[goalSize-sum] = 0; // Aquí nos podríamos asegurar de que el 0 es un buen matching, pero ya demasiado complicado es el código...
				sum += 1;
				if (sum > goalSize) { throw std::string("end"); }
				match[goalSize-sum]+=1;
			}
			bool goodMatch = true;
			for (int32_t e=0; e<goalSize; e++) {
				if (goal->symbols[e]->symbolType != world->symbols[match[e]]->symbolType) {
					goodMatch = false;
					break;
				}
			}
			if (not goodMatch) continue;
			/// MATCH SUCCESS CODE BEGINS
			// equals
			for (int i=0; i<goalSize; i++) {
				for (int j=i+1; j<goalSize; j++) {
					if (match[i] == match[j]) {
						if (not canBeEqual(goal, goal->symbols[i]->identifier, goal->symbols[j]->identifier)) {
							i = j = goalSize + 1; // This breaks the loop as well
							goodMatch = false;
							break;
						}
					}
				}
			}
			if (not goodMatch) continue;
			// links
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
				for (uint32_t l2=0; l2<world->edges.size(); l2++) {
					if (world->edges[l2].symbolPair.first == id1W) {
						if (world->edges[l2].symbolPair.second == id2W) {
							if (world->edges[l2].linking == goal->edges[l1].linking) {
								linkFound = true;
								break;
							}
						}
					}
				}
				if (not linkFound) {
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
			/// MATCH SUCCESS CODE ENDS
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
















