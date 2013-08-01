#pragma once

#include <stdio.h>
#include <string>
#include <vector>
#include <map>
#include <algorithm>


typedef std::string AGMState;
typedef std::vector<AGMState> AGMStatesVector;
typedef std::string AGMAgentName;

class AGMAgent
{
public:
	AGMAgent(std::string n);
	bool operator==(const AGMAgent &other) const;

	bool addState(std::string n);
	std::string getName() const;
	AGMStatesVector getStates() const;
private:
	AGMAgentName name;
	AGMStatesVector states;
};
typedef std::vector<AGMAgent> AGMAgentVector;


typedef std::string AGMConfig;
typedef std::vector<AGMConfig> AGMConfigsVector;

typedef std::pair<AGMAgentName, AGMConfig> AGMAgentConigNamePair;
typedef std::map<AGMAgentConigNamePair, AGMState> AGMConfigTable;


class AGMBehaviorDescription
{
public:
	AGMBehaviorDescription();
	
	bool addAgent(std::string agentName);
	bool addAgentState(std::string agentName, std::string stateName);
	bool addConfiguration(std::string configName);
	AGMState getConfigForAgent(const AGMAgentName &agent, const AGMConfig &config) const;
	bool setConfigForAgent(const AGMAgentName &agent, const AGMConfig &config, AGMState const &state);
	bool validStateForAgent(const AGMAgentName &agent, const AGMState &state) const;
	bool tableIsValid();

	void print();
// private:
	AGMConfigsVector configurations;
	AGMAgentVector   agents;
	AGMConfigTable   table;
};
