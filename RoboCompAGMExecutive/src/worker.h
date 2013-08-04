/*
 *    Copyright (C) 2006-2011 by RoboLab - University of Extremadura
 *
 *    This file is part of RoboComp
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
#ifndef WORKER_H
#define WORKER_H

#include <QtGui>
#include <stdint.h>
#include <qlog/qlog.h>

#include <Planning.h>
#include <Speech.h>
#include <InnerModelManager.h>
#include <GualzruExecutive.h>
#include <GualzruBehavior.h>
#include <GualzruCommonBehavior.h>

#include <IceStorm/IceStorm.h>

#include <agm.h>
#include <agm_model.h>

#include "config.h"


#define BASIC_PERIOD 100

typedef RoboCompInnerModelManager::NodeInformationSequence RCISSeq;

using namespace RoboCompGualzruCommonBehavior;

class Worker;

class GualzruBehaviorTopicI : virtual public RoboCompGualzruBehavior::GualzruBehaviorTopic
{
public:
	GualzruBehaviorTopicI(Worker *worker_)
	{
		worker = worker_;
	}
	virtual void modificationProposal(const RoboCompWorldModel::ModelEvent &result, const Ice::Current&);
	virtual void update(const RoboCompWorldModel::GualzruWorldNode &node, const Ice::Current&);
private:
	Worker *worker;
};


typedef std::map<std::string, RoboCompGualzruCommonBehavior::GualzruCommonBehaviorPrx> AgentMap;

class WorkerParameters
{
public:
	/// GualzruExecutive topic publishing proxy
	RoboCompExecutive::ExecutiveTopicPrx executiveTopic;
	/// GualzruExecutive Visualization topic publishing proxy
	RoboCompExecutive::ExecutiveVisualizationTopicPrx executiveVisualizationTopic;
	/// Proxy to the planner
	RoboCompPlanning::PlanningPrx planning;
	/// Proxy to speech
	RoboCompSpeech::SpeechPrx speech;
	/// Proxy to InnerModelManager
	RoboCompInnerModelManager::InnerModelManagerPrx immanager;


	AGM *agm;
	AgentMap agentProxies;

	std::string pddlPath;
	std::string agmbdPath;
	std::string grammarPDDLString;


};


struct ModificationListsContainer
{
	// Nodes                        GualzruWorldNode
	RoboCompWorldModel::NodeSequence newNodes;
	RoboCompWorldModel::NodeSequence constantNodes;
	RoboCompWorldModel::NodeSequence removedNodes;
	// Edges
	RoboCompWorldModel::EdgeSequence newEdges;
	RoboCompWorldModel::EdgeSequence constantEdges;
	RoboCompWorldModel::EdgeSequence removedEdges;
};

/**
       \brief
       @author authorname
*/
class ExecutiveI;
class Worker  : public QThread
{
Q_OBJECT
friend class ExecutiveI;
public:
	Worker(WorkerParameters &config);
	~Worker();

	QMutex *mutex;
	QMutex *processMutex;
	QQueue <RoboCompWorldModel::ModelEvent> eventQueue;

	void enqueueEvent(const RoboCompWorldModel::ModelEvent &r);
	void update(const RoboCompWorldModel::GualzruWorldNode &r);
	void run();
	void reset();
	void broadcastModel();


	AGMModel::SPtr worldModel;
	AGMModel::SPtr targetModel;
	RoboCompPlanning::Plan currentSolution;

	int numberOfModificationsProposed;
	FILE *fd;
	QTime time;
private:
	bool active;
	int Period;
	WorkerParameters prms;
	void printSomeInfo(const RoboCompWorldModel::ModelEvent &e);

	bool eventIsCompatibleWithTheCurrentModel(const RoboCompWorldModel::ModelEvent &event) const;

	string currentBehavioralConfiguration;
	void setCurrentBehavioralConfiguration();
	void executeCurrentBehavioralConfiguration();

	bool behaviorActivated;

	std::string grammarPDDLString;

	void handleAcceptedModificationProposal();

	bool handleModificationProposal(const RoboCompWorldModel::ModelEvent &proposal);
// 	bool handleUpdate(const RoboCompWorldModel::GualzruWorldNode &update);
	
	
	/** RCIS - Imagination **/
	/** RCIS - Imagination **/
	void updateRCISModel();
	void updateRCISNode(const RoboCompWorldModel::GualzruWorldNode &r);
	std::string node2String(const RoboCompWorldModel::GualzruWorldNode &node);
	void buildModificationLists(const RoboCompWorldModel::ModelEvent &event);
	ModificationListsContainer modificationList;
	void buildNodeModificationLists(const RoboCompWorldModel::ModelEvent &event);
	void buildEdgeModificationLists(const RoboCompWorldModel::ModelEvent &event);

	void RCIS_addRobotNode         (RoboCompWorldModel::GualzruWorldNode &node);
	void RCIS_addFloorNode         (RoboCompWorldModel::GualzruWorldNode &node);
	void RCIS_addOrientedFloorNode (RoboCompWorldModel::GualzruWorldNode &node);
	void RCIS_addWallNode          (RoboCompWorldModel::GualzruWorldNode &node);

	void RCIS_updateOrientedFloorNode (RoboCompWorldModel::GualzruWorldNode &node);
	void RCIS_updateRoomNode          (RoboCompWorldModel::GualzruWorldNode &node);
	void RCIS_updateWallNode          (RoboCompWorldModel::GualzruWorldNode &node);


	void RCIS_imaginateRobotMesh(float neckAngle, float yaw);
	void RCIS_imaginateRoom(float robotYaw, float height, float robotPitch);

	void RCIS_removeNode_nonexistingok(std::string nodeName);
	void RCIS_addTransform_existingsetfromparent(std::string nodeName, std::string parentName, RoboCompInnerModelManager::Pose3D pose);
	void RCIS_addPlane_existingsetfromparent(std::string nodeName, std::string parentName, RoboCompInnerModelManager::Plane3D plane);

	/** RCIS - Imagination **/
	/** RCIS - Imagination **/

signals:
	void kill();
};

#endif
