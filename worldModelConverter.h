#ifndef WORLDMODELCONVERTER_H
#define WORLDMODELCONVERTER_H

#include "worldModel.h"
#include "worldModelEdge.h"
#include "worldModelSymbols.h"

class WorldModelConverter
{
public:
	static void fromInternalToIce(const WorldModel::SPtr &world, RoboCompWorldModel::GualzruWorld &dst);
	static void fromIceToInternal(const RoboCompWorldModel::GualzruWorld &world, WorldModel::SPtr &dst);
	static void fromInternalToIce(const WorldModelSymbol::SPtr &node, RoboCompWorldModel::GualzruWorldNode &dst);
	static void fromIceToInternal(const RoboCompWorldModel::GualzruWorldNode &node, WorldModelSymbol::SPtr &dst);

	static bool includeIceModificationInInternalModel(const RoboCompWorldModel::GualzruWorldNode &node, WorldModel::SPtr &world);
};


#endif

