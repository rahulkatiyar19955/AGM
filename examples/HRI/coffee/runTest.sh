#!/usr/bin/env sh

# tests="1_rule_findObjectVisually 2_findObject 3_findMug 4_cleanTable"
tests="4_cleanTable"

for i in $tests;
do
	echo -n "\n\n\n\nRun next ($i)? "; read a
	agglplan table.aggl          $i/world.xml $i/goal.xml
done;

