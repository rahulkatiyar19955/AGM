import string
class PlanningCache:
	def __init__(self):
		print 'PlanningCache::init()'
		self.data = dict()
		self.availableId = 0
		try:
			while True:
				D = open('D'+str(self.availableId)+'.py', 'r').read()
				I = open('I'+str(self.availableId)+'.xml', 'r').read()
				G = open('G'+str(self.availableId)+'.py', 'r').read()
				plan = open('plan'+str(self.availableId)+'.agglp', 'r').read()
				cost = float(open('cost'+str(self.availableId)+'.txt', 'r').read())
				ret = True
				if plan=='fail':
					ret = False
				self.include(PlanningContext(ret, D, I, G, plan, cost), False)
				#print 'Read planning context', self.availableId
		except IOError:
			pass
		except:
			traceback.print_exc()
	def include(self, domain, initialstate, goalstate, plan, success, shouldIWrite=True):
		#try:
		if shouldIWrite:
			try:
				#print 'PLAN: ', plan
				D = open('D'+str(self.availableId)+'.py', 'w')
				D.write(domain)
				D.close()
				I = open('I'+str(self.availableId)+'.xml', 'w')
				I.write(initialstate)
				I.close()
				G = open('G'+str(self.availableId)+'.py', 'w')
				G.write(goalstate)
				G.close()
				plan = open('plan'+str(self.availableId)+'.agglp', 'w')
				if success: plan.write(plan)
				else: plan.write('fail')
				plan.close()
			except:
				print 'Can\'t write cache'
				sys.exit(-1)
		self.availableId += 1
		md = md5.new()
		string = string.rstrip(domain, '\n')+'\n'+string.rstrip(initialstate, '\n')+'\n'+string.rstrip(goalstate, '\n')
		md.update(string)
		checksum = md.hexdigest()
		print 'Including planning context with checksum', checksum
		try:
			self.data[checksum].append((domain, initialstate, goalstate, plan, success))
		except:
			self.data[checksum] = []
			self.data[checksum].append((domain, initialstate, goalstate, plan, success))

	def getPlan(self, domain, initialstate, goalstate):
		md = md5.new()
		domain[-1] = string.rstrip(domain, '\n')
		initialstate[-1] = string.rstrip(initialstate, '\n')
		goalstate[-1] = string.rstrip(goalstate, '\n')
		string = domain+'\n'+initialstate+'\n'+goalstate
		md.update(string)
		checksum = md.hexdigest()
		print 'Query cache, checksum', checksum
		if checksum in self.data.keys():
			lis = self.data[checksum]
			print 'Match for the checksum'
			for i in lis:
				if i[0] == domain and i[1] == initialstate and i[2] == goalstate:
					if i[3] == 'fail':
						return False, i[3]
					else:
						print 'GOT PLAN FROM CACHE'
						return True, i[3]
			print 'No exact cache match'
			return None
		else:
			print self.data.keys()
			print 'No cache for the checksum'
			return None

	def getPlanFromFiles(self, domainF, initialstateF, goalstateF):
		domain       = open(domainF,       'r').read()
		initialstate = open(initialstateF, 'r').read()
		goalstate    = open(goalstateF,    'r').read()
		return self.getPlan(domain, initialstate, goalstate)

