cmake_minimum_required( VERSION 2.8)

#  General options  #
#####################
set(CMAKE_CXX_FLAGS "-Wall -Wfatal-errors " )
INCLUDE_DIRECTORIES ( . libagm )


#  Optional features  #
#######################
option (PYTHON_BINDINGS "Build python bindings" OFF)
option (ROBOCOMP_SUPPORT "Build with support for RoboComp" OFF)


#  Set sources  #
#################
SET (AGM_CODE
  libagm/agm.cpp
  libagm/agm_misc_functions.cpp
  libagm/agm_model.cpp
  libagm/agm_modelEdge.cpp
  libagm/agm_modelPrinter.cpp
  libagm/agm_modelSymbols.cpp
  libagm/agm_modelConverter.cpp
  libagm/agm_search.cpp
  libagm/agm_searchPath.cpp
  libagm/agm_rule.cpp
)


SET (HEADERS
  libagm/agm.h
  libagm/agm_modelDrawer.h
  libagm/agm_modelEdge.h
  libagm/agm_modelException.h
  libagm/agm_model.h
  libagm/agm_modelPrinter.h
  libagm/agm_modelSymbols.h
  libagm/agm_misc_functions.h
  libagm/agm_modelConverter.h
  libagm/agm_search.h
  libagm/agm_rule.h
  libagm/agm_config.h
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
	SET(SOURCES ${SOURCES} libagm/agm_python.cpp)
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
	SET(ICE_LIBS -lIce)
	ROBOCOMP_WRAP_ICE( AGMWorldModel )
	ADD_DEFINITIONS(-DROBOCOMP_SUPPORT=1)
endif (ROBOCOMP_SUPPORT)

# LibXML
FIND_PACKAGE(LibXml2 REQUIRED)
include_directories(${LIBXML2_INCLUDE_DIR})
set(LIBS ${LIBS} ${LIBXML2_LIBRARIES} )

#  Macro for compiling UI files and wrap command  #
###################################################
MACRO( WRAP_PYTHON_UI )
  FOREACH( input_file ${ARGN} )
    ADD_CUSTOM_COMMAND (
      OUTPUT ui/ui_${input_file}.py
      COMMAND pyside-uic ui/${input_file}.ui -o ui/ui_${input_file}.py
      DEPENDS ui/${input_file}.ui
      COMMENT "Generating ui/ui_${input_file}.py from ui/${input_file}.ui"
    )
    ADD_CUSTOM_TARGET(ui_${input_file} ALL DEPENDS ui/ui_${input_file}.py )
  ENDFOREACH( input_file )
ENDMACRO( WRAP_PYTHON_UI )

WRAP_PYTHON_UI( guiAGGLEditor guiGraphViewer appearance )


# COMPILE FLEX AND BISON FILE FOR THE AGGL PARSER #
###################################################
# Create target for the parser
ADD_CUSTOM_TARGET(AGGLParser echo "Creating agglparser.cpp")
ADD_CUSTOM_COMMAND(
  SOURCE libagm/aggllexer.l
  COMMAND flex
  ARGS --outfile=libagm/aggllexer.cpp libagm/aggllexer.l
  OUTPUT libagm/aggllexer.cpp
)
 ADD_CUSTOM_COMMAND(
   SOURCE libagm/agglparser.y
   COMMAND bison
   ARGS -d -y libagm/agglparser.y -o libagm/agglparser.cpp
   DEPENDS libagm/aggllexer.cpp
   OUTPUT libagm/agglparser.cpp libagm/agglparser.hpp
)
SET_SOURCE_FILES_PROPERTIES(agglparser.cpp GENERATED) 
SET_SOURCE_FILES_PROPERTIES(aggllexer.cpp GENERATED) 
SET(AGM_CODE ${AGM_CODE} aggllexer.cpp agglparser.cpp)
SET(LIBS ${LIBS} -lfl )


#  Library building  #
######################
if (ROBOCOMP_SUPPORT)
   add_library(agmdummy SHARED AGMWorldModel.cpp )
endif (ROBOCOMP_SUPPORT)

add_library(agm SHARED ${AGM_CODE} )
target_link_libraries(agm ${Boost_LIBRARIES} ${LIBS} ${PYTHON_LIBRARIES})
add_dependencies(agm agmdummy)

add_executable ( testagm tools/testagm.cpp )
target_link_libraries ( testagm  -L. -lagm ${LIBS} ${ICE_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} )
add_dependencies(testagm agm)

add_executable ( agm_xml2pddlProblem tools/agm_xml2pddlProblem.cpp )
target_link_libraries ( agm_xml2pddlProblem  -L. -lagm ${LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} )
add_dependencies(testagm agm)




#  Doxygen  #
#############
find_package(Doxygen)
if(DOXYGEN_FOUND)
  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/doc/Doxyfile.in ${CMAKE_CURRENT_BINARY_DIR}/doc/Doxyfile @ONLY)
  add_custom_target(doc
  ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/doc/Doxyfile
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT "Generating API documentation with Doxygen" VERBATIM
)
endif(DOXYGEN_FOUND)

#  fake project to execute command  #
#####################################
add_subdirectory(fake)



#  Installation  #
##################
INSTALL(FILES libagm.so DESTINATION /opt/robocomp/lib/ )
INSTALL(FILES ${HEADERS} DESTINATION /opt/robocomp/include/ )
INSTALL(PROGRAMS agm_xml2pddlProblem DESTINATION /opt/robocomp/bin/ )
INSTALL(PROGRAMS agm_xmlViewer.py DESTINATION /opt/robocomp/bin/ RENAME agm_xmlViewer )
INSTALL(PROGRAMS AGGLEditor.py DESTINATION /opt/robocomp/bin/ RENAME AGGLEditor)
INSTALL(PROGRAMS aggl2pddl DESTINATION /opt/robocomp/bin/ )
INSTALL(PROGRAMS aggl2agglpy DESTINATION /opt/robocomp/bin/ )
INSTALL(PROGRAMS "AGGLPlanner/agglplanner.py" DESTINATION /opt/robocomp/bin/ RENAME agglplanner )
INSTALL(PROGRAMS "AGGLPlanner/agglplanner.py" DESTINATION /opt/robocomp/share/ RENAME agglplanner.py )
INSTALL(PROGRAMS "AGGLPlanner/agglplanchecker.py" DESTINATION /opt/robocomp/bin/ RENAME agglplanchecker )
INSTALL(PROGRAMS "AGGLPlanner/agglplanchecker.py" DESTINATION /opt/robocomp/share/ RENAME agglplanchecker.py )
INSTALL(PROGRAMS "AGGLPlanner/agglplan.py" DESTINATION /opt/robocomp/bin/ RENAME agglplan )
INSTALL(PROGRAMS "AGGLPlanner/agglplan.py" DESTINATION /opt/robocomp/share/ RENAME agglplan.py )

if (ROBOCOMP_SUPPORT)
INSTALL(FILES AGMWorldModel.h DESTINATION /opt/robocomp/include/ )
endif (ROBOCOMP_SUPPORT)

INSTALL(PROGRAMS ui_guiAGGLEditor.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS ui_guiGraphViewer.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS ui_appearance.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS parseAGGL.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS pddlAGGL.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS xmlModelParser.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS generateAGGLPlannerCode.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS AGMModule.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS AGGL.py DESTINATION /opt/robocomp/share)
INSTALL(PROGRAMS aggl_completion.bash DESTINATION /etc/bash_completion.d/ RENAME AGGLEditor)



