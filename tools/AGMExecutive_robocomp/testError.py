#!/usr/bin/env python

import pickle, sys

import AGMExecutive_core

peid = sys.argv[1]

agmData = pickle.load(peid+'agmData.pckl')
domainPath = pickle.load(peid+'domainPath.pckl')
init = pickle.load(peid+'init.pckl')
currentModel = pickle.load(peid+'currentModel.pckl')
plan = pickle.load(peid+'plan.pckl')

ret, stepsFwd, planMonitoring = AGMExecutive_core.AGMExecutiveMonitoring(self.agmData, domainPath, init, self.currentModel, target, AGGLPlannerPlan(self.plan))
