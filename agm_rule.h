#pragma once

#include <iostream>
#include <vector>
#include <stdint.h>

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
	std::vector<int32_t> symbolsToRemoveID;
	strVector symbolsToRetypeName;
	strVector symbolsToRetypeType;
	std::vector<int32_t> symbolsToRetypeID;
	// Effect Links
	strVector addLinksA;
	std::vector<int32_t> addLinksAID;
	strVector addLinksB;
	std::vector<int32_t> addLinksBID;
	strVector addLinksLabel;
	strVector remLinksA;
	strVector remLinksB;
	std::vector<int32_t> remLinksAID;
	std::vector<int32_t> remLinksBID;
	strVector remLinksLabel;
	// Unaffected links
	
	
	
	void print();
	void setName(const char *nam);
	void setActive(const char *act);
	void setCost(int c);
	void addSymbol(bool left, std::string name, std::string type);
	void addLink(bool left, std::string a, std::string b, std::string label, int negated);
	void computeEffects();
	void clear();
	
	/// RHS
	strVector rhsSymbolsNames;
	strVector rhsSymbolsTypes;
	strVector rhsLinksA;
	strVector rhsLinksB;
	std::vector<int32_t> rhsLinksAID;
	std::vector<int32_t> rhsLinksBID;
	strVector rhsLinksLabel;

	int cost;
};

