#ifndef WORLDMODELPRINTER_H
#define WORLDMODELPRINTER_H

#include <stdio.h>

#include "agm_model.h"
#include "agm_modelEdge.h"
#include "agm_modelSymbols.h"

class AGMModelPrinter
{
public:
	static void printWorld(const AGMModel::SPtr &w);
	static void printWorld(const AGMModel *w);
	static void printWorld(const RoboCompWorldModel::GualzruWorld &w);
	static void printWorld(FILE *fd, const RoboCompWorldModel::GualzruWorld &w);
};


#endif

