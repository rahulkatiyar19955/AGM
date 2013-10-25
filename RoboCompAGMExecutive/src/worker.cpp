/*
 *    Copyright (C) 2013 by Luis J. Manso - University of Extremadura
 *
 *    This file is part of AGM (Active Grammar-based Modeling)
 *
 *    RoboComp is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    RoboComp is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "worker.h"
#include <agm_model.h>
#include <agm_modelEdge.h>
#include <agm_modelSymbols.h>
#include <agm_modelConverter.h>
#include <agm_modelPrinter.h>

/**
* \brief Default constructor
*/
Worker::Worker(WorkerParameters &parameters)
{
	std::locale::global(std::locale("C"));
	prms = parameters;
	missionChanged = true;

	mutex = new QMutex();
	processMutex = new QMutex();

	numberOfModificationsProposed = 0;

	fd = fopen("executive_results.txt", "w");
	if (fd==NULL)
	{
		printf("Can't open executive_results.txt for writing\n");
		exit(-1);
	}

	// Initial world
	bool initializeFromXML = false;
	std::string im = parameters.initialModelXML;
	if (im.size() > 0)
	{
		if (im[0]!=' ' and im[0]!='\t' and im!="" and im!="none" and im!="off")
		{
			initializeFromXML = true;
		}
	}
	if (initializeFromXML)
	{
		printf("Initializing from file (\"%s\").\n", parameters.initialModelXML.c_str());
		worldModel = AGMModel::SPtr(new AGMModel());
		AGMModelConverter::fromXMLToInternal(parameters.initialModelXML, worldModel);
	}
	else
	{
		printf("Initializing from empty world (with an start symbol).\n");
		worldModel = AGMModel::SPtr(new AGMModel());
		worldModel->newSymbol("startsymbol");
	}
	printf("--------------\n");
	AGMModelPrinter::printWorld(worldModel);
	printf("--------------\n");
	// Initial target (empty)
	targetModel = AGMModel::SPtr(new AGMModel());


	RoboCompAGMWorldModel::Event e;
	e.why    = RoboCompAGMWorldModel::InitialWorld;
	e.sender = "executive";
	e.backModel.nodes.clear();
	e.backModel.edges.clear();
	AGMModelConverter::fromInternalToIce(worldModel, e.backModel);
	AGMModelConverter::fromInternalToIce(worldModel, e.newModel);
	prms.executiveTopic->modelModified(e);
	AGMModelPrinter::printWorld(worldModel);
}

void AGMAgentTopicI::modificationProposal(const RoboCompAGMWorldModel::Event &result, const Ice::Current&)
{
	qDebug() << "\n\nEvent from: " << result.sender.c_str();
	worker->enqueueEvent(result);
}

void AGMAgentTopicI::update(const RoboCompAGMWorldModel::Node &result, const Ice::Current&)
{
	worker->update(result);
}

void Worker::enqueueEvent(const RoboCompAGMWorldModel::Event &r)
{
// 	std::cout << "New event from " << r.sender << "!\n";
// 	AGMModelPrinter::printWorld(r.newModel);
	mutex->lock();
	eventQueue.enqueue(r);
	processMutex->unlock();
	mutex->unlock();
}

void Worker::update(const RoboCompAGMWorldModel::Node &r)
{
	mutex->lock();
	prms.executiveTopic->modelUpdated(r);
	mutex->unlock();
}

void Worker::printSomeInfo(const RoboCompAGMWorldModel::Event &event)
{
	if (generateTXT) 
	{
		fprintf(fd, "\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n");
		fprintf(fd, "Time: %d:%d:%d\n", time.hour(), time.minute(), time.second()); 
		fprintf(fd, "Sender: %s\n", event.sender.c_str());
		char mimimi[1000];
		sprintf(mimimi, "modification%d.txt", numberOfModificationsProposed++);
		fprintf(fd, "File: %s\n", mimimi);
		FILE *fdw = fopen(mimimi, "w");
		if (fdw != NULL)
		{
			fprintf(fdw, "Why:    %d\n", event.why);
			fprintf(fdw, "Who:    %s\n", event.sender.c_str());
			fprintf(fdw, "Back:\n");
			fprintf(fdw, "------------------------------------------------------\n");
			AGMModelPrinter::printWorld(fdw, event.backModel);
			fprintf(fdw, "------------------------------------------------------\n");
			fprintf(fdw, "New:\n");
			fprintf(fdw, "------------------------------------------------------\n");
			AGMModelPrinter::printWorld(fdw, event.newModel);
			fprintf(fdw, "------------------------------------------------------\n");
			fclose(fdw);
		}
		fflush(fd);
	}
}

