(define (domain AGGL)

	(:predicates
		(firstunknown ?u)
		(unknownorder ?ua ?ub)

		(isA ?n)
		(isC ?n)
		(isB ?n)
		(isE ?n)
		(isD ?n)
		(isF ?n)

		(unido ?u ?v)
	)

	(:functions
		(total-cost)
	)

	(:action recta
		:parameters ( ?va ?vListAGMInternal ?vlist0 )
		:precondition (and (isA ?va) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isB ?vlist0) (unido ?va ?vlist0) (increase (total-cost) 1)
		)
	)

	(:action triangulo
		:parameters ( ?va ?vb ?vListAGMInternal ?vlist0 )
		:precondition (and (isA ?va) (isB ?vb) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isC ?vlist0) (unido ?vb ?vlist0) (unido ?vlist0 ?va) (increase (total-cost) 1)
		)
	)

	(:action cuadrado
		:parameters ( ?va ?vc ?vb ?vListAGMInternal ?vlist0 )
		:precondition (and (isA ?va) (isC ?vc) (isB ?vb) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) (unido ?vb ?vc) (unido ?vc ?va) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isD ?vlist0) (unido ?vc ?vlist0) (unido ?vlist0 ?va) (not (unido ?vc ?va)) (increase (total-cost) 1)
		)
	)

	(:action pentagono
		:parameters ( ?va ?vc ?vb ?vd ?vListAGMInternal ?vlist0 )
		:precondition (and (isA ?va) (isC ?vc) (isB ?vb) (isD ?vd) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) (unido ?vb ?vc) (unido ?vc ?vd) (unido ?vd ?va) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isE ?vlist0) (unido ?vd ?vlist0) (unido ?vlist0 ?va) (not (unido ?vd ?va)) (increase (total-cost) 1)
		)
	)

	(:action hexagono
		:parameters ( ?va ?vc ?vb ?ve ?vd ?vListAGMInternal ?vlist0 )
		:precondition (and (isA ?va) (isC ?vc) (isB ?vb) (isE ?ve) (isD ?vd) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) (unido ?vb ?vc) (unido ?vc ?vd) (unido ?vd ?ve) (unido ?ve ?va) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isF ?vlist0) (unido ?ve ?vlist0) (unido ?vlist0 ?va) (not (unido ?ve ?va)) (increase (total-cost) 1)
		)
	)

)
