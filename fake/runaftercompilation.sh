#!/usr/bin/env bash

if [ "$1" = "True" ] ; then
  echo "#define ROBOCOMP_SUPPORT 1" > ../agm_config.h
else
  echo "" > ../agm_config.h
fi


