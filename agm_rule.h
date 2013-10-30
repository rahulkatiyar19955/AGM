#pragma once

#include <iostream>
#include <vector>

typedef std::vector<std::string> strVector;


class AGGLRule
{
public:
	std::string name;
	bool active;
	// LHS
	strVector lhsSymbolsNames;
	strVector lhsSymbolsTypes;
	strVector lhsLinksA;
	strVector lhsLinksB;
	strVector lhsLinksLabel;
	// Effect symbols
	strVector symbolsToCreateName;
	strVector symbolsToCreateType;
	strVector symbolsToRemove;
	strVector symbolsToRetypeName;
	strVector symbolsToRetypeType;
	// Effect Links
	strVector addLinksA;
	strVector addLinksB;
	strVector addLinksLabel;
	strVector remLinksA;
	strVector remLinksB;
	strVector remLinksLabel;
	
	void print();
	void setName(const char *nam);
	void setActive(const char *act);
	void addSymbol(bool left, std::string name, std::string type);
	void addLink(bool left, std::string a, std::string b, std::string label);
	void computeEffects();
	void clear();
	
	/// RHS
	strVector rhsSymbolsNames;
	strVector rhsSymbolsTypes;
	strVector rhsLinksA;
	strVector rhsLinksB;
	strVector rhsLinksLabel;

};

