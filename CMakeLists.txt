cmake_minimum_required( VERSION 2.6 )

MACRO( WRAP_PYTHON_UI )
  FOREACH( input_file ${ARGN} )
    ADD_CUSTOM_COMMAND (
      OUTPUT ui_${input_file}.py
      COMMAND pyuic4 ${input_file}.ui -o ui_${input_file}.py
      DEPENDS ${input_file}.ui
      COMMENT "Generating ui_${input_file}.py from ${input_file}.ui"
    )
    ADD_CUSTOM_TARGET(ui_${input_file} ALL DEPENDS ui_${input_file}.py )
  ENDFOREACH( input_file )
ENDMACRO( WRAP_PYTHON_UI )

#ADD_CUSTOM_COMMAND (
#	OUTPUT graphmars
#	COMMAND cp graphmars.py graphmars
#	COMMAND chmod 755 graphmars
#)
#ADD_CUSTOM_TARGET(exec_graphmars ALL DEPENDS graphmars )

WRAP_PYTHON_UI( guiAGMEditor appearance )

# Program destination directory
# SET( DEST_DIR "/usr/local/bin/")
# INSTALL(FILES monitorComp       DESTINATION ${DEST_DIR} PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE )



