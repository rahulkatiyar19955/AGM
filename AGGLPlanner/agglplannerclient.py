#sudo apt-get install pypy pypy-setuptools
#git clone https://github.com/eleme/thriftpy.git
#cd thriftpy
#sudo pypy setup.py install

#from thriftpy.protocol.binary import TBinaryProtocolFactory
#from thriftpy.transport.buffered import TBufferedTransportFactory
#from thriftpy.transport.framed import TFramedTransportFactory

import thriftpy
agglplanner_thrift = thriftpy.load("agglplanner.thrift", module_name="agglplanner_thrift")

from thriftpy.rpc import make_client

client = make_client(agglplanner_thrift.AGGLPlanner, '127.0.0.1', 6000)
print client.getDomainIdentifier('kdkodkeod edke ode')

