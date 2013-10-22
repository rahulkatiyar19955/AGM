#include <iostream>
#include <fstream>
#include <sstream>

#include <agm.h>


/*
 * 
 *   A G M
 * 
 */
void AGM_toupper(std::string &action)
{
	std::transform(action.begin(), action.end(), action.begin(), ::toupper);
}
void AGM_tolower(std::string &action)
{
	std::transform(action.begin(), action.end(), action.begin(), ::tolower);
}

AGM::AGM(std::string pddlFileFull_, std::string pddlFilePartial_)
{
	pddlFileFull = pddlFileFull_;
	pddlFilePartial = pddlFilePartial_;

	loadFromFile(pddlFileFull, pddlFilePartial);
}


void AGM::loadFromFile(std::string pddlFileFull, std::string pddlFilePartial)
{
	readFileToString(pddlFileFull,    fullPDDLContent);
	readFileToString(pddlFilePartial, partialPDDLContent);
}

void AGM::readFileToString(std::string &file, std::string &content)
{
	std::string line;
	std::ifstream ifile(file.c_str());
	if (ifile.is_open())
	{
		while (ifile.good())
		{
			getline(ifile, line);
			content += line;
			content += "\n";
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





