#pragma once

#include <agm_model.h>
#include <agm_modelEdge.h>
#include <agm_modelSymbols.h>

class AGMModelConverter
{
public:
	static void fromInternalToIce(const AGMModel::SPtr &world, RoboCompWorldModel::GualzruWorld &dst);
	static void fromIceToInternal(const RoboCompWorldModel::GualzruWorld &world, AGMModel::SPtr &dst);
	static void fromInternalToIce(const AGMModelSymbol::SPtr &node, RoboCompWorldModel::GualzruWorldNode &dst);
	static void fromIceToInternal(const RoboCompWorldModel::GualzruWorldNode &node, AGMModelSymbol::SPtr &dst);

	static bool includeIceModificationInInternalModel(const RoboCompWorldModel::GualzruWorldNode &node, AGMModel::SPtr &world);
};


