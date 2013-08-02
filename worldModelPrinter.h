#ifndef WORLDMODELPRINTER_H
#define WORLDMODELPRINTER_H

#include <stdio.h>

#include "worldModel.h"
#include "worldModelEdge.h"
#include "worldModelSymbols.h"

class WorldModelPrinter
{
public:
	static void printWorld(const WorldModel::SPtr &w);
	static void printWorld(const WorldModel *w);
	static void printWorld(const RoboCompWorldModel::GualzruWorld &w);
	static void printWorld(FILE *fd, const RoboCompWorldModel::GualzruWorld &w);
};


#endif

