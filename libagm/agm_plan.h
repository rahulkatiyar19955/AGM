#ifndef AGMPLAN_H
#define AGMPLAN_H


#include <boost/algorithm/string.hpp>



typedef std::pair<std::string, std::string> AGMParameter;
typedef std::vector< AGMParameter > AGMParameters;

struct AGMAction
{
public:
	std::string name:
	AGMParameters parameters;

private:
	static AGMAction fromString(std::string actionStr)
	{
		AGMAction action;

		std::vector<std::string> actionStrs;
		boost::split(actionStrs, actionStr, boost::is_any_of("\n@,{}"), boost::token_compress_on);
		for (auto part: actionStrs)
		{
			printf("%s\n", part.c_str());
		}
		printf("--------\n");
	}
};


struct AGMPlan
{
public:
	std::vector<AGMAction> actions;

private:

	static AGMPlan fromString(std::string plan)
	{
		AGMPlan plan;

		std::vector<std::string> actionStrs;
		boost::split(actionStrs, params["plan"].value, boost::is_any_of("\n"));

		for (auto actionStr : actionStrs)
		{
			plan.append(AGMAction::fromString(actionStr))
		}
		
		return plan;
	}

	void append(AGMAction action)
	{
		actions.push_back(action);
	}

};

#endif