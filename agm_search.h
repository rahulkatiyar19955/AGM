#pragma once

#include <stdio.h>

#include "agm_model.h"
#include "agm_modelEdge.h"
#include "agm_modelSymbols.h"


class AGMSearch
{
/*** 
   * Data types
	*/
public:
	// structure AGMRuleExecution
	struct AGMRuleExecution
	{
		std::string ruleName;
		std::map< std::string, int32_t> symbolMapping;
	};

	// Structure used to store the result of the search process
	struct AGMSearchPath
	{
	public:
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
};


