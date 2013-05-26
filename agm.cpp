#include "agm.h"

#include <iostream>
#include <fstream>
#include <sstream>

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
		AGMStatesVector states = it->getStates();
		AGMStatesVector::iterator it2 = std::find(states.begin(), states.end(), state);
		if (it2 != states.end())
			return true;
		return false;
	}
	return false;	
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



/*
 * 
 *   A G M
 * 
 */

AGM::AGM(std::string pddlFile, std::string agmbdFile)
{
	loadFromFile(pddlFile, agmbdFile);
}

void AGM::loadFromFile(std::string pddlFile, std::string agmbdFile)
{
	bool r;
	std::string line;
	std::ifstream ifile(agmbdFile.c_str());
	if (ifile.is_open())
	{
		while (ifile.good())
		{
			getline(ifile, line);
			if (line.size()>0)
			{
				std::string word;
				std::istringstream iss(line);
				std::vector<std::string> words;
				while(iss >> word) words.push_back(word);
				switch(line[0])
				{
					case 'A':
						for (int v=1; v<words.size(); v++)
						{
							if (v==1)
							{
								r = table.addAgent(words[1]);
							}
							else
							{
								r = table.addAgentState(words[1], words[v]);
							}
							if (r==false)
							{
								std::cout << "Error in the input agmbd file" << std::endl;
								std::cout << line << std::endl;
								exit(-1);
							}
						}
						break;
					case 'C':
						for (int v=1; v<words.size(); v++)
						{
							r = table.addConfiguration(words[v]);
							if (r==false)
							{
								std::cout << "Error in the input agmbd file" << std::endl;
								std::cout << line << std::endl;
								exit(-1);
							}
						}
						break;
					case 'S':
						r = table.setConfigForAgent(words[1], words[2], words[3]);
						if (r==false)
						{
							std::cout << "Error in the input agmbd file" << std::endl;
							std::cout << line << std::endl;
							exit(-1);
						}
						break;
					case '#':
						break;
					default:
						std::cout << "Error in the input agmbd file" << std::endl;
						std::cout << line << std::endl;
						exit(-1);
				}
			}
		}
		ifile.close();
	}
	else
	{
		std::cout << "Unable to open file" << std::cout;
	}

// 	return 0;
/*
	bool r;
	r = table.addAgent("agent1");
	r = table.addAgentState("agent1", "a1a");
	r = table.addAgentState("agent1", "a1c");
	r = table.addAgentState("agent1", "a1b");
	r = table.addAgent("agent3");
	r = table.addAgentState("agent3", "a3a");
	r = table.addAgentState("agent3", "a3b");
	r = table.addAgent("agent2");
	r = table.addAgentState("agent2", "a2a");
	r = table.addAgentState("agent2", "a2d");
	r = table.addAgentState("agent2", "a2b");
	r = table.addAgentState("agent2", "a2c");
	
	r = table.addConfiguration("do1");
	r = table.addConfiguration("do3");
	r = table.addConfiguration("do2");


	r = table.setConfigForAgent("agent1", "do1", "a1a");
	r = table.setConfigForAgent("agent1", "do2", "a1b");
	r = table.setConfigForAgent("agent1", "do3", "a1c");
	r = table.setConfigForAgent("agent2", "do1", "a2a");
	r = table.setConfigForAgent("agent2", "do2", "a2b");
	r = table.setConfigForAgent("agent2", "do3", "a2c");
	r = table.setConfigForAgent("agent3", "do1", "a3a");
	r = table.setConfigForAgent("agent3", "do2", "a3b");
	r = table.setConfigForAgent("agent3", "do3", "a3a");
*/

	print();

}

void AGM::print()
{
	table.print();
}



