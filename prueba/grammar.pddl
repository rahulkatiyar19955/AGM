(define (domain final)

	(:predicates
		(firstunknown ?u)
		(unknownorder ?ua ?ub)

		(ISroom ?n)
		(ISfloor ?n)
		(ISwall ?n)
		(ISobject ?n)
		(ISgravity ?n)
		(ISplane ?n)
		(ISrobot ?n)
		(ISstart ?n)
		(ISmug ?n)
		(ISobstacle ?n)
		(ISnotWall ?n)
		(IStable ?n)

		(link ?u ?v)
		(looks ?u ?v)
		(in ?u ?v)
		(lookTowards ?u ?v)
		(lookPerpendicular ?u ?v)
	)

	(:functions
		(total-cost)
	)

	(:action modelGravity
		:parameters ( ?stackAGMInternal ?stack0 ?stack1 )
		:precondition (and (ISstart ?stack1) (firstunknown ?stack0) (unknownorder ?stack0 ?stackAGMInternal) (not(= ?stackAGMInternal ?stack0)) (not(= ?stackAGMInternal ?stack1)) (not(= ?stack0 ?stack1)) )
		:effect (and (not (firstunknown ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISgravity ?stack1) (ISrobot ?stack0) (not (ISstart ?stack1)) (link ?stack0 ?stack1) (increase (total-cost) 1) )
	)

	(:action lookFloor
		:parameters ( ?g ?gualzru ?stackAGMInternal )
		:precondition (and (ISgravity ?g) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?g ?gualzru)) (not(= ?g ?stackAGMInternal)) (not(= ?gualzru ?stackAGMInternal)) (link ?gualzru ?g) )
		:effect (and (lookTowards ?gualzru ?g) (not (link ?gualzru ?g)) (increase (total-cost) 1) )
	)

	(:action modelHeight
		:parameters ( ?g ?gualzru ?stackAGMInternal )
		:precondition (and (ISgravity ?g) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?g ?gualzru)) (not(= ?g ?stackAGMInternal)) (not(= ?gualzru ?stackAGMInternal)) (lookTowards ?gualzru ?g) )
		:effect (and (not(ISgravity ?g)) (ISplane ?g) (in ?gualzru ?g) (increase (total-cost) 1) )
	)

	(:action lookPerpendicularFloor
		:parameters ( ?gualzru ?floor ?stackAGMInternal )
		:precondition (and (ISplane ?floor) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?gualzru ?floor)) (not(= ?gualzru ?stackAGMInternal)) (not(= ?floor ?stackAGMInternal)) (lookTowards ?gualzru ?floor) )
		:effect (and (lookPerpendicular ?gualzru ?floor) (not (lookTowards ?gualzru ?floor)) (increase (total-cost) 1) )
	)

	(:action modelYaw
		:parameters ( ?gualzru ?floor ?stackAGMInternal )
		:precondition (and (ISplane ?floor) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?gualzru ?floor)) (not(= ?gualzru ?stackAGMInternal)) (not(= ?floor ?stackAGMInternal)) (lookPerpendicular ?gualzru ?floor) )
		:effect (and (not(ISplane ?floor)) (ISfloor ?floor) (increase (total-cost) 1) )
	)

	(:action lookFirstWall
		:parameters ( ?gualzru ?floor ?stackAGMInternal ?stack0 ?stack1 ?stack2 ?stack3 )
		:precondition (and (ISfloor ?floor) (ISrobot ?gualzru) (firstunknown ?stack3) (unknownorder ?stack3 ?stack2) (unknownorder ?stack2 ?stack1) (unknownorder ?stack1 ?stack0) (unknownorder ?stack0 ?stackAGMInternal) (not(= ?gualzru ?floor)) (not(= ?gualzru ?stackAGMInternal)) (not(= ?gualzru ?stack0)) (not(= ?gualzru ?stack1)) (not(= ?gualzru ?stack2)) (not(= ?gualzru ?stack3)) (not(= ?floor ?stackAGMInternal)) (not(= ?floor ?stack0)) (not(= ?floor ?stack1)) (not(= ?floor ?stack2)) (not(= ?floor ?stack3)) (not(= ?stackAGMInternal ?stack0)) (not(= ?stackAGMInternal ?stack1)) (not(= ?stackAGMInternal ?stack2)) (not(= ?stackAGMInternal ?stack3)) (not(= ?stack0 ?stack1)) (not(= ?stack0 ?stack2)) (not(= ?stack0 ?stack3)) (not(= ?stack1 ?stack2)) (not(= ?stack1 ?stack3)) (not(= ?stack2 ?stack3)) (lookPerpendicular ?gualzru ?floor) )
		:effect (and (not (firstunknown ?stack3)) (not (unknownorder ?stack3 ?stack2)) (not (unknownorder ?stack2 ?stack1)) (not (unknownorder ?stack1 ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISnotWall ?stack3) (ISnotWall ?stack2) (ISnotWall ?stack1) (ISnotWall ?stack0) (link ?stack0 ?stack1) (link ?stack1 ?stack2) (looks ?gualzru ?stack0) (link ?stack2 ?stack3) (link ?floor ?stack0) (not (lookPerpendicular ?gualzru ?floor)) (increase (total-cost) 1) )
	)

	(:action lookNextWall
		:parameters ( ?w2 ?w1 ?gualzru ?stackAGMInternal )
		:precondition (and (ISnotWall ?w2) (ISwall ?w1) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?w2 ?w1)) (not(= ?w2 ?gualzru)) (not(= ?w2 ?stackAGMInternal)) (not(= ?w1 ?gualzru)) (not(= ?w1 ?stackAGMInternal)) (not(= ?gualzru ?stackAGMInternal)) (looks ?gualzru ?w1) (link ?w1 ?w2) )
		:effect (and (looks ?gualzru ?w2) (not (looks ?gualzru ?w1)) (increase (total-cost) 1) )
	)

	(:action modelWall
		:parameters ( ?w2 ?w1 ?gualzru ?stackAGMInternal )
		:precondition (and (ISnotWall ?w2) (ISnotWall ?w1) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?w2 ?w1)) (not(= ?w2 ?gualzru)) (not(= ?w2 ?stackAGMInternal)) (not(= ?w1 ?gualzru)) (not(= ?w1 ?stackAGMInternal)) (not(= ?gualzru ?stackAGMInternal)) (looks ?gualzru ?w1) (link ?w1 ?w2) )
		:effect (and (not(ISnotWall ?w1)) (ISwall ?w1) (increase (total-cost) 1) )
	)

	(:action modelLastWall
		:parameters ( ?floor ?robot ?w4 ?w3 ?w2 ?w1 ?stackAGMInternal )
		:precondition (and (ISfloor ?floor) (ISrobot ?robot) (ISnotWall ?w4) (ISwall ?w3) (ISwall ?w2) (ISwall ?w1) (firstunknown ?stackAGMInternal) (not(= ?floor ?robot)) (not(= ?floor ?w4)) (not(= ?floor ?w3)) (not(= ?floor ?w2)) (not(= ?floor ?w1)) (not(= ?floor ?stackAGMInternal)) (not(= ?robot ?w4)) (not(= ?robot ?w3)) (not(= ?robot ?w2)) (not(= ?robot ?w1)) (not(= ?robot ?stackAGMInternal)) (not(= ?w4 ?w3)) (not(= ?w4 ?w2)) (not(= ?w4 ?w1)) (not(= ?w4 ?stackAGMInternal)) (not(= ?w3 ?w2)) (not(= ?w3 ?w1)) (not(= ?w3 ?stackAGMInternal)) (not(= ?w2 ?w1)) (not(= ?w2 ?stackAGMInternal)) (not(= ?w1 ?stackAGMInternal)) (looks ?robot ?w4) (link ?floor ?w1) (link ?w1 ?w2) (link ?w2 ?w3) (link ?w3 ?w4) )
		:effect (and (not(ISfloor ?floor)) (ISroom ?floor) (not(ISnotWall ?w4)) (ISwall ?w4) (increase (total-cost) 1) )
	)

	(:action detectObstacle
		:parameters ( ?room ?gualzru ?stackAGMInternal ?stack0 )
		:precondition (and (ISroom ?room) (ISrobot ?gualzru) (firstunknown ?stack0) (unknownorder ?stack0 ?stackAGMInternal) (not(= ?room ?gualzru)) (not(= ?room ?stackAGMInternal)) (not(= ?room ?stack0)) (not(= ?gualzru ?stackAGMInternal)) (not(= ?gualzru ?stack0)) (not(= ?stackAGMInternal ?stack0)) (in ?gualzru ?room) )
		:effect (and (not (firstunknown ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISobstacle ?stack0) (in ?stack0 ?room) (increase (total-cost) 1) )
	)

	(:action modelTable
		:parameters ( ?obstacle ?room ?gualzru ?stackAGMInternal )
		:precondition (and (ISobstacle ?obstacle) (ISroom ?room) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?obstacle ?room)) (not(= ?obstacle ?gualzru)) (not(= ?obstacle ?stackAGMInternal)) (not(= ?room ?gualzru)) (not(= ?room ?stackAGMInternal)) (not(= ?gualzru ?stackAGMInternal)) (in ?gualzru ?room) (in ?obstacle ?room) )
		:effect (and (not(ISobstacle ?obstacle)) (IStable ?obstacle) (increase (total-cost) 1) )
	)

	(:action detectObjectInTable
		:parameters ( ?table ?room ?gualzru ?stackAGMInternal ?stack0 )
		:precondition (and (IStable ?table) (ISroom ?room) (ISrobot ?gualzru) (firstunknown ?stack0) (unknownorder ?stack0 ?stackAGMInternal) (not(= ?table ?room)) (not(= ?table ?gualzru)) (not(= ?table ?stackAGMInternal)) (not(= ?table ?stack0)) (not(= ?room ?gualzru)) (not(= ?room ?stackAGMInternal)) (not(= ?room ?stack0)) (not(= ?gualzru ?stackAGMInternal)) (not(= ?gualzru ?stack0)) (not(= ?stackAGMInternal ?stack0)) (in ?gualzru ?room) (in ?table ?room) )
		:effect (and (not (firstunknown ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISobject ?stack0) (in ?stack0 ?table) (increase (total-cost) 1) )
	)

	(:action modelMugInTable
		:parameters ( ?table ?object ?room ?gualzru ?stackAGMInternal )
		:precondition (and (IStable ?table) (ISobject ?object) (ISroom ?room) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?table ?object)) (not(= ?table ?room)) (not(= ?table ?gualzru)) (not(= ?table ?stackAGMInternal)) (not(= ?object ?room)) (not(= ?object ?gualzru)) (not(= ?object ?stackAGMInternal)) (not(= ?room ?gualzru)) (not(= ?room ?stackAGMInternal)) (not(= ?gualzru ?stackAGMInternal)) (in ?gualzru ?room) (in ?table ?room) (in ?object ?table) )
		:effect (and (not(ISobject ?object)) (ISmug ?object) (increase (total-cost) 1) )
	)

)
