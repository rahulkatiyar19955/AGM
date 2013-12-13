#!/usr/bin/env bash

filepath="../agm_config.h"
if [ -e ${filepath} ] ; then
# 	echo "${filepath} exists"
	words=`wc ${filepath} | awk '{ print $2 }'`
else
	words=""
# 	echo "${filepath} does NOT exist"
fi
# echo "wc ${words}"

back="ddd"
if [ "${words}" = "3" ] ; then
	back="True"
else
	back="False"
fi

if [ "$back" != "$1" ] ; then
	echo "Updating ${filepath}"
	if [ "$1" = "True" ] ; then
		echo "#define ROBOCOMP_SUPPORT 1" > ${filepath}
	else
		echo "" > ${filepath}
	fi
# else
# 	echo "not updating"
fi

