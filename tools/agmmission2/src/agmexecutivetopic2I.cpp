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
#include "agmexecutivetopic2I.h"

AGMExecutiveTopic2I::AGMExecutiveTopic2I(GenericWorker *_worker, QObject *parent) : QObject(parent)
{
	worker = _worker;
	mutex = worker->mutex;       // Shared worker mutex
}


AGMExecutiveTopic2I::~AGMExecutiveTopic2I()
{
}

void AGMExecutiveTopic2I::structuralChange(const RoboCompAGMWorldModel2::World  &w, const Ice::Current&)
{
	worker->structuralChange(w);
}

void AGMExecutiveTopic2I::edgesUpdated(const RoboCompAGMWorldModel2::EdgeSequence  &es, const Ice::Current&)
{
	worker->edgesUpdated(es);
}

void AGMExecutiveTopic2I::edgeUpdated(const RoboCompAGMWorldModel2::Edge  &e, const Ice::Current&)
{
	worker->edgeUpdated(e);
}

void AGMExecutiveTopic2I::symbolUpdated(const RoboCompAGMWorldModel2::Node  &n, const Ice::Current&)
{
	worker->symbolUpdated(n);
}

void AGMExecutiveTopic2I::symbolsUpdated(const RoboCompAGMWorldModel2::NodeSequence  &ns, const Ice::Current&)
{
	worker->symbolsUpdated(ns);
}






