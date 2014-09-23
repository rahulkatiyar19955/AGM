#include <agm_misc_functions.h>
#include <agm_modelConverter.h>
#include <agm_modelPrinter.h>

#include <algorithm>

float str2float(const std::string &s)
{
	if (s.size()<=0)
	{
		AGMMODELEXCEPTION("libagm: Error parsing float <empty>\n");
	}

	float ret;
	std::string str = s;
	replace(str.begin(), str.end(), ',', '.');
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
void AGMMisc::publishModification(AGMModel::SPtr &newModel, AGMAgentTopicPrx &agmagenttopic, AGMModel::SPtr &oldModel, std::string sender)
{
	RoboCompAGMWorldModel::Event e;
	e.sender = sender;
	e.why = RoboCompAGMWorldModel::BehaviorBasedModification;
	oldModel->removeDanglingEdges();
	AGMModelConverter::fromInternalToIce(oldModel, e.backModel);
	newModel->removeDanglingEdges();
	AGMModelConverter::fromInternalToIce(newModel, e.newModel);
	//printf("<<%d\n", newModel->numberOfSymbols());
	//AGMModelPrinter::printWorld(newModel);
	agmagenttopic->modificationProposal(e);
	//printf(">>\n");
}

void AGMMisc::publishNodeUpdate(AGMModelSymbol::SPtr &symbol, AGMAgentTopicPrx &agmagenttopic)
{
	RoboCompAGMWorldModel::Node iceSymbol;
	AGMModelConverter::fromInternalToIce(symbol, iceSymbol);
	agmagenttopic->update(iceSymbol);
}



#endif


float AGMMisc::str2float(const std::string &s)
{
	return ::str2float(s);
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










