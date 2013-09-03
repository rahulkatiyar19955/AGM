(define (domain )

	(:predicates
		(firstunknown ?u)
		(unknownorder ?ua ?ub)

		(ISlocked ?n)
		(ISroom ?n)
		(ISfloor ?n)
		(ISwall ?n)
		(ISunlocked ?n)
		(ISobstacle ?n)
		(ISgravity ?n)
		(ISrobot ?n)
		(ISstart ?n)
		(ISplane ?n)
		(ISnotWall ?n)
		(ISview ?n)

		(observed ?u ?v)
		(lookTowards ?u ?v)
		(is ?u ?v)
		(lookPerpendicular ?u ?v)
		(uncovered ?u ?v)
		(link ?u ?v)
		(looks ?u ?v)
		(in ?u ?v)
		(covered ?u ?v)
		(has ?u ?v)
	)

	(:functions
		(total-cost)
	)

	(:action modelGravity
		:parameters ( ?stackAGMInternal ?stack0 ?stack1 )
		:precondition (and (ISstart ?stack1) (firstunknown ?stack0) (unknownorder ?stack0 ?stackAGMInternal) )
		:effect (and (not (firstunknown ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISgravity ?stack1) (ISrobot ?stack0) (not (ISstart ?stack1)) (link ?stack0 ?stack1) (increase (total-cost) 1) )
	)

	(:action lookFloor
		:parameters ( ?g ?gualzru ?stackAGMInternal )
		:precondition (and (ISgravity ?g) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?g ?gualzru)) (link ?gualzru ?g) )
		:effect (and (lookTowards ?gualzru ?g) (not (link ?gualzru ?g)) (increase (total-cost) 1) )
	)

	(:action modelHeight
		:parameters ( ?g ?gualzru ?stackAGMInternal )
		:precondition (and (ISgravity ?g) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?g ?gualzru)) (lookTowards ?gualzru ?g) )
		:effect (and (not(ISgravity ?g)) (ISplane ?g) (in ?gualzru ?g) (increase (total-cost) 1) )
	)

	(:action lookPerpendicularFloor
		:parameters ( ?floor ?gualzru ?stackAGMInternal )
		:precondition (and (ISrobot ?gualzru) (ISplane ?floor) (firstunknown ?stackAGMInternal) (not(= ?floor ?gualzru)) (lookTowards ?gualzru ?floor) )
		:effect (and (lookPerpendicular ?gualzru ?floor) (not (lookTowards ?gualzru ?floor)) (increase (total-cost) 1) )
	)

	(:action modelYaw
		:parameters ( ?floor ?gualzru ?stackAGMInternal )
		:precondition (and (ISrobot ?gualzru) (ISplane ?floor) (firstunknown ?stackAGMInternal) (not(= ?floor ?gualzru)) (lookPerpendicular ?gualzru ?floor) )
		:effect (and (not(ISplane ?floor)) (ISfloor ?floor) (increase (total-cost) 1) )
	)

	(:action lookFirstWall
		:parameters ( ?floor ?gualzru ?stackAGMInternal ?stack0 ?stack1 ?stack2 ?stack3 )
		:precondition (and (ISrobot ?gualzru) (ISfloor ?floor) (firstunknown ?stack3) (unknownorder ?stack3 ?stack2) (unknownorder ?stack2 ?stack1) (unknownorder ?stack1 ?stack0) (unknownorder ?stack0 ?stackAGMInternal) (not(= ?floor ?gualzru)) (lookPerpendicular ?gualzru ?floor) )
		:effect (and (not (firstunknown ?stack3)) (not (unknownorder ?stack3 ?stack2)) (not (unknownorder ?stack2 ?stack1)) (not (unknownorder ?stack1 ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISnotWall ?stack3) (ISnotWall ?stack2) (ISnotWall ?stack1) (ISnotWall ?stack0) (link ?stack0 ?stack1) (link ?stack1 ?stack2) (looks ?gualzru ?stack0) (link ?stack2 ?stack3) (link ?floor ?stack0) (not (lookPerpendicular ?gualzru ?floor)) (increase (total-cost) 1) )
	)

	(:action lookNextWall
		:parameters ( ?w2 ?w1 ?gualzru ?stackAGMInternal )
		:precondition (and (ISnotWall ?w2) (ISwall ?w1) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?w2 ?w1)) (not(= ?w2 ?gualzru)) (not(= ?w1 ?gualzru)) (looks ?gualzru ?w1) (link ?w1 ?w2) )
		:effect (and (looks ?gualzru ?w2) (not (looks ?gualzru ?w1)) (increase (total-cost) 1) )
	)

	(:action modelWall
		:parameters ( ?w2 ?w1 ?gualzru ?stackAGMInternal )
		:precondition (and (ISnotWall ?w2) (ISnotWall ?w1) (ISrobot ?gualzru) (firstunknown ?stackAGMInternal) (not(= ?w2 ?w1)) (not(= ?w2 ?gualzru)) (not(= ?w1 ?gualzru)) (looks ?gualzru ?w1) (link ?w1 ?w2) )
		:effect (and (not(ISnotWall ?w1)) (ISwall ?w1) (increase (total-cost) 1) )
	)

	(:action modelLastWall
		:parameters ( ?floor ?robot ?w4 ?w3 ?w2 ?w1 ?stackAGMInternal ?stack0 ?stack1 )
		:precondition (and (ISfloor ?floor) (ISrobot ?robot) (ISnotWall ?w4) (ISwall ?w3) (ISwall ?w2) (ISwall ?w1) (firstunknown ?stack1) (unknownorder ?stack1 ?stack0) (unknownorder ?stack0 ?stackAGMInternal) (not(= ?floor ?robot)) (not(= ?floor ?w4)) (not(= ?floor ?w3)) (not(= ?floor ?w2)) (not(= ?floor ?w1)) (not(= ?robot ?w4)) (not(= ?robot ?w3)) (not(= ?robot ?w2)) (not(= ?robot ?w1)) (not(= ?w4 ?w3)) (not(= ?w4 ?w2)) (not(= ?w4 ?w1)) (not(= ?w3 ?w2)) (not(= ?w3 ?w1)) (not(= ?w2 ?w1)) (looks ?robot ?w4) (link ?floor ?w1) (link ?w1 ?w2) (link ?w2 ?w3) (link ?w3 ?w4) )
		:effect (and (not(ISfloor ?floor)) (ISroom ?floor) (not(ISnotWall ?w4)) (ISwall ?w4) (not (firstunknown ?stack1)) (not (unknownorder ?stack1 ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISunlocked ?stack1) (ISview ?stack0) (uncovered ?stack0 ?floor) (is ?robot ?stack1) (has ?robot ?stack0) (not (looks ?robot ?w4)) (increase (total-cost) 1) )
	)

	(:action lockRobot
		:parameters ( ?lock ?robot ?stackAGMInternal )
		:precondition (and (ISunlocked ?lock) (ISrobot ?robot) (firstunknown ?stackAGMInternal) (not(= ?lock ?robot)) (is ?robot ?lock) )
		:effect (and (not(ISunlocked ?lock)) (ISlocked ?lock) (increase (total-cost) 1) )
	)

	(:action addObstacle
		:parameters ( ?lock ?robot ?room ?view ?stackAGMInternal ?stack0 )
		:precondition (and (ISlocked ?lock) (ISview ?view) (ISrobot ?robot) (ISroom ?room) (firstunknown ?stack0) (unknownorder ?stack0 ?stackAGMInternal) (not(= ?lock ?robot)) (not(= ?lock ?room)) (not(= ?lock ?view)) (not(= ?robot ?room)) (not(= ?robot ?view)) (not(= ?room ?view)) (is ?robot ?lock) (has ?robot ?view) (in ?robot ?room) (uncovered ?view ?room) )
		:effect (and (not (firstunknown ?stack0)) (not (unknownorder ?stack0 ?stackAGMInternal)) (firstunknown ?stackAGMInternal) (ISobstacle ?stack0) (in ?stack0 ?room) (increase (total-cost) 1) )
	)

	(:action markViewCovered
		:parameters ( ?lock ?robot ?room ?view ?stackAGMInternal )
		:precondition (and (ISlocked ?lock) (ISview ?view) (ISrobot ?robot) (ISroom ?room) (firstunknown ?stackAGMInternal) (not(= ?lock ?robot)) (not(= ?lock ?room)) (not(= ?lock ?view)) (not(= ?robot ?room)) (not(= ?robot ?view)) (not(= ?room ?view)) (is ?robot ?lock) (has ?robot ?view) (in ?robot ?room) (uncovered ?view ?room) )
		:effect (and (not(ISlocked ?lock)) (ISunlocked ?lock) (covered ?view ?room) (not (uncovered ?view ?room)) (increase (total-cost) 1) )
	)

	(:action saccadeFinishesInspectionMovement
		:parameters ( ?lock ?robot ?room ?view ?stackAGMInternal )
		:precondition (and (ISlocked ?lock) (ISview ?view) (ISrobot ?robot) (ISroom ?room) (firstunknown ?stackAGMInternal) (not(= ?lock ?robot)) (not(= ?lock ?room)) (not(= ?lock ?view)) (not(= ?robot ?room)) (not(= ?robot ?view)) (not(= ?room ?view)) (is ?robot ?lock) (in ?robot ?room) (has ?robot ?view) (covered ?view ?room) )
		:effect (and (not(ISlocked ?lock)) (ISunlocked ?lock) (uncovered ?view ?room) (not (covered ?view ?room)) (increase (total-cost) 1) )
	)

	(:action markRoomObserved
		:parameters ( ?lock ?robot ?room ?view ?stackAGMInternal )
		:precondition (and (ISlocked ?lock) (ISview ?view) (ISrobot ?robot) (ISroom ?room) (firstunknown ?stackAGMInternal) (not(= ?lock ?robot)) (not(= ?lock ?room)) (not(= ?lock ?view)) (not(= ?robot ?room)) (not(= ?robot ?view)) (not(= ?room ?view)) (is ?robot ?lock) (has ?robot ?view) (in ?robot ?room) (uncovered ?view ?room) )
		:effect (and (covered ?view ?room) (not (uncovered ?view ?room)) (increase (total-cost) 1) )
	)

	(:action boringRoom
		:parameters ( ?lock ?robot ?room ?view ?stackAGMInternal )
		:precondition (and (ISlocked ?lock) (ISview ?view) (ISrobot ?robot) (ISroom ?room) (firstunknown ?stackAGMInternal) (not(= ?lock ?robot)) (not(= ?lock ?room)) (not(= ?lock ?view)) (not(= ?robot ?room)) (not(= ?robot ?view)) (not(= ?room ?view)) (is ?robot ?lock) (in ?robot ?room) (has ?robot ?view) (covered ?view ?room) )
		:effect (and (not(ISlocked ?lock)) (ISunlocked ?lock) (observed ?robot ?room) (uncovered ?view ?room) (not (covered ?view ?room)) (increase (total-cost) 1) )
	)

)
