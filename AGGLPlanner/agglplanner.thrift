struct PlanResult
{
	1: i32 cost,
	2: string plan,
}

service AGGLPlanner
{
	i32 getDomainIdentifier(1:string domainText),
	PlanResult planAGGT(        1: i32 domainIdentifier, 2: string initWorld, 3: string target, 4: list<string> excludeList, 5: list<string> awakenRules                                     ) throws (1: string theError),
	PlanResult planHierarchical(1: i32 domainIdentifier, 2: string initWorld, 3: string target, 4: list<string> excludeList, 5: list<string> awakenRules, 6: map<string,string> symbolMapping) throws (1: string theError),
}
