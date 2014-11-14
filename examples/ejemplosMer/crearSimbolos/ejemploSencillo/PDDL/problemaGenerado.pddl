(define (problem problemaGenerado)

	(:domain AGGL )
	(:objects
		A_1
		A_2
		unknown_0
		unknown_1
		unknown_2
		unknown_3
		unknown_4
		unknown_5
		unknown_6
		unknown_7
		unknown_8
		unknown_9
		unknown_10
		unknown_11
	)

	(:init
		(= (total-cost) 0)
		(firstunknown unknown_0)
		(unknownorder unknown_0 unknown_1)
		(unknownorder unknown_1 unknown_2)
		(unknownorder unknown_2 unknown_3)
		(unknownorder unknown_3 unknown_4)
		(unknownorder unknown_4 unknown_5)
		(unknownorder unknown_5 unknown_6)
		(unknownorder unknown_6 unknown_7)
		(unknownorder unknown_7 unknown_8)
		(unknownorder unknown_8 unknown_9)
		(unknownorder unknown_9 unknown_10)
		(unknownorder unknown_10 unknown_11)
		(isA A_1)
		(isA A_2)
	)
	
	(:goal
		(exists ( ?B_1001 ?C_1002 ?D_1003 ?E_1004 ?F_1005 ?B_1006 ?C_1007 ?D_1008 ?E_1009 ?F_1010 )
			(and
				(isA A_1)
				(isB ?B_1001)
				(isC ?C_1002)
				(isD ?D_1003)
				(isE ?E_1004)
				(isF ?F_1005)
				(isA A_2)
				(isB ?B_1006)
				(isC ?C_1007)
				(isD ?D_1008)
				(isE ?E_1009)
				(isF ?F_1010)
				(unido A_1 ?B_1001)
				(unido ?B_1001 ?C_1002)
				(unido ?C_1002 ?D_1003)
				(unido ?D_1003 ?E_1004)
				(unido ?E_1004 ?F_1005)
				(unido ?F_1005 A_1)
				(unido A_2 ?B_1006)
				(unido ?B_1006 ?C_1007)
				(unido ?C_1007 ?D_1008)
				(unido ?D_1008 ?E_1009)
				(unido ?E_1009 ?F_1010)
				(unido ?F_1010 A_2)
			)
		)
	)

	(:metric minimize (total-cost))


)
