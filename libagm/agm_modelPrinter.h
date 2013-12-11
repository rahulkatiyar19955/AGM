#ifndef WORLDMODELPRINTER_H
#define WORLDMODELPRINTER_H

#include <stdio.h>

#include <agm_config.h>
#include "agm_model.h"
#include "agm_modelEdge.h"
#include "agm_modelSymbols.h"

/*!
 * @brief Utility class to print AGMModel graphs
 *
 * 
 * 
 */
class AGMModelPrinter
{
public:
	static void printWorld(const AGMModel::SPtr &w);
	static void printWorld(const AGMModel *w);
#ifdef ROBOCOMP_SUPPORT
	static void printWorld(const RoboCompAGMWorldModel::World &w);
	static void printWorld(FILE *fd, const RoboCompAGMWorldModel::World &w);
#endif
};


#endif

