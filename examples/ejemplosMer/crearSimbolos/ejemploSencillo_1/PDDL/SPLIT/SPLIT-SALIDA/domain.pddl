(define (domain SPLIT-aggl)
(:types tipo )

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
	(proc_none)
	(do_recta_2)
	(Arg_vlist0_tipo ?vlist0 - tipo)
	(do_triangulo_2)
	(do_triangulo_3)
	(do_triangulo_4)
	(Arg_va_tipo ?va - tipo)
	(Arg_vb_tipo ?vb - tipo)
	(do_cuadrado_2)
	(do_cuadrado_3)
	(Arg_vc_tipo ?vc - tipo)
	(do_pentagono_2)
	(do_pentagono_3)
	(do_pentagono_4)
	(do_pentagono_5)
	(Arg_vd_tipo ?vd - tipo)
	(do_hexagono_2)
	(do_hexagono_3)
	(do_hexagono_4)
	(do_hexagono_5)
	(Arg_ve_tipo ?ve - tipo)
)

(:action recta_1
	:parameters(
		?va - tipo
		?vlist0 - tipo
	)
	:precondition
		(and
		(isA ?va)
		(firstunknown ?vlist0)
		(proc_none)
		)
	:effect
		(and
		(unido ?va ?vlist0)
		(do_recta_2)
		(Arg_vlist0_tipo ?vlist0)
		(not(proc_none))
		)
)


(:action recta_2
	:parameters(
		?vlistagminternal - tipo
		?vlist0 - tipo
	)
	:precondition
		(and
		(unknownorder ?vlist0 ?vlistagminternal)
		(= ?vlistagminternal ?vlist0)
		(do_recta_2)
		(Arg_vlist0_tipo ?vlist0)
		)
	:effect
		(and
		(firstunknown ?vlistagminternal)
		(isB ?vlist0)
		(proc_none)
		(not(firstunknown ?vlist0))
		(not(unknownorder ?vlist0 ?vlistagminternal))
		(not(do_recta_2))
		(not(Arg_vlist0_tipo ?vlist0))
		)
)


(:action triangulo_1
	:parameters(
		?va - tipo
		?vb - tipo
	)
	:precondition
		(and
		(unido ?va ?vb)
		(proc_none)
		)
	:effect
		(and
		(do_triangulo_2)
		(Arg_va_tipo ?va)
		(Arg_vb_tipo ?vb)
		(not(proc_none))
		)
)


(:action triangulo_2
	:parameters(
		?va - tipo
		?vlist0 - tipo
	)
	:precondition
		(and
		(isA ?va)
		(firstunknown ?vlist0)
		(do_triangulo_2)
		(Arg_va_tipo ?va)
		)
	:effect
		(and
		(unido ?vlist0 ?va)
		(do_triangulo_3)
		(Arg_vlist0_tipo ?vlist0)
		(not(do_triangulo_2))
		(not(Arg_va_tipo ?va))
		)
)


(:action triangulo_3
	:parameters(
		?vb - tipo
		?vlist0 - tipo
	)
	:precondition
		(and
		(isB ?vb)
		(do_triangulo_3)
		(Arg_vb_tipo ?vb)
		(Arg_vlist0_tipo ?vlist0)
		)
	:effect
		(and
		(isC ?vlist0)
		(unido ?vb ?vlist0)
		(do_triangulo_4)
		(not(do_triangulo_3))
		(not(Arg_vb_tipo ?vb))
		)
)


(:action triangulo_4
	:parameters(
		?vlistagminternal - tipo
		?vlist0 - tipo
	)
	:precondition
		(and
		(unknownorder ?vlist0 ?vlistagminternal)
		(= ?vlistagminternal ?vlist0)
		(do_triangulo_4)
		(Arg_vlist0_tipo ?vlist0)
		)
	:effect
		(and
		(firstunknown ?vlistagminternal)
		(proc_none)
		(not(firstunknown ?vlist0))
		(not(unknownorder ?vlist0 ?vlistagminternal))
		(not(do_triangulo_4))
		(not(Arg_vlist0_tipo ?vlist0))
		)
)


