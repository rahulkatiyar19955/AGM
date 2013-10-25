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
#pragma once

#include "config.h"

#include <QtGui>
#include <stdint.h>
#include <qlog/qlog.h>

#include <Planning.h>
#include <Speech.h>
#include <AGMExecutive.h>
#include <AGMCommonBehavior.h>
#include <AGMAgent.h>
#include <AGMWorldModel.h>

#include <IceStorm/IceStorm.h>

#include <agm.h>
#include <agm_model.h>



#define BASIC_PERIOD 100


using namespace RoboCompAGMCommonBehavior;

class Worker;

class AGMAgentTopicI : virtual public RoboCompAGMAgent::AGMAgentTopic
{
public:
	AGMAgentTopicI(Worker *worker_)
	{
		worker = worker_;
	}
	virtual void modificationProposal(const RoboCompAGMWorldModel::Event &result, const Ice::Current&);
	virtual void update(const RoboCompAGMWorldModel::Node &node, const Ice::Current&);
private:
	Worker *worker;
};


typedef std::map<std::string, RoboCompAGMCommonBehavior::AGMCommonBehaviorPrx> AgentMap;

class WorkerParameters
{
public:
	/// GualzruExecutive topic publishing proxy
	RoboCompAGMExecutive::AGMExecutiveTopicPrx executiveTopic;
	/// GualzruExecutive Visualization topic publishing proxy
	RoboCompAGMExecutive::AGMExecutiveVisualizationTopicPrx executiveVisualizationTopic;
	/// Proxy to the planner
	RoboCompPlanning::PlanningPrx planning;
	/// Proxy to speech
	RoboCompSpeech::SpeechPrx speech;
	/// Proxy to the planner
	RoboCompPlanning::PlanningPrx pelea;

	/// Generic AGM Stuff
	AGM *agm;
	std::string initialModelXML;

	std::vector <std::string> agents;
	AgentMap agentProxies;
};


/**
	\brief
	@author authorname
*/
class AGMExecutiveI;

class Worker  : public QThread
{
Q_OBJECT
friend class AGMExecutiveI;
public:
	Worker(WorkerParameters &config);
	~Worker();

	QMutex *mutex;
	QMutex *processMutex;
	QQueue <RoboCompAGMWorldModel::Event> eventQueue;

	void enqueueEvent(const RoboCompAGMWorldModel::Event &r);
	void update(const RoboCompAGMWorldModel::Node &r);
	void run();
	void reset();
	void broadcastModel();


	AGMModel::SPtr worldModel;
	AGMModel::SPtr targetModel;
	bool missionChanged;
	RoboCompPlanning::Plan currentSolution;

	int numberOfModificationsProposed;
	FILE *fd;
	QTime time;
private:
	bool active;
	int Period;
	WorkerParameters prms;
	void printSomeInfo(const RoboCompAGMWorldModel::Event &e);

	bool eventIsCompatibleWithTheCurrentModel(const RoboCompAGMWorldModel::Event &event) const;

	void loopMethod();
	void reactivateAgents();

// 	bool behaviorActivated;

	std::string planString;

	void handleAcceptedModificationProposal();

	bool handleModificationProposal(const RoboCompAGMWorldModel::Event &proposal);


signals:
	void kill();
};


