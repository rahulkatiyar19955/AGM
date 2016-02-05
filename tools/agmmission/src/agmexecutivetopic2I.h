/*
 *    Copyright (C) 2016 by YOUR NAME HERE
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
#ifndef AGMEXECUTIVETOPIC2_H
#define AGMEXECUTIVETOPIC2_H

// QT includes
#include <QtCore/QObject>

// Ice includes
#include <Ice/Ice.h>
#include <AGMExecutive2.h>

#include <config.h>
#include "genericworker.h"

using namespace RoboCompAGMExecutive2;

class AGMExecutiveTopic2I : public QObject , public virtual RoboCompAGMExecutive2::AGMExecutiveTopic2
{
Q_OBJECT
public:
	AGMExecutiveTopic2I( GenericWorker *_worker, QObject *parent = 0 );
	~AGMExecutiveTopic2I();
	
	void structuralChange(const RoboCompAGMWorldModel2::World  &w, const Ice::Current&);
	void edgesUpdated(const RoboCompAGMWorldModel2::EdgeSequence  &es, const Ice::Current&);
	void edgeUpdated(const RoboCompAGMWorldModel2::Edge  &e, const Ice::Current&);
	void symbolUpdated(const RoboCompAGMWorldModel2::Node  &n, const Ice::Current&);
	void symbolsUpdated(const RoboCompAGMWorldModel2::NodeSequence  &ns, const Ice::Current&);

	QMutex *mutex;
private:

	GenericWorker *worker;
public slots:


};

#endif
