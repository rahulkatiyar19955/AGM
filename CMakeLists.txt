cmake_minimum_required( VERSION 2.8)

#  General options  #
#####################
set(CMAKE_CXX_FLAGS "-Wall -Wfatal-errors " )
INCLUDE_DIRECTORIES ( . )


#  Optional features  #
#######################
option (PYTHON_BINDINGS "Build python bindings" ON)
option (ROBOCOMP_SUPPORT "Build with support for RoboComp" ON)


#  Set sources  #
#################
SET (AGM_CODE
  agm.cpp
  agm_behavior.cpp
  agm_misc_functions.cpp
  agm_model.cpp
  agm_modelEdge.cpp
  agm_modelPrinter.cpp
  agm_modelSymbols.cpp
  agm_modelConverter.cpp

  WorldModel.cpp
)


SET (HEADERS
  agm_behavior.h
  agm.h
  agm_modelDrawer.h
  agm_modelEdge.h
  agm_modelException.h
  agm_model.h
  agm_modelPrinter.h
  agm_modelSymbols.h
  agm_misc_functions.h
  agm_modelConverter.h
)


#  Show enabled optional features  #
####################################
MESSAGE(STATUS "\n\nOptional features:")

if (PYTHON_BINDINGS)
	MESSAGE(STATUS "PYTHON BINDINGS:        YES")
else (PYTHON_BINDINGS)
	MESSAGE(STATUS "PYTHON BINDINGS:        NO")
endif (PYTHON_BINDINGS)

if (ROBOCOMP_SUPPORT)
	MESSAGE(STATUS "ROBOCOMP SUPPORT:       YES")
else (ROBOCOMP_SUPPORT)
	MESSAGE(STATUS "ROBOCOMP SUPPORT:       NO")
endif (ROBOCOMP_SUPPORT)

MESSAGE(STATUS "\n\n")


#  Handle optional features  #
##############################

# Python bindings
if (PYTHON_BINDINGS)
	# Add bindings source code file
	SET(SOURCES ${SOURCES} agm_python.cpp)
	# Linking and wrapping stuff
	# (boost)
	set(Boost_USE_STATIC_LIBS   OFF)
	set(Boost_USE_MULTITHREADED ON)
	find_package(Boost COMPONENTS system thread python REQUIRED)
	include_directories(${Boost_INCLUDE_DIRS})
	link_directories(${Boost_LIBRARY_DIRS})
	# (libpython)
	find_package(PythonLibs REQUIRED)
	MESSAGE(STATUS "PYTHON BINDINGS: DIRS ${PYTHON_INCLUDE_DIRS}")
	MESSAGE(STATUS "PYTHON BINDINGS: LIBS ${PYTHON_LIBRARIES}")
	include_directories(${PYTHON_INCLUDE_DIRS})
	link_directories(${PYTHON_LIBRARIES})
endif (PYTHON_BINDINGS)

# RoboComp support
if (ROBOCOMP_SUPPORT)
	MESSAGE(STATUS "ROBOCOMP PATH:        $ENV{ROBOCOMP}")
	INCLUDE( $ENV{ROBOCOMP}/CMake/robocomp.cmake )
	ROBOCOMP_INITIALIZE( $ENV{ROBOCOMP}/ )
	ROBOCOMP_WRAP_ICE( WorldModel )
	SET(ICE_LIBS -lIce)
endif (ROBOCOMP_SUPPORT)


#  Macro for compiling UI files and wrap command  #
###################################################
MACRO( WRAP_PYTHON_UI )
  FOREACH( input_file ${ARGN} )
    ADD_CUSTOM_COMMAND (
      OUTPUT ui_${input_file}.py
      COMMAND pyside-uic ${input_file}.ui -o ui_${input_file}.py
      DEPENDS ${input_file}.ui
      COMMENT "Generating ui_${input_file}.py from ${input_file}.ui"
    )
    ADD_CUSTOM_TARGET(ui_${input_file} ALL DEPENDS ui_${input_file}.py )
  ENDFOREACH( input_file )
ENDMACRO( WRAP_PYTHON_UI )

WRAP_PYTHON_UI( guiAGGLEditor guiAGMExecutiveClient appearance )


#  Library building  #
######################
add_library(agm SHARED ${AGM_CODE} )
target_link_libraries(agm ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

add_executable ( testagm testagm.cpp  )
target_link_libraries ( testagm  -L. -lagm ${ICE_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} )
add_dependencies(testagm agm)



#  Installation  #
##################
INSTALL(FILES libagm.so DESTINATION /opt/robocomp/lib/ )
INSTALL(FILES ${HEADERS} DESTINATION /opt/robocomp/include/ )