(:action cuadrado_1
	:parameters(
		?vb - tipo
		?vc - tipo
		?va - tipo
	)
	:precondition
		(and
		(unido ?vb ?vc)
		(unido ?vc ?va)
		(isA ?va)
		(isC ?vc)
		(unido ?va ?vb)
		(proc_none)
		)
	:effect
		(and
		(do_cuadrado_2)
		(Arg_vb_tipo ?vb)
		(Arg_vc_tipo ?vc)
		(Arg_va_tipo ?va)
		(not(proc_none))
		)
)


(:action cuadrado_2
	:parameters(
		?vlistagminternal - tipo
		?vlist0 - tipo
		?vb - tipo
	)
	:precondition
		(and
		(unknownorder ?vlist0 ?vlistagminternal)
		(= ?vlistagminternal ?vlist0)
		(isB ?vb)
		(firstunknown ?vlist0)
		(do_cuadrado_2)
		(Arg_vb_tipo ?vb)
		)
	:effect
		(and
		(firstunknown ?vlistagminternal)
		(isD ?vlist0)
		(do_cuadrado_3)
		(Arg_vlist0_tipo ?vlist0)
		(not(firstunknown ?vlist0))
		(not(unknownorder ?vlist0 ?vlistagminternal))
		(not(do_cuadrado_2))
		(not(Arg_vb_tipo ?vb))
		)
)


(:action cuadrado_3
	:parameters(
		?vc - tipo
		?vlist0 - tipo
		?va - tipo
	)
	:precondition
		(and
		(do_cuadrado_3)
		(Arg_vc_tipo ?vc)
		(Arg_vlist0_tipo ?vlist0)
		(Arg_va_tipo ?va)
		)
	:effect
		(and
		(unido ?vc ?vlist0)
		(unido ?vlist0 ?va)
		(proc_none)
		(not(unido ?vc ?va))
		(not(do_cuadrado_3))
		(not(Arg_vc_tipo ?vc))
		(not(Arg_vlist0_tipo ?vlist0))
		(not(Arg_va_tipo ?va))
		)
)


(:action pentagono_1
	:parameters(
		?vc - tipo
		?vd - tipo
		?va - tipo
	)
	:precondition
		(and
		(unido ?vc ?vd)
		(unido ?vd ?va)
		(proc_none)
		)
	:effect
		(and
		(do_pentagono_2)
		(Arg_vc_tipo ?vc)
		(Arg_vd_tipo ?vd)
		(Arg_va_tipo ?va)
		(not(proc_none))
		)
)


(:action pentagono_2
	:parameters(
		?va - tipo
		?vc - tipo
		?vb - tipo
	)
	:precondition
		(and
		(isA ?va)
		(isC ?vc)
		(unido ?vb ?vc)
		(do_pentagono_2)
		(Arg_va_tipo ?va)
		(Arg_vc_tipo ?vc)
		)
	:effect
		(and
		(do_pentagono_3)
		(Arg_vb_tipo ?vb)
		(not(do_pentagono_2))
		(not(Arg_vc_tipo ?vc))
		)
)


(:action pentagono_3
	:parameters(
		?vb - tipo
		?vlist0 - tipo
		?va - tipo
	)
	:precondition
		(and
		(isB ?vb)
		(firstunknown ?vlist0)
		(unido ?va ?vb)
		(do_pentagono_3)
		(Arg_vb_tipo ?vb)
		(Arg_va_tipo ?va)
		)
	:effect
		(and
		(do_pentagono_4)
		(Arg_vlist0_tipo ?vlist0)
		(not(do_pentagono_3))
		(not(Arg_vb_tipo ?vb))
		)
)


(:action pentagono_4
	:parameters(
		?vd - tipo
		?vlist0 - tipo
		?va - tipo
	)
	:precondition
		(and
		(do_pentagono_4)
		(Arg_vd_tipo ?vd)
		(Arg_vlist0_tipo ?vlist0)
		(Arg_va_tipo ?va)
		)
	:effect
		(and
		(unido ?vd ?vlist0)
		(unido ?vlist0 ?va)
		(do_pentagono_5)
		(not(unido ?vd ?va))
		(not(do_pentagono_4))
		(not(Arg_va_tipo ?va))
		)
)


