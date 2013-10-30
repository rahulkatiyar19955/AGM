#include "agm.h"
#include "agm_search.h"
#include "agm_modelPrinter.h"

AGMSearch::AGMSearch(const boost::shared_ptr<AGM> &agm_)
{
	//Initialization
	agm = agm_;
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

	printf("nodesToExplore: %ld\n", nodesToExplore.size());

	//Main loop
	uint32_t nodes=0;
	while (not nodesToExplore.empty())
	{
		nodes++;
		printf("%d\n", nodes);
		//Expand best node
		AGMSearchPathList l;
		l = expandBestNodeAndRemoveItFromTheNodesToExplore();
		printf("expanded: %ld\n", l.size());
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
		printf("Processing:\n");
		AGMModelPrinter::printWorld(head.result);
		nodesToExplore.pop_front();

		const int32_t headSize = head.result->symbols.size();

		/// Generate each possible matching for every possible rule
		for (uint32_t ruleNumber=0; ruleNumber<agm->size(); ++ruleNumber)
		{
// 			printf("RULE %s\n", agm->rules[ruleNumber].name.c_str());
// 			printf("links %ld\n", agm->rules[ruleNumber].lhsLinksLabel.size());
			std::vector<int32_t> match;
			const int32_t lhsSize = agm->rules[ruleNumber].lhsSymbolsNames.size();
			match.resize(lhsSize);
			for (int32_t p=0; p<lhsSize; p++)
			{
				if (p<lhsSize-1) match[p] = 0;
				else match[p] = -1;
			}
			try
			{
				while (1)
				{
					// Increment match to a possible compatible changes (it ensures that SOME of the symbols match types)
					int32_t sum = 1;
					while (1)
					{
						match[lhsSize-sum] += 1;
						if (match[lhsSize-sum] >= headSize) // If we to the last element of the first number, break
							break;
						if (agm->rules[ruleNumber].lhsSymbolsTypes[lhsSize-sum] == head.result->symbols[match[lhsSize-sum]]->symbolType) // If the type is valid, break
							break;
					}
					while (match[lhsSize-sum] == headSize) // If we got to the last element of the first number continue with the ones on the left
					{
						match[lhsSize-sum] = 0; // Aquí nos podríamos asegurar de que el 0 es un buen matching, pero ya demasiado complicado es el código...
						sum += 1;
						if (sum > lhsSize) { throw std::string("end"); }
						match[lhsSize-sum]+=1;
					}
					bool goodMatch = true;
					std::map<int32_t, int32_t> rule2world, world2rule;
					for (int32_t i=0; i<lhsSize; i++)
					{
						rule2world[i] = match[i];
					}
					for (int32_t i=0; i<lhsSize; i++)
					{
						world2rule[match[i]] = i;
					}
					try
					{
						for (int32_t e=0; e<lhsSize; e++) {
							if (agm->rules[ruleNumber].lhsSymbolsTypes[e] != head.result->symbols[rule2world.at(e)]->symbolType) {
								goodMatch = false;
								break;
							}
						}
					}
					catch (...)
					{
// 						printf("nooo\n");
					}
					if (not goodMatch) continue;

// 					printf("Type-based match!!!\n");
// 					printf("Match: ");
// 					for (int32_t i=0; i<lhsSize; i++)
// 						printf("%d->%d   ", i, match[i]);
// 					printf("\n");


					/// RULE TRIGGERING CODE BEGINS
					// 0 Here we have a symbol->symbol match (of the symbols in the LHS)
					// 1 Verify that we have all the links specified in the LHS
					// 2 Append symbols to create
					// 3 Remove symbols to delete
					// 4 Update symbols to retype
					// 5 Append links to create
					// 6 Remove links to delete
					// 7 Create a new path by appending the new rule triggering to the current path
					// 8 Append the created path to the list  ***IF ITS NOT IN THE MEMORY OF WATCHED NODES***
					// There we go...
					// for (int32_t e=0; e<lhsSize; e++)
					// 	agm->rules[ruleNumber].lhsSymbolsTypes[e] == head.result->symbols[match[e]]->symbolType

					/// 1 Verify that we have all the links specified in the LHS
					bool foundAllLinks = true;
					for (uint32_t i=0; i<agm->rules[ruleNumber].lhsLinksLabel.size() and foundAllLinks; i++)
					{
// 						printf("%s===[%s]===>%s\n", agm->rules[ruleNumber].lhsLinksA[i].c_str(), agm->rules[ruleNumber].lhsLinksLabel[i].c_str(), agm->rules[ruleNumber].lhsLinksB[i].c_str());
// 						printf(" edges %ld\n", head.result->edges.size());
// 						printf(" symbols %ld\n", head.result->symbols.size());
						bool found = false;
						for (uint32_t j=0; j<head.result->edges.size() and not found; j++)
						{
							if (agm->rules[ruleNumber].lhsLinksLabel[i] == head.result->edges[j].linking)
							{
								const int32_t fW_identifier = head.result->edges[j].symbolPair.first;
								const int32_t sW_identifier = head.result->edges[j].symbolPair.second;
								std::map<int32_t, int32_t>::iterator fRiter_index = world2rule.find(head.result->getIndexByIdentifier(fW_identifier));
								std::map<int32_t, int32_t>::iterator sRiter_index = world2rule.find(head.result->getIndexByIdentifier(sW_identifier));
// 								printf("  W %d->%d\n", fW_identifier, sW_identifier);
								if (fRiter_index == world2rule.end() or sRiter_index == world2rule.end() )
								{
// 									printf("   nope\n");
									continue;
								}
								const int32_t fR = fRiter_index->second;
								const int32_t sR = sRiter_index->second;
// 								printf("  R %d->%d\n", fR, sR);
// 								printf("   %d>>>[%s]>>>%d\n", fR,  head.result->edges[ j].linking.c_str(), sR);
// 								printf("   %s---[%s]--->%s\n",
// 									agm->rules[ruleNumber].lhsSymbolsNames[fR].c_str(),
// 									head.result->edges[ j].linking.c_str(),
// 									agm->rules[ruleNumber].lhsSymbolsNames[sR].c_str()
// 								);
								if (agm->rules[ruleNumber].lhsLinksA[i] == agm->rules[ruleNumber].lhsSymbolsNames[fR])
								{
									if (agm->rules[ruleNumber].lhsLinksB[i] == agm->rules[ruleNumber].lhsSymbolsNames[sR])
									{
										found = true;
									}
								}
							}
						}
						if (not found)
						{
							foundAllLinks = false;
							break;
						}
					}
					if (foundAllLinks)
					{
						printf("   Found all links:  %s!!!\n", agm->rules[ruleNumber].name.c_str());
					}
					else
					{
						continue;
					}

// 					printf("   Match: ");
// 					for (int32_t i=0; i<lhsSize; i++)
// 						printf("%d->%d   ", i, match[i]);
// 					printf("\n");


					AGMSearchPath newSearchNode = head; ///    :_-)
					std::map<std::string, int32_t> names2worldIndex;
					std::map<std::string, int32_t> names2worldIdentifier;
					/// 2 Append symbols to create
					for (uint32_t i=0; i<agm->rules[ruleNumber].symbolsToCreateType.size(); i++)
					{
						printf("Add a %s\n", agm->rules[ruleNumber].symbolsToCreateType[i].c_str());
						names2worldIndex     [agm->rules[ruleNumber].symbolsToCreateName[i]] = newSearchNode.result->symbols.size();
						AGMModelSymbol::SPtr n = newSearchNode.result->newSymbol(agm->rules[ruleNumber].symbolsToCreateType[i]);
						names2worldIdentifier[agm->rules[ruleNumber].symbolsToCreateName[i]] = n->identifier;
					}

					/// 3 Remove symbols to delete
					for (uint32_t i=0; i<agm->rules[ruleNumber].symbolsToRemove.size(); i++)
					{
						const int32_t removeLHS_index = agm->rules[ruleNumber].symbolsToRemoveID[i];
						const int32_t removeWorld_index = rule2world[removeLHS_index];
						const int32_t world_identifier = newSearchNode.result->symbols[removeWorld_index]->identifier;
						names2worldIndex[agm->rules[ruleNumber].symbolsToRemove[i]] = removeWorld_index;
						names2worldIdentifier[agm->rules[ruleNumber].symbolsToRemove[i]] = world_identifier;
						newSearchNode.result->removeSymbol(world_identifier);
					}

					/// 4 Update symbols to retype
					for (uint32_t i=0; i<agm->rules[ruleNumber].symbolsToRetypeName.size(); i++)
					{
						const int32_t retypeLHS_index = agm->rules[ruleNumber].symbolsToRetypeID[i];
						const int32_t retypeWorld_index = rule2world[retypeLHS_index];
						const int32_t world_identifier = newSearchNode.result->symbols[retypeWorld_index]->identifier;
						names2worldIndex[agm->rules[ruleNumber].symbolsToRetypeName[i]] = retypeWorld_index;
						names2worldIdentifier[agm->rules[ruleNumber].symbolsToRetypeName[i]] = world_identifier;
						newSearchNode.result->symbols[retypeWorld_index]->symbolType = agm->rules[ruleNumber].symbolsToRetypeType[i];
					}

					

					/// 5 Append links to create
					for (uint32_t i=0; i<agm->rules[ruleNumber].addLinksA.size(); i++)
					{
						const std::string label = agm->rules[ruleNumber].addLinksLabel[i];
						const int32_t aLHS_index = agm->rules[ruleNumber].addLinksAID[i];
						const int32_t aWorld_index = rule2world[aLHS_index];
						const int32_t aWID = newSearchNode.result->symbols[aWorld_index]->identifier;
						const int32_t bLHS_index = agm->rules[ruleNumber].addLinksBID[i];
						const int32_t bWorld_index = rule2world[bLHS_index];
						const int32_t bWID = newSearchNode.result->symbols[bWorld_index]->identifier;
						AGMModelEdge edge(aWID, bWID, label);
					}

					/// 6 Remove links to delete
					for (uint32_t i=0; i<agm->rules[ruleNumber].remLinksA.size(); i++)
					{
						const std::string label = agm->rules[ruleNumber].remLinksLabel[i];
						const int32_t aLHS_index = agm->rules[ruleNumber].remLinksAID[i];
						const int32_t aWorld_index = rule2world[aLHS_index];
						const int32_t aWID = newSearchNode.result->symbols[aWorld_index]->identifier;
						const int32_t bLHS_index = agm->rules[ruleNumber].remLinksBID[i];
						const int32_t bWorld_index = rule2world[bLHS_index];
						const int32_t bWID = newSearchNode.result->symbols[bWorld_index]->identifier;
						for (std::vector<AGMModelEdge>::iterator it=newSearchNode.result->edges.begin(); it!=newSearchNode.result->edges.end();)
						{
							if (it->linking == agm->rules[ruleNumber].remLinksLabel[i] and it->symbolPair.first == aWID and it->symbolPair.second == bWID)
							{
								it = newSearchNode.result->edges.erase(it);
							}
							else
							{
								++it;
							}
						}
					}

					/// 7 Create a new path by appending the new rule triggering to the current path
					AGMRuleExecution exec;
					newSearchNode.path.push_back(exec);

					/// 8 Append the created path to the list ***IF ITS NOT IN THE MEMORY OF WATCHED NODES***
					if ( /**                                **/ true )
					{
						printf("Returning:\n");
						AGMModelPrinter::printWorld(newSearchNode.result);
						ret.push_back(newSearchNode);
					}

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
	else
	{
		printf("Nothing to expand");
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
// 					printf("No link:   %d---[%s]--->%d\n", id1G, goal->edges[l1].linking.c_str(), id2G);
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
















