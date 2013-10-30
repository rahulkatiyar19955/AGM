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


AGM::AGM(const AGM::SPtr &src)
{
	pddlFileFull       = src->pddlFileFull;
	pddlFilePartial    = src->pddlFilePartial;
	fullPDDLContent    = src->fullPDDLContent;
	partialPDDLContent = src->partialPDDLContent;
	currentModel = AGMModel::SPtr(new AGMModel(src->currentModel));
}

AGM::AGM(std::string agglfile, std::string pddlFileFull_, std::string pddlFilePartial_)
{
	if (not parseAGGL(agglfile.c_str(), this, &rules))
	{
		throw "Error reading AGGL file";
	}

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
	else if (file != "")
	{
		std::cout << "Unable to open file:" << file << std::cout;
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


AGGLRule &AGM::rule(int r)
{
	return rules[r];
}



void AGM::addAttribute(std::string key, std::string value)
{
	attributes[key] = value;
}

void AGM::addAttribute(const char *key, const char *value)
{
	attributes[std::string(key)] = std::string(value);
}

void AGM::addAttribute(std::string key, int value)
{
	char text[512];
	snprintf(text, 511, "%d", value);
	attributes[key] = std::string(text);
}

void AGM::addAttribute(const char *key, int value)
{
	char text[512];
	snprintf(text, 511, "%d", value);
	attributes[std::string(key)] = std::string(text);
}

	