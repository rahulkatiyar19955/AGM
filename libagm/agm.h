#pragma once

#include <agm_misc_functions.h>
#include <agm_model.h>
#include <agm_modelSymbols.h>
#include <agm_modelPrinter.h>
#include <agm_modelEdge.h>
#include <agm_modelConverter.h>

/** @defgroup CPPAPI AGM's C++ API

\warning This information is outdated, the API has been improved since this text was written.

\section creating Creating a modeling
doc doc doc

\section modifying Making a structural modification to a model
Este código borra el símbolo de identificador cero e introduce dos símbolos en su lugar. Es pues un cambio estructural:


\code{.cpp}
// Create a new copy of the model
AGMModel::SPtr newModel(new AGMModel(worldModel));
// Create two symbols
AGMModelSymbol::SPtr robot  = newModel->newSymbol("robot");
AGMModelSymbol::SPtr status = newModel->newSymbol("status");
// Create a link
AGMModelEdge edge(robot->identifier, status->identifier, "bored");
newModel->edges.push_back(edge);
// Remove symbol
newModel->removeSymbol(0);
// Create a modification event with the previous and proposed model
RoboCompAGMWorldModel::Event e;
e.sender = "balltracker";
e.why = RoboCompAGMWorldModel::BehaviorBasedModification;
AGMModelConverter::fromInternalToIce(worldModel, e.backModel);
AGMModelConverter::fromInternalToIce(newModel, e.newModel);
try { agmagenttopic->modificationProposal(e);}
catch(const Ice::Exception &e) { std::cout << e << std::endl;};
\endcode

Como resultado, este código publica una propuesta de modificación que capturará el ejecutivo. Si se desarrolla un componente que haga muchos cambios es posible que sea conveniente meter las últimas siete líneas dentro de una función.


\section update Updating a symbol
Las actualización de un nodo es más sencilla:

\code{.cpp}
// Modify the attributes in the current model
worldModel->symbols[ballIndex]->attributes["x"] = xPos;
worldModel->symbols[ballIndex]->attributes["y"] = yPos;
worldModel->symbols[ballIndex]->attributes["z"] = zPos;
// Fill a RoboCompAGMWorldModel::Node structure with
// the new data.
RoboCompAGMWorldModel::Node node;
AGMModelConverter::fromInternalToIce(worldModel->symbols[ballIndex], node);
// Publish the proposal
try { agmagenttopic->update(node); }
catch(const Ice::Exception &e) { cout << e << endl; }
\endcode


\section print Printing a model
Regardless of whether we have a AGMModel::SPtr or it RoboComp Ice version we will use the same function:

\code{.cpp}
AGMModelPrinter::printWorld(model);
\endcode

**/



