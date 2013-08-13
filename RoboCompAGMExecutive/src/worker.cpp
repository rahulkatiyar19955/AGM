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
	prms = parameters;

	mutex = new QMutex();
	processMutex = new QMutex();

	numberOfModificationsProposed = 0;

	fd = fopen("executive_results.txt", "w");
	if (fd==NULL)
	{
		printf("Can't open executive_results.txt for writing\n");
		exit(-1);
	}


	std::locale::global(std::locale("C"));

	worldModel = AGMModel::SPtr(new AGMModel());
	worldModel->newSymbol("startsymbol");
	AGMModelPrinter::printWorld(worldModel);

	
	targetModel = AGMModel::SPtr(new AGMModel());

	/// Read the grammar file and store it in a string
	grammarPDDLString = prms.grammarPDDLString;

	RoboCompAGMWorldModel::Event e;
	e.why    = RoboCompAGMWorldModel::InitialWorld;
	e.sender = "executive";
	AGMModelConverter::fromInternalToIce(worldModel, e.backModel);
	AGMModelConverter::fromInternalToIce(worldModel, e.newModel);
	prms.executiveTopic->modelModified(e);
	AGMModelPrinter::printWorld(worldModel);
}

void AGMAgentTopicI::modificationProposal(const RoboCompAGMWorldModel::Event &result, const Ice::Current&)
{
	qDebug() << "Event from: " << result.sender.c_str();
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
		processMutex->lock();
		setCurrentBehavioralConfiguration();
	}
}


void Worker::setCurrentBehavioralConfiguration()
{
	printf("setCurrentBehavioralConfiguration\n");
	if (not active) return;
	mutex->lock();

	/// Process new events
	RoboCompAGMWorldModel::Event event;
	while (not eventQueue.isEmpty())
	{
		event = eventQueue.dequeue();
		printSomeInfo(event);

		if (eventIsCompatibleWithTheCurrentModel(event) )
		{
			eventQueue.clear();
			prms.executiveTopic->modelModified(event);
			AGMModelConverter::fromIceToInternal(event.newModel, worldModel);
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
	std::string problemPDDLString = worldModel->generatePDDLProblem(targetModel, 6, "gualzruGrammar", "problemo");

	/// Get solution to the problem
	if (problemPDDLString.size()>0)
	{
		try
		{
			if (prms.planning->getSolution(grammarPDDLString, problemPDDLString, currentSolution))
			{
				if (currentSolution.actions.size() > 0)
				{
					currentBehavioralConfiguration = prms.agm->action2behavior[currentSolution.actions[0].name];
					if (currentBehavioralConfiguration == "")
						qFatal("No behavior associated with rule %s: Take a look at the AGMBD file.\n", currentSolution.actions[0].name.c_str());
				}
				else
				{
					currentBehavioralConfiguration = "";
				}
				executeCurrentBehavioralConfiguration();
				RoboCompAGMWorldModel::World targetModelICE;
				RoboCompAGMWorldModel::World worldModelICE;
				AGMModelConverter::fromInternalToIce(targetModel, targetModelICE);
				AGMModelConverter::fromInternalToIce( worldModel,  worldModelICE);
				prms.executiveVisualizationTopic->update(worldModelICE, targetModelICE, currentSolution);
			}
			else
			{
				printf("%s\n", problemPDDLString.c_str());
				qFatal("No solution. :-(");
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
	RoboCompPlanning::Plan tempSolution;
	static AGMModel::SPtr tempTargetWorldModel = AGMModel::SPtr(new AGMModel());

	try
	{
		AGMModelConverter::fromIceToInternal(event.newModel, tempTargetWorldModel);
	}
	catch(std::string ss)
	{
		printf("Error 1: %s\n", ss.c_str());
		return false;
	}
	catch(...)
	{
		printf("Error 2\n");
		return false;
	}

	std::string modificationPDDLString = worldModel->generatePDDLProblem(tempTargetWorldModel, 5, "gualzruGrammar", "problemo");

	if (prms.planning->getSolution(grammarPDDLString, modificationPDDLString, tempSolution))
	{
		printf("Everythin nice\n");
		return true;
	}
	else
	{
		printf("Error NOT COMPATIBLE\n\n%s\n\n", modificationPDDLString.c_str());
		return false;
	}
}


void Worker::executeCurrentBehavioralConfiguration()
{
	if (currentBehavioralConfiguration.size() == 0)
		return;

	prms.speech->say(currentBehavioralConfiguration, true);
	std::cout << currentBehavioralConfiguration << std::endl;
	std::cout << currentBehavioralConfiguration << std::endl;
	std::cout << currentBehavioralConfiguration << std::endl;

// 	std::map<AGMAgentConigNamePair, AGMState>
	AGMConfigTable &table = prms.agm->table.table;
	AGMAgentVector &agents = prms.agm->table.agents;

	for (uint i=0; i<agents.size(); i++)
	{
		printf("\tAGENT: %s\n", agents[i].getName().c_str());
		try
		{
			AGMState state = table[AGMAgentConigNamePair(agents[i].getName(), currentBehavioralConfiguration)];
			printf("\t\tstate: %s\n", state.c_str());
			try
			{
				// Print info
				if (generateTXT) fprintf(fd, "activating %s behavior of agent %s\n", state.c_str(), agents[i].getName().c_str());
				// Build parameters' map
				ParameterMap pm;
				Parameter p;
				p.editable = true;
				p.type = "string";
				p.value = state;
				pm["mode"] = p;
				p.value = currentSolution.actions[0].name;
				for (uint uu=0; uu<currentSolution.actions[0].symbols.size(); ++uu)
				{
					p.value += std::string(" ") + currentSolution.actions[0].symbols[uu];
				}
				pm["action"] = p;
				// Activation
				bool ok = prms.agentProxies[agents[i].getName()]->activateAgent(pm);
				if (not ok)
				{
					fprintf(stdout, "There was some problem activating agent %s\n", agents[i].getName().c_str());
				}
			}
			catch(...)
			{
				qDebug() << "Couldn't reach agent" << agents[i].getName().c_str();
			}
		}
		catch(...)
		{
			qFatal("No configuration for %s --> %s seems to exist", currentBehavioralConfiguration.c_str(), agents[i].getName().c_str());
		}
	}

	qDebug() << "Behaviors activated!! -- ";
}

void Worker::reset()
{
	// Create event
	RoboCompAGMWorldModel::Event e;
	e.why    = RoboCompAGMWorldModel::InitialWorld;
	e.sender = "executive";

	// New model
	worldModel->clear();
	worldModel->name = "worldModelReseted";
	worldModel->newSymbol("startsymbol");
	AGMModelConverter::fromInternalToIce(worldModel, e.backModel);
	AGMModelConverter::fromInternalToIce(worldModel, e.newModel);

	prms.executiveTopic->modelModified(e);
	handleAcceptedModificationProposal();
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


