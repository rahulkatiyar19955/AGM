#pragma once

#include <agm_misc_functions.h>
#include <agm_model.h>
#include <agm_modelSymbols.h>
#include <agm_modelPrinter.h>
#include <agm_modelEdge.h>
#include <agm_modelConverter.h>
#include <agm_search.h>
#include <agm_rule.h>

/** @defgroup CPPAPI AGM's C++ API

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
Da igual que sea un AGMModel::Sptr o la versión Ice del tipo de datos, usaremos la misma función:

\code{.cpp}
AGMModelPrinter::printWorld(model);
\endcode

**/


/**
\page tutorials Turorials
\tableofcontents

\section installation Installing AGM
doc doc doc

\section modifying Making a structural modification to a model
Este código borra el símbolo de identificador cero e introduce dos símbolos en su lugar. Es pues un cambio estructural:


 */


