#!/usr/bin/env pypy



#sudo apt-get install pypy pypy-setuptools cython
#git clone https://github.com/eleme/thriftpy.git
#cd thriftpy
#sudo pypy setup.py install
#sudo make clean
#sudo python setup.py install

#from thriftpy.protocol.binary import TBinaryProtocolFactory
#from thriftpy.transport.buffered import TBufferedTransportFactory
#from thriftpy.transport.framed import TFramedTransportFactory

import thriftpy
agglplanner_thrift = thriftpy.load("/usr/local/share/agm/agglplanner.thrift", module_name="agglplanner_thrift")

from thriftpy.rpc import make_server


import sys, imp, traceback, thread


sys.path.append('/usr/local/share/agm/')
import agglplanner


class JobObject(object):
	def __init__(self, identifier, jobInstance):
		self.lock = thread.allocate_lock()
		self.identifier = identifier
		self.jobInstance = jobInstance


class Worker(object):
	mapsLock = thread.allocate_lock()
	lastUsedDomainKey = 0
	domainMap = {}
	lastUsedTargetKey = 0
	targetMap = {}
	lastUsedJobKey = 0
	jobMap = {}
	
	def getDomainIdentifier(self, domainText):
		print '------------------------------------------------------------------------'
		print 'getDomainIdentifier domainText(', type(domainText), ')'
		try:
			self.mapsLock.acquire()
			ret = self.lastUsedDomainKey + 1
			self.domainMap[ret] = agglplanner.DomainInformation(ret, domainText)
			self.lastUsedDomainKey += 1
			return ret
		except:
			traceback.print_exc()
			return -1
		finally:
			self.mapsLock.release()

	def getTargetIdentifier(self, targetText):
		print '------------------------------------------------------------------------'
		print 'getTargetIdentifier targetText(', type(targetText), ')'
		try:
			self.mapsLock.acquire()
			ret = self.lastUsedTargetKey + 1
			self.targetMap[ret] = agglplanner.TargetInformation(ret, targetText)
			open("targetText.txt", 'w').write(targetText)
			open("targetCode.py", 'w').write(self.targetMap[ret].code)
			self.lastUsedTargetKey += 1
			return ret
		except:
			open("roro", 'w').write(self.targetMap[ret].code)
			traceback.print_exc()
			return -1
		finally:
			self.mapsLock.release()

	def startPlanning(self, domainId, initWorld, targetId, excludeList, awakenRules):
		print '------------------------------------------------------------------------'
		print 'startPlanning', domainId, '(', type(domainId), ')', 'initWorld(', type(initWorld), ')', targetId, '(', type(targetId), ')', excludeList, '(', type(excludeList), ')', awakenRules, '(', type(awakenRules), ')'
		try:
			self.mapsLock.acquire()
			ret = self.lastUsedJobKey + 1
			dI = self.domainMap[domainId]
			tI = self.targetMap[targetId]
			planningObject = agglplanner.AGGLPlanner(dI.parsed, dI.module, initWorld, tI.module)
			self.jobMap[ret] = JobObject(ret, planningObject)
			self.lastUsedJobKey += 1
			return ret
		except:
			open("error.txt", 'w').write(self.targetMap[targetId].code)
			traceback.print_exc()
			return -1
		finally:
			self.mapsLock.release()

	def forceStopPlanning(self, jobIdentifier):
		print '------------------------------------------------------------------------'
		print 'forceStopPlanning', jobIdentifier, '(', type(jobIdentifier), ')'
		ret = 0
		try:
			self.mapsLock.acquire()
			job = self.jobMap[jobIdentifier]
			job.jobInstance.setStopFlag()
		except:
			traceback.print_exc()
			return 1
		finally:
			self.mapsLock.release()
		return 0

	def getPlanningResults(self, jobIdentifier):
		print '------------------------------------------------------------------------'
		print 'getPlanningResults', jobIdentifier, '(', type(jobIdentifier), ')'
		ret = agglplanner_thrift.PlanningResults()
		try:
			self.mapsLock.acquire()
			job = self.jobMap[jobIdentifier]
			self.mapsLock.release()
			plan = job.jobInstance.run()
			print plan
			ret.plan = str(plan)
			ret.cost = 1
		except:
			traceback.print_exc()
			raise
		return ret

#PlanResult planHierarchical(1: i32 domainId, 2: string initWorld, 3:i32 targetId, 4: list<string> excludeList, 5: list<string> awakenRules, 6: map<string,string> symbolMapping) throws (1: string theError),


	

server = make_server(agglplanner_thrift.AGGLPlanner, Worker(), '127.0.0.1', 6000)
server.serve()

