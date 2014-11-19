(define (domain AGGL)

	(:requirements :strips :typing )
	(:types tipo)
	(:predicates
		(firstunknown ?u - tipo)
		(unknownorder ?ua ?ub - tipo)

		(isA ?n - tipo)
		(isC ?n - tipo)
		(isB ?n - tipo)
		(isE ?n - tipo)
		(isD ?n - tipo)
		(isF ?n - tipo)

		(unido ?u ?v - tipo)
	)

	(:action recta
		:parameters ( ?va ?vListAGMInternal ?vlist0 - tipo )
		:precondition (and (isA ?va) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isB ?vlist0) (unido ?va ?vlist0)
		)
	)

	(:action triangulo
		:parameters ( ?va ?vb ?vListAGMInternal ?vlist0 - tipo )
		:precondition (and (isA ?va) (isB ?vb) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isC ?vlist0) (unido ?vb ?vlist0) (unido ?vlist0 ?va)
		)
	)

	(:action cuadrado
		:parameters ( ?va ?vc ?vb ?vListAGMInternal ?vlist0 - tipo )
		:precondition (and (isA ?va) (isC ?vc) (isB ?vb) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) (unido ?vb ?vc) (unido ?vc ?va) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isD ?vlist0) (unido ?vc ?vlist0) (unido ?vlist0 ?va) (not (unido ?vc ?va))
		)
	)

	(:action pentagono
		:parameters ( ?va ?vc ?vb ?vd ?vListAGMInternal ?vlist0 - tipo )
		:precondition (and (isA ?va) (isC ?vc) (isB ?vb) (isD ?vd) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) (unido ?vb ?vc) (unido ?vc ?vd) (unido ?vd ?va) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isE ?vlist0) (unido ?vd ?vlist0) (unido ?vlist0 ?va) (not (unido ?vd ?va))
		)
	)

	(:action hexagono
		:parameters ( ?va ?vc ?vb ?ve ?vd ?vListAGMInternal ?vlist0 - tipo )
		:precondition (and (isA ?va) (isC ?vc) (isB ?vb) (isE ?ve) (isD ?vd) (firstunknown ?vlist0) (unknownorder ?vlist0 ?vListAGMInternal) (not(= ?vListAGMInternal ?vlist0)) (unido ?va ?vb) (unido ?vb ?vc) (unido ?vc ?vd) (unido ?vd ?ve) (unido ?ve ?va) )
		:effect (and (not (firstunknown ?vlist0)) (not (unknownorder ?vlist0 ?vListAGMInternal)) (firstunknown ?vListAGMInternal) (isF ?vlist0) (unido ?ve ?vlist0) (unido ?vlist0 ?va) (not (unido ?ve ?va))
		)
	)

)
