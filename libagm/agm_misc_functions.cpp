#include <agm_misc_functions.h>
#include <agm_modelConverter.h>

#include <algorithm>

float str2float(const std::string &s)
{
	if (s.size()<=0)
	{
		printf("libagm: Error parsing float <empty>\n");
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
		printf("libagm: Error parsing int <empty>\n");
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
void AGMMisc::publishModification(AGMModel::SPtr &newModel, AGMAgentTopicPrx &agmagenttopic, AGMModel::SPtr &oldModel)
{
	RoboCompAGMWorldModel::Event e;
	AGMModelConverter::fromInternalToIce(oldModel, e.backModel);
	AGMModelConverter::fromInternalToIce(newModel, e.newModel);
	printf("<<\n");
	agmagenttopic->modificationProposal(e);
	printf(">>\n");
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


std::string AGMMisc::str2float(const float &f)
{
	return ::float2str(f);
}


std::string AGMMisc::str2int(const int32_t &i)
{
	return ::int2str(i);
}










