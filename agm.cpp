#include <iostream>
#include <fstream>
#include <sstream>

#include "agm.h"




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



