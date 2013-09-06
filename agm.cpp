#include <iostream>
#include <fstream>
#include <sstream>

#include <agm.h>


/*
 * 
 *   A G M
 * 
 */

AGM::AGM(std::string pddlFile_, std::string agmbdFile_)
{
	pddlFile = pddlFile_;
	loadFromFile(pddlFile_, agmbdFile_);
}

void AGM::loadFromFile(std::string pddlFile, std::string agmbdFile)
{
	bool r;
	std::string line;
	std::ifstream ifile(agmbdFile.c_str());
	if (ifile.is_open())
	{
		std::cout << "File " << agmbdFile << " opened correclty.\n";
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
						for (uint32_t v=1; v<words.size(); v++)
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
								std::cout << "AGM::loadFromFile(): Error in the input agmbd file (1)" << std::endl;
								std::cout << line << std::endl;
								exit(-1);
							}
						}
						break;
					case 'C':
						for (uint32_t v=1; v<words.size(); v++)
						{
							r = table.addConfiguration(words[v]);
							if (r==false)
							{
								std::cout << "AGM::loadFromFile(): Error in the input agmbd file (2)" << std::endl;
								std::cout << line << std::endl;
								exit(-1);
							}
						}
						break;
					case 'R':
						if (words.size() != 3)
						{
							std::cout << "AGM::loadFromFile(): Error in the input agmbd file (5)" << std::endl;
							std::cout << line << std::endl;
							exit(-1);
						}
						action2behavior[words[1]] = words[2];
						break;
					case 'S':
						r = table.setConfigForAgent(words[1], words[2], words[3]);
						if (r==false)
						{
							std::cout << "AGM::loadFromFile(): Error in the input agmbd file (3)" << std::endl;
							std::cout << line << std::endl;
							exit(-1);
						}
						break;
					case '#':
						break;
					default:
						bool blank = true;
						for (int strIdx = 0; strIdx<line.size(); strIdx++)
						{
							if (line[strIdx] != ' ' and line[strIdx] != '\t' and line[strIdx] != '\n' and line[strIdx] != '\v' and line[strIdx] != '\f' and line[strIdx] != '\r')
							{
								blank = false;
								break;
							}
						}
						if (not blank)
						{
							std::cout << "AGM::loadFromFile(): Error in the input agmbd file (4)" << std::endl;
							std::cout << line << std::endl;
							exit(-1);
						}
				}
			}
		}
		ifile.close();
	}
	else
	{
		std::cout << "Unable to open file" << std::cout;
		exit(1);
	}

}

void AGM::print()
{
	table.print();
}


std::string AGM::pddlProblemForTarget(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName)
{
	return currentModel.generatePDDLProblem(target, unknowns, domainName, problemName);
}


bool AGM::checkModel(AGMModel::SPtr model)
{
	return false;
}


bool AGM::proposeModel(AGMModel::SPtr model)
{
	return true;
}


bool AGM::updateModel(AGMModelSymbol)
{
	return true;
}





