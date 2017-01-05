#sudo apt-get install pypy pypy-setuptools
#git clone https://github.com/eleme/thriftpy.git
#cd thriftpy
#make sudo pypy setup.py install

#from thriftpy.protocol.binary import TBinaryProtocolFactory
#from thriftpy.transport.buffered import TBufferedTransportFactory
#from thriftpy.transport.framed import TFramedTransportFactory

import thriftpy
agglplanner_thrift = thriftpy.load("agglplanner.thrift", module_name="agglplanner_thrift")

from thriftpy.rpc import make_client

client = make_client(agglplanner_thrift.AGGLPlanner, '127.0.0.1', 6000)


print 'Get domain id...'
domainText = open('/home/robocomp/robocomp/components/robocomp-shelly/files/planningDomain/domain_min.aggl', 'r').read()
domainId = client.getDomainIdentifier(domainText)
print domainId

print 'Get target id...'
targetText = open('/home/robocomp/robocomp/components/robocomp-shelly/etc/targetReachTableD.aggt', 'r').read()
targetId = client.getTargetIdentifier(targetText)
print targetId

print 'Get target id...'
targetText = open('/home/robocomp/robocomp/components/robocomp-shelly/etc/targetReachTableD.aggt', 'r').read()
targetId = client.getTargetIdentifier(targetText)
print targetId

print 'Reading init world...'
initWorld = open('/home/robocomp/robocomp/components/robocomp-shelly/etcSim/initialModel_hybrid.xml', 'r').read()

print 'Calling planner...'
jobIdentifier = client.startPlanning(domainId, initWorld, targetId, [], [])
print 'got job identifier', jobIdentifier
result = client.getPlanningResults(jobIdentifier)
print result

print 'Calling planner...'
jobIdentifier = client.startPlanning(domainId, initWorld, targetId, [], [])
print 'got job identifier', jobIdentifier
print 'stopping job'
client.forceStopPlanning(jobIdentifier)
result = client.getPlanningResults(jobIdentifier)
print result


print 'Calling planner...'
jobIdentifier = client.startPlanning(domainId, initWorld, targetId, [], [])
print 'got job identifier', jobIdentifier
result = client.getPlanningResults(jobIdentifier)
print result


