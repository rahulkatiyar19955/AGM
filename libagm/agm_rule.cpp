#include "agm_rule.h"

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void AGGLRule::print()
{
	printf(" Name: %s (%s)\n", name.c_str(), active?"active":"passive");
	if (symbolsToCreateName.size()>0) printf("   Create symbols:\n");
	for (uint32_t i=0; i<symbolsToCreateName.size(); ++i)
	{
		printf("      %s (%s)\n", symbolsToCreateName[i].c_str(), symbolsToCreateType[i].c_str());
	}
	if (symbolsToRemove.size()>0) printf("   Remove symbols:\n");
	for (uint32_t i=0; i<symbolsToRemove.size(); ++i)
	{
		printf("      %s\n", symbolsToRemove[i].c_str());
	}
	if (symbolsToRetypeName.size()>0) printf("   Retype symbols:\n");
	for (uint32_t i=0; i<symbolsToRetypeName.size(); ++i)
	{
		printf("      %s (%s)\n", symbolsToRetypeName[i].c_str(), symbolsToRetypeType[i].c_str());
	}
	if (addLinksA.size()>0) printf("   Create links:\n");
	for (uint32_t i=0; i<addLinksA.size(); ++i)
	{
		printf("      %s---[%s]--->%s\n", addLinksA[i].c_str(), addLinksLabel[i].c_str(), addLinksB[i].c_str());
	}
	if (remLinksA.size()>0) printf("   Remove links:\n");
	for (uint32_t i=0; i<remLinksA.size(); ++i)
	{
		printf("      %s---[%s]--->%s\n", remLinksA[i].c_str(), remLinksLabel[i].c_str(), remLinksB[i].c_str());
	}
}

void AGGLRule::setCost(int32_t c)
{
	cost = c;
}

void AGGLRule::setName(const char *nam)
{
	name = std::string(nam);
}

void AGGLRule::setActive(const char *act)
{
	std::string acti(act);
	if (acti == "active")
		active = true;
	else if (acti == "passive")
		active = false;
	else
	{
		printf("Wrong active/passive\n");
		exit(-1);
	}
}
void AGGLRule::addSymbol(bool left, std::string name, std::string type)
{
	if (left)
	{
		lhsSymbolsNames.push_back(name);
		lhsSymbolsTypes.push_back(type);
	}
	else
	{
		rhsSymbolsNames.push_back(name);
		rhsSymbolsTypes.push_back(type);
	}
}
void AGGLRule::addLink(bool left, std::string a, std::string b, std::string label, int negated)
{
	if (left)
	{
		lhsLinksA.push_back(a);
		lhsLinksB.push_back(b);
		lhsLinksLabel.push_back(label);
	}
	else
	{
		rhsLinksAID.push_back(rhsLinksA.size());
		rhsLinksBID.push_back(rhsLinksB.size());
		rhsLinksA.push_back(a);
		rhsLinksB.push_back(b);
		rhsLinksLabel.push_back(label);
	}
}

void printV(std::string name, strVector v)
{
	printf("%s: ", name.c_str());
	for (uint32_t s=0; s<v.size(); s++)
	{
		printf("%s ", v[s].c_str());
	}
	printf("\n");
}

