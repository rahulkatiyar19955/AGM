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
#include "worker.h"

#include <agm_modelConverter.h>
#include <agm_modelPrinter.h>

/**
* \brief Default constructor
*/

Worker::Worker(RoboCompAGMAgent::AGMAgentTopicPrx behaviorTopic_, RoboCompAGMExecutive::AGMExecutivePrx executive_proxy_) :
#ifdef USE_QTGUI
QWidget(NULL), Ui_GualzruVisualizer()
#else
QObject(NULL)
#endif
{
	behaviorTopic = behaviorTopic_;
	executive = executive_proxy_;

	refresh = false;
	mutex = new QMutex();
	worldModel = AGMModel::SPtr(new AGMModel());
	targetModel = AGMModel::SPtr(new AGMModel());



#ifdef USE_QTGUI
	setupUi(this);
// 	connect(activeCheck, SIGNAL(stateChanged(int)), this, SLOT(activeStateChanged(int)));
	connect(activateButton, SIGNAL(clicked()), this, SLOT(activate()));
	connect(deactivateButton, SIGNAL(clicked()), this, SLOT(deactivate()));
	worldModelDraw  = new RCDraw(800, 600, modelGraph);
	targetModelDraw = new RCDraw(400, 400, targetGraph);
	worldModelDrawer = new AGMModelDrawer(worldModelDraw, tableWidget);
	targetModelDrawer = new AGMModelDrawer(targetModelDraw);
	worldModelDraw->removeImage();
	targetModelDraw->removeImage();
	show();
#endif

	connect(resetButton,     SIGNAL(clicked()), this, SLOT(resetB()));
	connect(broadcastButton, SIGNAL(clicked()), this, SLOT(broadcastB()));

	connect(&timer, SIGNAL(timeout()), this, SLOT(compute()));
	timer.start(150);
}

/**
* \brief Default destructor
*/
Worker::~Worker()
{

}

void Worker::activate()
{
	try
	{
		executive->activate();
	}
	catch(...)
	{
		printf("gualzru_visualizer: Error: Can't communicate with executive\n");
	}
}

void Worker::deactivate()
{
	try
	{
		executive->deactivate();
	}
	catch(...)
	{
		printf("gualzru_visualizer: Error: Can't communicate with executive\n");
	}
}

void Worker::compute()
{
	mutex->lock();

	if (refresh)
	{
		refresh = false;
		/// Print PLAN
		QString planString;
		for (uint i=0; i<plan.actions.size(); ++i)
		{
			planString += QString::fromStdString(plan.actions[i].name);
			planString += " ( ";
			if (plan.actions[i].symbols.size() > 0)
				planString += QString::fromStdString(plan.actions[i].symbols[0]);
			for (uint s=1; s<plan.actions[i].symbols.size(); ++s)
			{
				planString += ", ";
				planString += QString::fromStdString(plan.actions[i].symbols[0]);
			}
			planString += " )\n";
		}
		planText->clear();
		planText->setText(planString);
	}

	/// Draw models
	worldModelDrawer->update(worldModel);
	targetModelDrawer->update(targetModel);



	mutex->unlock();


	static bool forceSent = true;
	static bool thereWasARoom = false;
	bool thereIsARoom = (worldModel->indexOfFirstSymbolByType("room") != -1);
	printf("thereIsARoom? %d\n", thereIsARoom);
	if (thereWasARoom != thereIsARoom or forceSent)
	{
		AGMModel::SPtr target(new AGMModel());
		if (not thereIsARoom)
		{
			target->newSymbol("room");
		}
		else
		{
			target->newSymbol("mug");
		}
		AGMModelConverter::fromInternalToIce(target, targetModelICE);
		executive->setMission(targetModelICE);
	}
	thereWasARoom = thereIsARoom;
	

	static int p=0;
	if (p++%10==0)
	{
		if (worldModelDraw->autoResize())
			worldModelDraw->setWindow(QRect(0, 0, worldModelDraw->getWidth(), worldModelDraw->getHeight()));
		if (targetModelDraw->autoResize())
			targetModelDraw->setWindow(QRect(0, 0, targetModelDraw->getWidth()/2, targetModelDraw->getHeight()/2));
	}
}



void Worker::modelModified(const RoboCompAGMWorldModel::Event &modification)
{
	mutex->lock();
	AGMModelConverter::fromIceToInternal(modification.newModel, worldModel);
	printf("MODEL MODIFIED (%s)\n", modification.sender.c_str());
	AGMModelPrinter::printWorld(worldModel);
	mutex->unlock();
}

void Worker::modelUpdated(const RoboCompAGMWorldModel::Node &modification)
{
	mutex->lock();
	AGMModelConverter::includeIceModificationInInternalModel(modification, worldModel);
	printf("MODEL UPDATED\n");
	AGMModelPrinter::printWorld(worldModel);
	mutex->unlock();
}


void Worker::update(const RoboCompAGMWorldModel::World &world_, const RoboCompAGMWorldModel::World &target_, const RoboCompPlanning::Plan &plan_)
{
	mutex->lock();
	worldModelICE = world_;
	targetModelICE = target_;
	AGMModelConverter::fromIceToInternal(world_,  worldModel);
	AGMModelConverter::fromIceToInternal(target_, targetModel);
	plan = plan_;
	refresh = true;
	mutex->unlock();
}

void Worker::closeEvent(QCloseEvent *event)
{
	exit(-1);
}

void Worker::resetB()
{
	executive->deactivate();
	executive->reset();
	executive->activate();
}

void Worker::broadcastB()
{
	executive->broadcastModel();
}


