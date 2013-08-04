/*
 *    Copyright (C) 2006-2012 by RoboLab - University of Extremadura
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
#ifndef EXECUTIVEI_H
#define EXECUTIVEI_H

#include <Ice/Ice.h>
#include <GualzruExecutive.h>

#include <config.h>
#include "worker.h"

#include <agm_modelConverter.h>

using namespace RoboCompExecutive;

class ExecutiveI :  public virtual RoboCompExecutive::Executive
{
public:
	ExecutiveI(Worker *_worker)
	{
		worker = _worker;
	}
	
	void deactivate(const Ice::Current & = Ice::Current())
	{
		worker->mutex->lock();
		worker->active = false;
		fclose(worker->fd);
		worker->mutex->unlock();
	}
	
	void activate(const Ice::Current & = Ice::Current())
	{
		worker->mutex->lock();
		worker->active = true;
		worker->processMutex->unlock();
		worker->mutex->unlock();
	}

	void getData(RoboCompWorldModel::GualzruWorld &world, RoboCompWorldModel::GualzruWorld &target, RoboCompPlanning::Plan &plan, const Ice::Current & = Ice::Current())
	{
		worker->mutex->lock();
		AGMModelConverter::fromInternalToIce(worker->worldModel,  world);
		AGMModelConverter::fromInternalToIce(worker->targetModel, target);
		plan = worker->currentSolution;
		worker->mutex->unlock();
	}
	
	void broadcastModel(const Ice::Current &c = Ice::Current())
	{
		worker->broadcastModel();
	}
	
	void reset(const Ice::Current &c= Ice::Current())
	{
		worker->reset();
	}
	

	bool modificationProposal(const RoboCompWorldModel::ModelEvent &proposal, const Ice::Current&)
	{
		return worker->handleModificationProposal(proposal);
	}
/*
	bool update(const RoboCompWorldModel::GualzruWorldNode &update, const Ice::Current&)
	{
		return worker->handleUpdate(update);
	}
*/

private:
	Worker *worker;
};

#endif