(:action pentagono_5
	:parameters(
		?vlistagminternal - tipo
		?vlist0 - tipo
		?vd - tipo
	)
	:precondition
		(and
		(unknownorder ?vlist0 ?vlistagminternal)
		(= ?vlistagminternal ?vlist0)
		(isD ?vd)
		(do_pentagono_5)
		(Arg_vlist0_tipo ?vlist0)
		(Arg_vd_tipo ?vd)
		)
	:effect
		(and
		(firstunknown ?vlistagminternal)
		(isE ?vlist0)
		(proc_none)
		(not(firstunknown ?vlist0))
		(not(unknownorder ?vlist0 ?vlistagminternal))
		(not(do_pentagono_5))
		(not(Arg_vlist0_tipo ?vlist0))
		(not(Arg_vd_tipo ?vd))
		)
)


(:action hexagono_1
	:parameters(
		?vlistagminternal - tipo
		?vlist0 - tipo
		?vd - tipo
	)
	:precondition
		(and
		(unknownorder ?vlist0 ?vlistagminternal)
		(= ?vlistagminternal ?vlist0)
		(isD ?vd)
		(firstunknown ?vlist0)
		(proc_none)
		)
	:effect
		(and
		(firstunknown ?vlistagminternal)
		(isF ?vlist0)
		(do_hexagono_2)
		(Arg_vlist0_tipo ?vlist0)
		(Arg_vd_tipo ?vd)
		(not(firstunknown ?vlist0))
		(not(unknownorder ?vlist0 ?vlistagminternal))
		(not(proc_none))
		)
)


(:action hexagono_2
	:parameters(
		?vc - tipo
		?vd - tipo
		?ve - tipo
	)
	:precondition
		(and
		(unido ?vc ?vd)
		(unido ?vd ?ve)
		(do_hexagono_2)
		(Arg_vd_tipo ?vd)
		)
	:effect
		(and
		(do_hexagono_3)
		(Arg_vc_tipo ?vc)
		(Arg_ve_tipo ?ve)
		(not(do_hexagono_2))
		(not(Arg_vd_tipo ?vd))
		)
)


(:action hexagono_3
	:parameters(
		?va - tipo
		?vc - tipo
		?vb - tipo
	)
	:precondition
		(and
		(isA ?va)
		(isC ?vc)
		(unido ?vb ?vc)
		(do_hexagono_3)
		(Arg_vc_tipo ?vc)
		)
	:effect
		(and
		(do_hexagono_4)
		(Arg_va_tipo ?va)
		(Arg_vb_tipo ?vb)
		(not(do_hexagono_3))
		(not(Arg_vc_tipo ?vc))
		)
)


(:action hexagono_4
	:parameters(
		?vb - tipo
		?ve - tipo
		?va - tipo
	)
	:precondition
		(and
		(isB ?vb)
		(isE ?ve)
		(unido ?va ?vb)
		(do_hexagono_4)
		(Arg_vb_tipo ?vb)
		(Arg_ve_tipo ?ve)
		(Arg_va_tipo ?va)
		)
	:effect
		(and
		(do_hexagono_5)
		(not(do_hexagono_4))
		(not(Arg_vb_tipo ?vb))
		)
)


(:action hexagono_5
	:parameters(
		?ve - tipo
		?vlist0 - tipo
		?va - tipo
	)
	:precondition
		(and
		(unido ?ve ?va)
		(do_hexagono_5)
		(Arg_ve_tipo ?ve)
		(Arg_vlist0_tipo ?vlist0)
		(Arg_va_tipo ?va)
		)
	:effect
		(and
		(unido ?ve ?vlist0)
		(unido ?vlist0 ?va)
		(proc_none)
		(not(unido ?ve ?va))
		(not(do_hexagono_5))
		(not(Arg_ve_tipo ?ve))
		(not(Arg_vlist0_tipo ?vlist0))
		(not(Arg_va_tipo ?va))
		)
)

)