bool Worker::handleModificationProposal(const RoboCompAGMWorldModel::Event &event)
{
	mutex->lock();
	printSomeInfo(event);

	if (eventIsCompatibleWithTheCurrentModel(event) )
	{
		prms.executiveTopic->modelModified(event);
		AGMModelConverter::fromIceToInternal(event.newModel, worldModel);
	}
	else
	{
		qDebug() << "Got incompatible change!";
		mutex->unlock();
		return false;
	}

	handleAcceptedModificationProposal();
	mutex->unlock();
	return true;
}



Worker::~Worker()
{

}

void Worker::run()
{
	time = QTime::currentTime();
	QDate date = QDate::currentDate();
	fprintf(fd, "\n\n####################################################################\n");
	fprintf(fd,     "####################################################################\n");
	fprintf(fd,     "#### %d/%d/%d %d:%d:%d #### EXECUTION STARTED ####\n", date.year(), date.month(), date.day(), time.hour(), time.minute(), time.second());
	fprintf(fd,     "####################################################################\n");
	fprintf(fd,     "####################################################################\n");

	for(;;)
	{
		printf("waiting..\n");
		processMutex->lock();
		loopMethod();
	}
}


void Worker::loopMethod()
{
// 	if (not active) return;
	mutex->lock();

	printf("fff\n");
	/// Process new events
	RoboCompAGMWorldModel::Event event;
	while (not eventQueue.isEmpty())
	{
		printf("eee\n");
		event = eventQueue.dequeue();
		printSomeInfo(event);
		if (eventIsCompatibleWithTheCurrentModel(event) )
		{
			eventQueue.clear();
			prms.executiveTopic->modelModified(event);
			AGMModelConverter::fromIceToInternal(event.newModel, worldModel);
			printf("Agent %s sent a COMPATIBLE event.\n", event.sender.c_str());
		}
		else
		{
			printf("Agent %s sent an INcompatible event.\n", event.sender.c_str());
			printf("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
			AGMModelPrinter::printWorld(event.backModel);
			printf("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n");
			AGMModelPrinter::printWorld(event.newModel);
		}
		if (generateTXT) 
			fflush(fd);
	}

	handleAcceptedModificationProposal();
	mutex->unlock();
}


void Worker::handleAcceptedModificationProposal()
{
	/// Get mission
	printf("handleAcceptedModificationProposal dd\n");

	/// Get problem string based on the new mission and the current model
	std::string problemPDDLString = worldModel->generatePDDLProblem(targetModel, 7, "gualzruGrammar", "problemo");

	/// Get solution to the problem
	if (problemPDDLString.size()>0)
	{
		try
		{
			bool gotPlan = false;
			planString = "";
			currentSolution.cost = 0;
			currentSolution.actions.clear();
			int32_t ret;
			if (missionChanged)
				ret = prms.pelea->getSolution(prms.agm->partialPDDLContent, problemPDDLString, currentSolution);
			else
				ret = prms.pelea->getNextAction(problemPDDLString, currentSolution);
			if (ret)
			{
				printf("got plan\n");
				gotPlan = true;
				if (currentSolution.actions.size() > 0)
				{
					/// Fill plan string
					planString = "";
					for (uint32_t ac=0; ac<currentSolution.actions.size(); ac++)
					{
						planString += "(";
						planString += currentSolution.actions[ac].name + " ";
						for (uint32_t sy=0; sy<currentSolution.actions[ac].symbols.size(); sy++)
						{
							planString += currentSolution.actions[ac].symbols[sy] + " ";
						}
						planString += ")\n";
					}
				}
			}

			if (gotPlan && currentSolution.actions.size()>0)
			{
				reactivateAgents();
				RoboCompAGMWorldModel::World targetModelICE;
				RoboCompAGMWorldModel::World worldModelICE;
				AGMModelConverter::fromInternalToIce(targetModel, targetModelICE);
				AGMModelConverter::fromInternalToIce( worldModel,  worldModelICE);
				prms.executiveVisualizationTopic->update(worldModelICE, targetModelICE, currentSolution);
			}
			else
			{
				if (gotPlan)
				{
					printf("Goal achieved!\n :-)");
				}
				else
				{
					printf("PROBLEM STRING\n");
					printf("%s\n", problemPDDLString.c_str());
					printf("GRAMMAR STRING\n");
					printf("%s\n", prms.agm->partialPDDLContent.c_str());
					printf("No solution. :-(\n");
				}
			}
		}
		catch(RoboCompPlanning::ServerException exc)
		{
			printf("Can't compute a plan for the proposed target!\n\t%s\n", exc.what.c_str());
			fprintf(fd, "Can't compute a plan for the proposed target!\n\t%s\n", exc.what.c_str());
		}
	}
	else
	{
		printf("No plans... should I commit suicide?\n");
	}
}


bool Worker::eventIsCompatibleWithTheCurrentModel(const RoboCompAGMWorldModel::Event &event) const
{
	static AGMModel::SPtr tempTargetWorldModel = AGMModel::SPtr(new AGMModel());

	printf("\nBACK\n");
	AGMModelPrinter::printWorld(event.backModel);
	printf("\n\nNEW\n");
	AGMModelPrinter::printWorld(event.newModel);

	
	try
	{
		AGMModelConverter::fromIceToInternal(event.newModel, tempTargetWorldModel);
	}
	catch(std::string ss)
	{
		printf("Error (string): %s\n", ss.c_str());
		return false;
	}
	catch(...)
	{
		printf("Error (unknown)\n");
		return false;
	}

	RoboCompPlanning::Plan tempSolution;
#ifndef AVOID_MODEL_CHECKING
	std::string modificationPDDLString = worldModel->generatePDDLProblem(tempTargetWorldModel, 5, "gualzruGrammar", "problemo");
	if (prms.planning->getSolution(prms.agm->fullPDDLContent, modificationPDDLString, tempSolution))
	{
#endif
		prms.executiveVisualizationTopic->successFulChange(tempSolution.actions);
		printf("Everythin nice\n");
		return true;
#ifndef AVOID_MODEL_CHECKING
	}
	else
	{
		prms.executiveVisualizationTopic->invalidChange(event.sender);
		printf("Error NOT COMPATIBLE\n\n%s\n\n", modificationPDDLString.c_str());
		return false;
	}
#endif
}


void Worker::reactivateAgents()
{
	printf("prms.agents.size() %ld\n", prms.agents.size());
	for (uint i=0; i<prms.agents.size(); i++)
	{
		printf("\tAGENT: %s\n", prms.agents[i].c_str());
		try
		{
			// Print info
			if (generateTXT) fprintf(fd, "activating agent %s\n", prms.agents[i].c_str());
			// Build parameters' map
			ParameterMap pm;
			Parameter p;
			p.editable = true;
			// Action parameter
			p.editable = true;
			p.type = "string";
			p.value = currentSolution.actions[0].name;
			for (uint uu=0; uu<currentSolution.actions[0].symbols.size(); ++uu)
			{
				p.value += std::string(" ") + currentSolution.actions[0].symbols[uu];
			}
			pm["action"] = p;
			// Plan parameter
			p.editable = true;
			p.type = "string";
			p.value = planString;
			pm["plan"] = p;

			// Activation
			bool ok = prms.agentProxies[prms.agents[i]]->activateAgent(pm);
			if (not ok)
			{
				fprintf(stdout, "There was some problem activating agent %s\n", prms.agents[i].c_str());
			}
		}
		catch(...)
		{
			qDebug() << "Couldn't reach agent" << prms.agents[i].c_str();
		}
	}

	qDebug() << "Behaviors activated!! -- ";
}

void Worker::reset()
{
	printf("reset...\n");
	// Create event
	RoboCompAGMWorldModel::Event e;
	e.why    = RoboCompAGMWorldModel::InitialWorld;
	e.sender = "executive";

	// New model
	worldModel->clear();
	worldModel->resetLastId();
	worldModel->name = "worldModelReseted";
	worldModel->newSymbol("startsymbol");
	AGMModelConverter::fromInternalToIce(worldModel, e.backModel);
	AGMModelConverter::fromInternalToIce(worldModel, e.newModel);

	prms.executiveTopic->modelModified(e);
	printf("reset done...\n");
	handleAcceptedModificationProposal();
	printf("reset done 2...\n");
}

void Worker::broadcastModel()
{
	RoboCompAGMWorldModel::Event e;
	e.why    = RoboCompAGMWorldModel::InitialWorld;
	e.sender = "executive";
	AGMModelConverter::fromInternalToIce(worldModel, e.backModel);
	AGMModelConverter::fromInternalToIce(worldModel, e.newModel);
	prms.executiveTopic->modelModified(e);
}


