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

class Dispatcher(object):
	lastUsedDomainKey = 0
	domainMap = {}
	
	
	def getDomainIdentifier(self, domainText):
		lastUsedDomainKey += 1
		print 'got', domainText
		print 'assign', lastUsedDomainKey
		return lastUsedDomainKey

	def planAGGT(self, domainIdentifier, initWorld, target, excludeList, awakenRules:
		return PlanResult

	def planHierarchical(self, domainIdentifier, initWorld, string target, excludeList, awakenRules, symbolMapping):
		return PlanResult
	
	

server = make_server(agglplanner_thrift.AGGLPlanner, Dispatcher(), '127.0.0.1', 6000)
server.serve()

