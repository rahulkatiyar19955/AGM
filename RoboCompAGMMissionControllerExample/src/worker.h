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
m *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
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
#include <IceStorm/IceStorm.h>

#include <AGMExecutive.h>
#include <AGMAgent.h>
#include <AGMCommonBehavior.h>
#include <Planning.h>

#include "config.h"

#include <agm_model.h>

#ifdef USE_QTGUI
	#include <agm_modelDrawer.h>
	#include "ui_guiDlg.h"
#endif


#define BASIC_PERIOD 30

using namespace std;

/**
       \brief
       @author authorname
*/
class Worker :
#ifdef USE_QTGUI
 public QWidget, public Ui_GualzruVisualizer
#else
 public QObject
#endif
{
Q_OBJECT
public:
	Worker(RoboCompAGMAgent::AGMAgentTopicPrx behaviorTopic_, RoboCompAGMExecutive::AGMExecutivePrx executive_proxy_);
	~Worker();

	bool refresh;
	QMutex *mutex;

	void update(const RoboCompAGMWorldModel::World &world_, const RoboCompAGMWorldModel::World &target_, const RoboCompPlanning::Plan &plan_);
	void modelModified(const RoboCompAGMWorldModel::Event &modification);
	void modelUpdated(const RoboCompAGMWorldModel::Node &modification);

private:
	AGMModel::SPtr worldModel;
	AGMModel::SPtr targetModel;
	RoboCompPlanning::Plan plan;

	RoboCompAGMWorldModel::World worldModelICE, targetModelICE;
	QTimer timer;
	
	RoboCompAGMAgent::AGMAgentTopicPrx behaviorTopic;
	RoboCompAGMExecutive::AGMExecutivePrx executive;

	RCDraw *worldModelDraw, *targetModelDraw;
	AGMModelDrawer *worldModelDrawer, *targetModelDrawer;
signals:
	void kill();
	
public slots:
	void compute();
	void activate();
	void deactivate();
	void closeEvent(QCloseEvent *event);
	void broadcastB();
	void resetB();
};

#endif