void AGGLRule::computeEffects()
{
// 	printf("symbol creation\n");
	/// Symbol deletion
	for (uint32_t i=0; i<rhsSymbolsNames.size(); i++)
	{
		//printf("%s\n", rhsSymbolsNames[i].c_str());
		bool found = false;
		for (uint32_t j=0; j<lhsSymbolsNames.size() and not found; j++)
		{
			if (rhsSymbolsNames[i] == lhsSymbolsNames[j])
				found = true;
		}
		if (not found)
		{
			//printf("not found (append)\n");
			symbolsToCreateName.push_back(rhsSymbolsNames[i]);
			symbolsToCreateType.push_back(rhsSymbolsTypes[i]);
		}
		else
		{
			//printf("found\n");
		}
	}
	//printf("symbol deletion\n");
	//printV("lhs", lhsSymbolsNames);
	//printV("rhs", rhsSymbolsNames);
	/// Symbol deletion
	for (uint32_t i=0; i<lhsSymbolsNames.size(); i++)
	{
		bool found = false;
		uint32_t j;
		for (j=0; j<rhsSymbolsNames.size() and not found; j++)
		{
			if (lhsSymbolsNames[i] == rhsSymbolsNames[j])
			{
				found = true;
				break;
			}
		}
		if (not found)
		{
			symbolsToRemove.push_back(lhsSymbolsNames[i]);
			symbolsToRemoveID.push_back(i);
		}
	}
	//printf("typing\n");
	/// Type changes
	for (uint32_t i=0; i<lhsSymbolsNames.size(); i++)
	{
		bool found = false;
		for (uint32_t j=0; j<symbolsToCreateName.size() and not found; j++)
		{
			if (lhsSymbolsNames[i] == symbolsToCreateName[j]) found = true;
		}
		for (uint32_t j=0; j<symbolsToRemove.size() and not found; j++)
		{
			if (lhsSymbolsNames[i] == symbolsToRemove[j]) found = true;
		}
		// If they remain
		if (not found)
		{
			for (uint32_t k=0; k<rhsSymbolsNames.size(); k++)
			{
				if (lhsSymbolsNames[i] == rhsSymbolsNames[k])
				{
					if (lhsSymbolsTypes[i] != rhsSymbolsTypes[k])
					{
						symbolsToRetypeName.push_back(lhsSymbolsNames[i]);
						symbolsToRetypeID.push_back(i);
						symbolsToRetypeType.push_back(rhsSymbolsTypes[k]);
					}
				}
			}
		}
	}
	//printf("link creation\n");
	/// Link creation
	for (uint32_t j=0; j<rhsLinksLabel.size(); j++)
	{
		bool found = false;
		for (uint32_t i=0; i<lhsLinksLabel.size() and not found; i++)
		{
			if (lhsLinksA[i] == rhsLinksA[j])
			{
				if (lhsLinksLabel[i] == rhsLinksLabel[j])
				{
					if (lhsLinksB[i] == rhsLinksB[j])
					{
						found = true;
					}
				}
			}
		}
		if (not found)
		{
			addLinksA.push_back(rhsLinksA[j]);
			addLinksB.push_back(rhsLinksB[j]);
			addLinksAID.push_back(rhsLinksAID[j]);
			addLinksBID.push_back(rhsLinksBID[j]);
			addLinksLabel.push_back(rhsLinksLabel[j]);
		}
	}
	//printf("link deletion\n");
	/// Link deletion
	for (uint32_t i=0; i<lhsLinksLabel.size(); i++)
	{
		bool found = false;
		for (uint32_t j=0; j<rhsLinksLabel.size() and not found; j++)
		{
			if (lhsLinksA[i] == rhsLinksA[j])
			{
				if (lhsLinksLabel[i] == rhsLinksLabel[j])
				{
					if (lhsLinksB[i] == rhsLinksB[j])
					{
						found = true;
					}
				}
			}
		}
		if (not found)
		{
			remLinksAID.push_back(remLinksA.size());
			remLinksBID.push_back(remLinksB.size());
			remLinksA.push_back(lhsLinksA[i]);
			remLinksB.push_back(lhsLinksB[i]);
			remLinksLabel.push_back(lhsLinksLabel[i]);
		}
	}
//printf("gocha!\n");
}

void AGGLRule::clear() 
{
	name = "";
	active = true;
	lhsSymbolsNames.clear();
	lhsSymbolsTypes.clear();
	lhsLinksA.clear();
	lhsLinksB.clear();
	lhsLinksLabel.clear();

	rhsSymbolsNames.clear();
	rhsSymbolsTypes.clear();
	rhsLinksA.clear();
	rhsLinksB.clear();
	rhsLinksAID.clear();
	rhsLinksBID.clear();
	rhsLinksLabel.clear();

	symbolsToCreateName.clear();
	symbolsToCreateType.clear();
	symbolsToRemove.clear();
	symbolsToRemoveID.clear();
	addLinksA.clear();
	addLinksB.clear();
	addLinksAID.clear();
	addLinksBID.clear();
	addLinksLabel.clear();
	remLinksA.clear();
	remLinksB.clear();
	remLinksAID.clear();
	remLinksBID.clear();
	remLinksLabel.clear();
	symbolsToRetypeName.clear();
	symbolsToRetypeID.clear();
	symbolsToRetypeType.clear();
}
