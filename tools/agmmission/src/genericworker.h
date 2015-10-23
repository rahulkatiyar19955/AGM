/*
 *    Copyright (C) 2006-2010 by RoboLab - University of Extremadura
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
#ifndef GENERICWORKER_H
#define GENERICWORKER_H

// #include <ipp.h>
#include <QtGui>
#include <stdint.h>
#include <qlog/qlog.h>
#include <CommonBehavior.h>
#include <ui_guiDlg.h>
#include "config.h"
#include <AGMExecutive.h>
#include <AGMAgent.h>
#include <AGMCommonBehavior.h>
#include <AGMExecutive.h>

#define CHECK_PERIOD 5000
#define BASIC_PERIOD 100

typedef map <string,::IceProxy::Ice::Object*> MapPrx;

using namespace std;

/**
       \brief
       @author authorname
*/
using namespace RoboCompAGMExecutive;
using namespace RoboCompAGMCommonBehavior;
using namespace RoboCompAGMExecutive;
using namespace RoboCompAGMAgent;
class GenericWorker :
#ifdef USE_QTGUI
public QWidget, public Ui_guiDlg
#else
public QObject
#endif
{
Q_OBJECT
public:
	GenericWorker(MapPrx& mprx);
	virtual ~GenericWorker();
	virtual void killYourSelf();
	virtual void setPeriod(int p);
	
	virtual bool setParams(RoboCompCommonBehavior::ParameterList params) = 0;
	QMutex *mutex;                //Shared mutex with servant

	AGMExecutivePrx agmexecutive_proxy;
	AGMAgentTopicPrx agmagenttopic;
	virtual bool activateAgent(const ParameterMap& params) = 0;
	virtual bool deactivateAgent() = 0;
	virtual StateStruct getAgentState() = 0;
	virtual ParameterMap getAgentParameters() = 0;
	virtual bool setAgentParameters(const ParameterMap& params) = 0;
	virtual void  killAgent() = 0;
	virtual int uptimeAgent() = 0;
	virtual bool reloadConfigAgent() = 0;
	virtual void  structuralChange(const RoboCompAGMWorldModel::Event& modification) = 0;
	virtual void  symbolUpdated(const RoboCompAGMWorldModel::Node& modification) = 0;
	virtual void  edgeUpdated(const RoboCompAGMWorldModel::Edge& modification) = 0;

	virtual void  update(const RoboCompAGMWorldModel::World& world, const RoboCompAGMWorldModel::World& target, const RoboCompPlanning::Plan& plan) = 0;

protected:
	QTimer timer;
	int Period;
public slots:
	virtual void compute() = 0;
signals:
	void kill();
};

#endif