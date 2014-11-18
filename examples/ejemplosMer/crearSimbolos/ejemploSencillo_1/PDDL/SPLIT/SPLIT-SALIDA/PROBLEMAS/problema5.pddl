(define (problem problemaGenerado)

	(:domain SPLIT-aggl )
	(:objects
		A_1 - tipo 
		unknown_0 - tipo 
		unknown_1 - tipo 
		unknown_2 - tipo 
		unknown_3 - tipo 
		unknown_4 - tipo 
	)

	(:init
		(firstunknown unknown_0)
		(unknownorder unknown_0 unknown_1)
		(unknownorder unknown_1 unknown_2)
		(unknownorder unknown_2 unknown_3)
		(unknownorder unknown_3 unknown_4)
		(isA A_1)
	)
	
	(:goal
		(exists ( ?A_1001 ?B_1002 ?C_1003 ?D_1004 ?E_1005 ?F_1006 )
			(and
				(isA ?A_1001)
				(isB ?B_1002)
				(isC ?C_1003)
				(isD ?D_1004)
				(isE ?E_1005)
				(isF ?F_1006)
				(unido ?A_1001 ?B_1002)
				(unido ?B_1002 ?C_1003)
				(unido ?C_1003 ?D_1004)
				(unido ?D_1004 ?E_1005)
				(unido ?E_1005 ?F_1006)
				(unido ?F_1006 ?A_1001)
			)
		)
	)



)
