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

import logging
logging.basicConfig(level=logging.DEBUG)

import thriftpy
agglplanner_thrift = thriftpy.load("/usr/local/share/agm/agglplanner.thrift", module_name="agglplanner_thrift")

from thriftpy.rpc import make_server


import sys, imp, traceback, thread


sys.path.append('/usr/local/share/agm/')
import agglplanner
from agglplanningcache import *

class JobObject(object):
	def __init__(self, identifier, jobInstance, domainId, targetId):
		self.lock = thread.allocate_lock()
		self.identifier = identifier
		self.jobInstance = jobInstance
		self.domainId = domainId
		self.targetId = targetId


class Worker(object):
	mapsLock = thread.allocate_lock()
	lastUsedDomainKey = 0
	domainMap = {}
	lastUsedTargetKey = 0
	targetMap = {}
	lastUsedJobKey = 0
	jobMap = {}
	cache = PlanningCache()

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
			print '------------------------------------------------------------------------'

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
			print '------------------------------------------------------------------------'

	def startPlanning(self, domainId, initWorld, targetId, excludeList, awakenRules):
		print '------------------------------------------------------------------------'
		print 'startPlanning', domainId, '(', type(domainId), ')', 'initWorld(', type(initWorld), ')', targetId, '(', type(targetId), ')', excludeList, '(', type(excludeList), ')', awakenRules, '(', type(awakenRules), ')'
		try:
			self.mapsLock.acquire()
			ret = self.lastUsedJobKey + 1
			dI = self.domainMap[domainId]
			tI = self.targetMap[targetId]
			planningObject = agglplanner.AGGLPlanner(dI.parsed, dI.module, initWorld, tI.module)
			self.jobMap[ret] = JobObject(ret, planningObject, domainId, targetId)
			self.lastUsedJobKey += 1
			return ret
		except:
			open("error.txt", 'w').write(self.targetMap[targetId].code)
			traceback.print_exc()
			return -1
		finally:
			self.mapsLock.release()
			print '------------------------------------------------------------------------'


	def forceStopPlanning(self, jobIdentifier):
		print '------------------------------------------------------------------------'
		print 'forceStopPlanning', jobIdentifier, '(', type(jobIdentifier), ')'
		try:
			self.mapsLock.acquire()
			job = self.jobMap[jobIdentifier]
			job.jobInstance.setStopFlag()
			return 0
		except:
			traceback.print_exc()
			return 1
		finally:
			self.mapsLock.release()
			print '------------------------------------------------------------------------'

	def getPlanningResults(self, jobIdentifier):
		print '------------------------------------------------------------------------'
		print 'getPlanningResults', jobIdentifier, '(', type(jobIdentifier), ')'
		print 'a'
		ret = agglplanner_thrift.PlanningResults()
		print 'b'
		try:
			print 'c'
			self.mapsLock.acquire()
			job = self.jobMap[jobIdentifier]
			dI = self.domainMap[job.domainId]
			tI = self.targetMap[job.targetId]
			print 'd'
		except:
			print 'ERROR AQUI 1'
			traceback.print_exc()
			raise
		finally:
			self.mapsLock.release()
		#
		# First: try with the cache
		#
		try:
			print 'e'
			cacheResult = self.cache.getPlanFromFiles(dI.text, job.jobInstance.initWorld.graph.toXMLString(), tI.code)
			print 'f', cacheResult
			if cacheResult:
				if len(cacheResult[1].strip()) == 0:
					print 'f2'
					cacheResult = False
			print 'g'
		except:
			traceback.print_exc()
			print 'h'
			print 'ERROR AQUI 2'
			cacheResult = False
		try:
			if cacheResult:
				print 'Got plan from cache'
				print '<<<'
				print cacheResult[1]
				print '>>>'
				cacheSuccess = cacheResult[0]
				cachePlan = cacheResult[1]
				# lines = cacheResult[1].split('\n')
				ret.plan = str(cacheResult[1])
				ret.cost = 1
				print 'salimos por cache'
				return ret
		except:
			print 'ERROR AQUI 234534'
		#
		# Second: try planning
		#
		try:
			print 'i'
			plan = job.jobInstance.run()
			print 'j'
			self.cache.includeFromFiles(dI.text, job.jobInstance.initWorld.graph.toXMLString(), tI.code, str(plan), True)
			print 'k'
			ret.plan = str(plan)
			ret.cost = 1
			print 'PLAN:', ret.plan
			return ret
		except:
			print 'ERROR AQUI 3'
			traceback.print_exc()
			print 'ERROR AQUI 3'
			ret.plan = 'errrorr'
			ret.cost = 100
			return ret
		finally:
			print '--------------------------------------------------'
		print 'WE SHOULD NOT GET HERE'
		sys.exit(-1)
#PlanResult planHierarchical(1: i32 domainId, 2: string initWorld, 3:i32 targetId, 4: list<string> excludeList, 5: list<string> awakenRules, 6: map<string,string> symbolMapping) throws (1: string theError),




server = make_server(agglplanner_thrift.AGGLPlanner, Worker(), '127.0.0.1', 6000, client_timeout=1000000)
server.serve()
