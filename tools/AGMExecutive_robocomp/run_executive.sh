#!/usr/bin/env bash

#
# RCIS
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession 
sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/cajasvacias1/Files/ && rcis simulatedWorld.xml &'
qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess 'RCIS'
sleep 2;

#
# IceStorm
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/cajasvacias1/Files'
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'icebox --Ice.Config=config.icebox'
qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess 'storm'
sleep 1;

#
# Navigator
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/cajasvacias1/Files'
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand '/home/robocomp/robocomp/Components/RoboLab/Experimental/vfhLocalNavigatorComp/bin/vfhlocalnavigatorcomp --Ice.Config=navigator.conf'
qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess 'navigator'
sleep 2;

#
# Agente de navegacion
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/cajasvacias1/Components/navegacion'
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'make && bin/navegacioncomp --Ice.Config=/home/robocomp/cajasvacias1/Files/navegacion.conf'
qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess 'navegacion'

#
# Agente rompellaves
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/cajasvacias1/Components/rompellaves'
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'make && bin/rompellavescomp --Ice.Config=/home/robocomp/cajasvacias1/Files/rompellaves.conf'
qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess 'rompellaves'
sleep 2;


#
# EXECUTIVE
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/AGM/tools/AGMExecutive_robocomp'
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'python AGMExecutive_robocomp.py --Ice.Config=config'
qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess 'executive'

#
# Mission
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
sess=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/cajasvacias1/Components/mission'
qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'make && bin/missionagent --Ice.Config=/home/robocomp/cajasvacias1/Files/mission.conf'
qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess 'mission'




