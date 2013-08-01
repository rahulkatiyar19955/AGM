#include "agm_behavior.h"

/*
 * 
 *   A G M S t a t e
 * 
 */

AGMAgent::AGMAgent(std::string n)
{
	name = n;
}

bool AGMAgent::addState(std::string n)
{
	if (std::find(states.begin(), states.end(), n) != states.end())
	{
		return false;
	}
	else
	{
		states.push_back(n);
		return true;
	}
}

bool AGMAgent::operator==(const AGMAgent &other) const
{
	return name == other.getName();
}

std::string AGMAgent::getName() const
{
	return name;
}

AGMStatesVector AGMAgent::getStates() const
{
	return states;
}

/*
 * 
 *   A G M B e h a v i o r D e s c r i p t i o n
 * 
 */

AGMBehaviorDescription::AGMBehaviorDescription()
{
}

bool AGMBehaviorDescription::addAgent(std::string agentName)
{
	AGMAgentVector::iterator it = std::find(agents.begin(), agents.end(), agentName);

	if (it != agents.end())
	{
		return false;
	}
	else
	{
		agents.push_back(AGMAgent(agentName));
		return true;
	}
}

bool AGMBehaviorDescription::addAgentState(std::string agentName, std::string agentState)
{
	AGMAgentVector::iterator it = std::find(agents.begin(), agents.end(), agentName);

	if (it != agents.end())
	{
		return it->addState(agentState);
	}
	else
	{
		return false;
	}
}

bool AGMBehaviorDescription::addConfiguration(std::string config)
{
	if (std::find(configurations.begin(), configurations.end(), config) != configurations.end())
	{
		return false;
	}
	else
	{
		configurations.push_back(config);
		return true;
	}
}

bool AGMBehaviorDescription::tableIsValid()
{
	return true;
}

AGMState AGMBehaviorDescription::getConfigForAgent(const AGMAgentName &agent, const AGMConfig &config) const
{
	const AGMAgentConigNamePair par(agent, config);
	const AGMConfigTable::const_iterator it = table.find(par);
	if (it == table.end())
	{
		throw 0;
	}
	return it->second;
}


bool AGMBehaviorDescription::setConfigForAgent(const AGMAgentName &agent, const AGMConfig &config, const AGMState &state)
{
	const AGMAgentConigNamePair par(agent, config);
	if (validStateForAgent(agent, state))
	{
		table[par] = state;
		return true;
	}
	else
		return false;
}

bool AGMBehaviorDescription::validStateForAgent(const AGMAgentName &agent, const AGMState &state) const
{
	AGMAgentVector::const_iterator it;
	for (it = agents.begin(); it != agents.end(); it++)
	{
		if (it->getName() == agent)
			break;
	}
	if (it != agents.end())
	{
// 		AGMStatesVector states = it->getStates();
// 		AGMStatesVector::iterator it2 = std::find(states.begin(), states.end(), state);
// 		if (it2 != states.end())
			return true;
// 		printf("NO SUCH STATE %s?\n", agent.c_str());
// 		return false;
	}
	else
	{
		printf("NO SUCH AGENT %s?\n", agent.c_str());
		return false;
	}
}

void AGMBehaviorDescription::print()
{
	printf("AGENTS:\n");
	for (AGMAgentVector::iterator it=agents.begin(); it!=agents.end(); it++)
	{
		printf("Agent: %s\n", it->getName().c_str());
		AGMStatesVector v = it->getStates();
		for (AGMStatesVector::iterator itS=v.begin(); itS!=v.end(); itS++)
		{
			printf("  ->  %s\n", itS->c_str());
		}
	}
	printf("\n");

	printf("CONFIGURATIONS:\n");
	for (AGMConfigsVector::iterator it=configurations.begin(); it!=configurations.end(); it++)
	{
		printf("  ->  %s\n", it->c_str());
	}
	
	
	printf("TABLE:\n");
	for (AGMAgentVector::iterator itA=agents.begin(); itA!=agents.end(); itA++)
	{
		for (AGMConfigsVector::iterator itC=configurations.begin(); itC!=configurations.end(); itC++)
		{
			AGMState s;
			try
			{
				s  = getConfigForAgent(itA->getName().c_str(), itC->c_str());
			}
			catch (...)
			{
				s = "---";
			}
			printf(" %s ", s.c_str());
		}
		printf("\n");
	}
}

