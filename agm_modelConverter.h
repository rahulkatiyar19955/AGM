#pragma once

#include <agm_model.h>
#include <agm_modelEdge.h>
#include <agm_modelSymbols.h>

#include "AGMWorldModel.h"

class AGMModelConverter
{
public:
// #ifdef ROBOCOMP_SUPPORT
	static void fromInternalToIce(const AGMModel::SPtr &world, RoboCompAGMWorldModel::World &dst);
	static void fromIceToInternal(const RoboCompAGMWorldModel::World &world, AGMModel::SPtr &dst);
	static void fromInternalToIce(const AGMModelSymbol::SPtr &node, RoboCompAGMWorldModel::Node &dst);
	static void fromIceToInternal(const RoboCompAGMWorldModel::Node &node, AGMModelSymbol::SPtr &dst);
	static void fromInternalToIce(const AGMModelSymbol *node, RoboCompAGMWorldModel::Node &dst);
	static bool includeIceModificationInInternalModel(const RoboCompAGMWorldModel::Node &node, AGMModel::SPtr &world);
// #endif
	static void fromXMLToInternal(const std::string path, AGMModel::SPtr &dst);


};


