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
namespace AGMMisc
{
	void publishModification(AGMModel::SPtr &newModel, AGMAgentTopicPrx &agmagenttopic, AGMModel::SPtr &oldModel)
	{
		RoboCompAGMWorldModel::Event e;
		AGMModelConverter::fromInternalToIce(oldModel, e.backModel);
		AGMModelConverter::fromInternalToIce(newModel, e.newModel);
		agmagenttopic->modificationProposal(e);

	}
}
#endif