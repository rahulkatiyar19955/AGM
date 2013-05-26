#ifndef WORLDMODELPRINTER_H
#define WORLDMODELPRINTER_H

#include <stdio.h>

#include "agm_model.h"
#include "agm_modelEdge.h"
#include "agm_modelSymbols.h"

class AGMModelPrinter
{
public:
	static void printAGM(const AGMModel::SPtr &w);
	static void printAGM(const AGMModel *w);
};


#endif

