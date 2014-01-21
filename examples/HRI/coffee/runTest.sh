#!/usr/bin/env sh

tests="0_findMilk"

for i in $tests;
do
	echo -n "\n\n\n\nRun next ($i)? "; read a
	agglplan coffee.aggl $i/world.xml $i/goal.xml
done;

