#pragma once

#include <stdio.h>

#include "agm_model.h"
#include "agm_modelEdge.h"
#include "agm_modelSymbols.h"


class AGM;

// Structure AGMRuleExecution
class AGMRuleExecution
{
public:
	std::string ruleName;
	std::map< std::string, int32_t> symbolMapping;

	void print()
	{
		printf("[%s ]\n", ruleName.c_str());
	}
};


// Structure used to store the result of the search process
struct AGMSearchPath
{
friend class AGMSearch;
public:
	AGMSearchPath();
	AGMSearchPath(const AGMModel::SPtr &init);
	void includeExecution(const AGMRuleExecution &exec);
	void print();
	bool goalIsMet(const AGMModel::SPtr &goal);
	void clear();
private:
	std::list< AGMRuleExecution > path;
	AGMModel::SPtr result;
};
typedef	std::list<AGMSearchPath> AGMSearchPathList;



class AGMSearch
{
/*** 
   * Data types
	*/
public:
	// Model list
	typedef std::list<AGMSearchPath> AGMSearchPathList;
	// Mapping "integer ==> pathList" (used for storing the explored nodes)
	typedef std::map<int, AGMSearchPathList> AGMMapIntegerSearchPath;
	// Mapping "integer ==> integer2modelMap" (used for storing the explored nodes)
	typedef std::map<int, AGMMapIntegerSearchPath> AGMModelExploredMemory;



public:
	AGMSearch(const boost::shared_ptr<AGM> &agm_);
	bool go(const AGMModel::SPtr &current_, const AGMModel::SPtr &goal_, AGMSearchPath &result);

private:
 	AGMSearchPathList expandBestNodeAndRemoveItFromTheNodesToExplore();
private:
	boost::shared_ptr<AGM> agm;
	AGMModel::SPtr current, goal;
	
	AGMSearchPathList nodesToExplore;
	AGMModelExploredMemory exploredNodes;
	AGMSearchPath result;

/// STATIC METHODS
public:
	static bool goalIsMet(const AGMModel::SPtr &world, const AGMModel::SPtr &goal);
	static bool canBeEqual(const AGMModel::SPtr &goal, int32_t a, int32_t b) { return 0; }

};






