#pragma once

#include <agm_config.h>
#include <agm_model.h>
#include <agm_modelException.h>

#if ROBOCOMP_SUPPORT == 1
	#include <AGMAgent.h>
	using namespace RoboCompAGMAgent;
#endif

/*! Converts an STD string to float. */
float str2float(const std::string &s, bool debug = false);
/*! Converts an STD string to integer. */
int32_t str2int(const std::string &s);


/*! Converts a float to an STD string. */
std::string float2str(const float &f);
/*! Converts an integer to an STD string. */
std::string int2str(const int32_t &i);




/*!
 * \class AGMMisc
 * @ingroup C++API
 * @brief Class containing several useful functions.
 *
 * Class containing several useful functions.
 * 
 */
class AGMMisc
{
public:
#if ROBOCOMP_SUPPORT == 1
	/*! Publish a new world model (<em>worldModel</em>) using the proxy <em>agmagenttopic</em> using <em>oldModel</em> as the old model. */
	static void publishModification(AGMModel::SPtr &newModel, AGMAgentTopicPrx &agmagenttopic, AGMModel::SPtr &oldModel, std::string sender="unspecified");
	static void publishNodeUpdate(AGMModelSymbol::SPtr &symbol, AGMAgentTopicPrx &agmagenttopic);
#endif
	static inline float str2float(const std::string &s, bool debug = false);
	static inline int32_t str2int(const std::string &s);
	static inline std::string float2str(const float &f);
	static inline std::string int2str(const int32_t &i);
};

