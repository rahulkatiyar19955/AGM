(define (problem problemaGenerado)

	(:domain AGGL )
	(:objects
		A_1
		unknown_0
		unknown_1
		unknown_2
		unknown_3
	)

	(:init
		(= (total-cost) 0)
		(firstunknown unknown_0)
		(unknownorder unknown_0 unknown_1)
		(unknownorder unknown_1 unknown_2)
		(unknownorder unknown_2 unknown_3)
		(ISA A_1)
	)
	
	(:goal
		(exists ( ?A_1001 ?B_1002 ?C_1003 ?D_1004 ?E_1005 )
			(and
				(ISA ?A_1001)
				(ISB ?B_1002)
				(ISC ?C_1003)
				(ISD ?D_1004)
				(ISE ?E_1005)
				(unido ?A_1001 ?B_1002)
				(unido ?B_1002 ?C_1003)
				(unido ?C_1003 ?D_1004)
				(unido ?D_1004 ?E_1005)
				(unido ?E_1005 ?A_1001)
			)
		)
	)

	(:metric minimize (total-cost))
)
