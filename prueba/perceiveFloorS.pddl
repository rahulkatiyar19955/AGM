(define (problem works)

	(:domain final)
	(:objects
		s u0 u1 u2 u3 u4 u5 u6 u7 u8 u9 u10
	)

	(:init
		(= (total-cost) 0)
		(firstunknown u0)
		(unknownorder u0 u1)
		(unknownorder u1 u2)
		(unknownorder u2 u3)
		(unknownorder u3 u4)
		(unknownorder u4 u5)
		(unknownorder u5 u6)
		(unknownorder u6 u7)
		(unknownorder u7 u8)
		(unknownorder u8 u9)
		(ISstart s)
	)
	(:metric minimize (total-cost))

	(:goal
		(and
			(ISfloor s)
		)
	)
)


