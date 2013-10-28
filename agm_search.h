#pragma once

#include <stdio.h>

#include "agm_model.h"
#include "agm_modelEdge.h"
#include "agm_modelSymbols.h"


class AGM;

// Structure AGMRuleExecution
struct AGMRuleExecution
{
	std::string ruleName;
	std::map< std::string, int32_t> symbolMapping;
};


// Structure used to store the result of the search process
struct AGMSearchPath
{
public:
	AGMSearchPath()
	{
		result = AGMModel::SPtr(new AGMModel());
	}
	AGMSearchPath(const AGMModel::SPtr &init)
	{
		result = AGMModel::SPtr(new AGMModel(init));
	}
	void includeExecution(const AGMRuleExecution &exec)
	{
		path.push_back(exec);
	}
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
	AGMSearch(const AGMModel::SPtr &current_, const AGMModel::SPtr &goal_, const boost::shared_ptr<AGM> &agm_);

private:
 	AGMSearchPathList expandBestNode();
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






