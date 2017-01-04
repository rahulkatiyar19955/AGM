#sudo apt-get install pypy pypy-setuptools
#git clone https://github.com/eleme/thriftpy.git
#cd thriftpy
#sudo pypy setup.py install

#from thriftpy.protocol.binary import TBinaryProtocolFactory
#from thriftpy.transport.buffered import TBufferedTransportFactory
#from thriftpy.transport.framed import TFramedTransportFactory

import thriftpy
agglplanner_thrift = thriftpy.load("agglplanner.thrift", module_name="agglplanner_thrift")

from thriftpy.rpc import make_server


import sys, imp, traceback


sys.path.append('/usr/local/share/agm/')
import agglplanner

class Worker(object):
	lastUsedDomainKey = 0
	domainMap = {}
	lastUsedTargetKey = 0
	targetMap = {}
	
	def getDomainIdentifier(self, domainText):
		try:
			ret = self.lastUsedDomainKey + 1
			self.domainMap[ret] = agglplanner.DomainInformation(ret, domainText)
			self.lastUsedDomainKey += 1
			return ret
		except:
			traceback.print_exc()
			return -1

	def getTargetIdentifier(self, targetText):
		try:
			ret = self.lastUsedTargetKey + 1
			self.targetMap[ret] = agglplanner.TargetInformation(ret, targetText)
			self.lastUsedTargetKey += 1
			return ret
		except:
			open("roro", 'w').write(self.targetMap[targetId].code)
			traceback.print_exc()
			return -1

	def planAGGT(self, domainId, initWorld, targetId, excludeList, awakenRules):
		ret = agglplanner_thrift.PlanningResults()
		try:
			dI = self.domainMap[domainId]
			tI = self.targetMap[targetId]
			r = agglplanner.AGGLPlanner(dI.parsed, dI.module, initWorld, tI.module)
			plan = r.run()
			ret.plan = str(plan)
			ret.cost = 1
		except:
			traceback.print_exc()
			raise
		return ret

#PlanResult planHierarchical(1: i32 domainId, 2: string initWorld, 3:i32 targetId, 4: list<string> excludeList, 5: list<string> awakenRules, 6: map<string,string> symbolMapping) throws (1: string theError),

#xmlModelParser.graphFromXML(initPath)
	#def planHierarchical(self, domainIdentifier, initWorld, string target, excludeList, awakenRules, symbolMapping):
		#return PlanResult
	
	

server = make_server(agglplanner_thrift.AGGLPlanner, Worker(), '127.0.0.1', 6000)
server.serve()

