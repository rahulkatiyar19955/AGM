#include <agm_misc_functions.h>
#include <agm_modelConverter.h>
#include <agm_modelPrinter.h>

#include <algorithm>

float str2float(const std::string &s, bool debug)
{
	if (s.size()<=0)
	{
		AGMMODELEXCEPTION("libagm: Error parsing float <empty>\n");
	}

	if (debug) printf("s1 %s\n", s.c_str());
	float ret;
	std::string str = s;
	replace(str.begin(), str.end(), ',', '.');
	if (debug) printf("s2 %s\n", str.c_str());
	std::istringstream istr(str);
	istr.imbue(std::locale("C"));
	istr >> ret;
	return ret;
}

int32_t str2int(const std::string &s)
{
	if (s.size()<=0)
	{
		AGMMODELEXCEPTION("libagm: Error parsing int <empty>\n");
	}

	int32_t ret;
	std::string str = s;
	replace(str.begin(), str.end(), ',', '.');
	std::istringstream istr(str);
	istr.imbue(std::locale("C"));
	istr >> ret;
	return ret;
}


std::string float2str(const float &f)
{
	std::ostringstream ostr;
	ostr.imbue(std::locale("C"));
	ostr << f;
	return ostr.str();
}

std::string int2str(const int32_t &i)
{
	std::ostringstream ostr;
	ostr.imbue(std::locale("C"));
	ostr << i;
	return ostr.str();
}


#if ROBOCOMP_SUPPORT == 1

void AGMMisc::publishModification(AGMModel::SPtr &newModel, AGMExecutivePrx &agmexecutive, std::string sender)
{
	newModel->removeDanglingEdges();
	RoboCompAGMWorldModel::World newModelICE;
	AGMModelConverter::fromInternalToIce(newModel, newModelICE);
	return agmexecutive->structuralChangeProposal(newModelICE, sender, "");
}

void AGMMisc::publishNodeUpdate(AGMModelSymbol::SPtr &symbol, AGMExecutivePrx &agmexecutive)
{
	RoboCompAGMWorldModel::Node iceSymbol;
	AGMModelConverter::fromInternalToIce(symbol, iceSymbol);
	agmexecutive->symbolUpdate(iceSymbol);
}

void AGMMisc::publishEdgeUpdate(AGMModelEdge &edge, AGMExecutivePrx &agmexecutive)
{
	RoboCompAGMWorldModel::Edge iceEdge;
	AGMModelConverter::fromInternalToIce(&edge, iceEdge);
	agmexecutive->edgeUpdate(iceEdge);
}

#endif


float AGMMisc::str2float(const std::string &s, bool debug)
{
	const std::string st = s;
	if (debug) printf("s %s\n", st.c_str());
	const float f = ::str2float(s, debug);
	if (debug) printf("f %f\n", f);
	return f;
}


int32_t AGMMisc::str2int(const std::string &s)
{
	return ::str2int(s);
}


std::string AGMMisc::float2str(const float &f)
{
	return ::float2str(f);
}


std::string AGMMisc::int2str(const int32_t &i)
{
	return ::int2str(i);
}





