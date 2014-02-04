cmake_minimum_required( VERSION 2.8)

#  Compiler options  #
#####################
set(CMAKE_CXX_FLAGS "-Wall -Wfatal-errors " )
INCLUDE_DIRECTORIES ( . libagm )


#  Optional features and options  #
###################################
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
	SET(ROBOCOMP_SUPPORT_VAL "1")
else (ROBOCOMP_SUPPORT)
	MESSAGE(STATUS "ROBOCOMP SUPPORT:       NO")
	SET(ROBOCOMP_SUPPORT_VAL "0")
endif (ROBOCOMP_SUPPORT)

MESSAGE(STATUS "\n\n")


#  Handle optional features  #
##############################

# Python bindings
if (PYTHON_BINDINGS)
	# Add bindings source code file
	SET(SOURCES ${SOURCES} libagm/agm_python.cpp)
endif (PYTHON_BINDINGS)

#  Boost library  #
set(Boost_USE_STATIC_LIBS   OFF)
set(Boost_USE_MULTITHREADED ON)
if (PYTHON_BINDINGS)
	find_package(Boost COMPONENTS system thread python REQUIRED)
else (PYTHON_BINDINGS)
	find_package(Boost COMPONENTS system thread REQUIRED)
endif (PYTHON_BINDINGS)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})
# (libpython)
find_package(PythonLibs REQUIRED)
MESSAGE(STATUS "PYTHON BINDINGS: DIRS ${PYTHON_INCLUDE_DIRS}")
MESSAGE(STATUS "PYTHON BINDINGS: LIBS ${PYTHON_LIBRARIES}")
include_directories(${PYTHON_INCLUDE_DIRS})
link_directories(${PYTHON_LIBRARIES})

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
      OUTPUT tools/ui/ui_${input_file}.py
      COMMAND pyside-uic tools/ui/${input_file}.ui -o tools/ui/ui_${input_file}.py
      DEPENDS tools/ui/${input_file}.ui
      COMMENT "Generating tools/ui/ui_${input_file}.py from tools/ui/${input_file}.ui"
    )
    ADD_CUSTOM_TARGET(ui_${input_file} ALL DEPENDS tools/ui/ui_${input_file}.py )
  ENDFOREACH( input_file )
ENDMACRO( WRAP_PYTHON_UI )
MACRO( WRAP_PYTHON_QRC )
  FOREACH( input_file ${ARGN} )
    ADD_CUSTOM_COMMAND (
      OUTPUT tools/ui/${input_file}_rc.py
      COMMAND pyside-rcc tools/ui/${input_file}.qrc -o tools/ui/${input_file}_rc.py
      DEPENDS tools/ui/${input_file}.qrc
      COMMENT "Generating tools/ui/${input_file}_rc.py from tools/ui/${input_file}.qrc"
    )
    ADD_CUSTOM_TARGET(${input_file}_rc ALL DEPENDS tools/ui/${input_file}_rc.py )
  ENDFOREACH( input_file )
ENDMACRO( WRAP_PYTHON_QRC )
WRAP_PYTHON_UI( guiAGGLEditor guiGraphViewer appearance )
WRAP_PYTHON_QRC( resource )


# # COMPILE FLEX AND BISON FILE FOR THE AGGL PARSER #
# ###################################################
# # Create target for the parser
# ADD_CUSTOM_TARGET(AGGLParser echo "Creating agglparser.cpp")
# ADD_CUSTOM_COMMAND(
#   SOURCE libagm/aggllexer.l
#   COMMAND flex
#   ARGS --outfile=libagm/aggllexer.cpp libagm/aggllexer.l
#   OUTPUT libagm/aggllexer.cpp
# )
#  ADD_CUSTOM_COMMAND(
#    SOURCE libagm/agglparser.y
#    COMMAND bison
#    ARGS -d -y libagm/agglparser.y -o libagm/agglparser.cpp
#    DEPENDS libagm/aggllexer.cpp
#    OUTPUT libagm/agglparser.cpp libagm/agglparser.hpp
# )
# SET_SOURCE_FILES_PROPERTIES(libagm/agglparser.cpp GENERATED) 
# SET_SOURCE_FILES_PROPERTIES(libagm/aggllexer.cpp GENERATED) 
# SET(AGM_CODE ${AGM_CODE} libagm/aggllexer.cpp libagm/agglparser.cpp)
# SET(LIBS ${LIBS} -lfl )


#  Library building  #
######################
if (ROBOCOMP_SUPPORT)
   add_library(agmdummy SHARED AGMWorldModel.cpp )
endif (ROBOCOMP_SUPPORT)

add_library(agm SHARED ${AGM_CODE} )
target_link_libraries(agm ${Boost_LIBRARIES} ${LIBS} ${PYTHON_LIBRARIES})
add_dependencies(agm agmdummy)

add_executable ( testagm tools/testagm.cpp )
target_link_libraries ( testagm agm -L. -L.. -lagm ${LIBS} ${ICE_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} )
add_dependencies(testagm agm)

add_executable ( agm_xml2pddlProblem tools/agm_xml2pddlProblem.cpp )
target_link_libraries ( agm_xml2pddlProblem agm -L. -L.. -lagm ${LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} )
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


# Configure actual header with the proper options
configure_file ("libagm/agm_config.in.h" "libagm/agm_config.h")



#  Installation  #
##################
SET( INST_BIN_PATH   ${CMAKE_INSTALL_PREFIX}/bin )
SET( INST_LIB_PATH   ${CMAKE_INSTALL_PREFIX}/lib )
SET( INST_INCL_PATH  ${CMAKE_INSTALL_PREFIX}/include )
SET( INST_SHARE_PATH ${CMAKE_INSTALL_PREFIX}/share/agm )

INSTALL(FILES libagm.so DESTINATION ${INST_LIB_PATH}/ )
INSTALL(FILES ${HEADERS} DESTINATION ${INST_INCL_PATH}/ )
INSTALL(PROGRAMS agm_xml2pddlProblem DESTINATION ${INST_BIN_PATH}/ )
INSTALL(PROGRAMS tools/agm_xmlViewer.py DESTINATION ${INST_BIN_PATH}/ RENAME agm_xmlViewer )
INSTALL(PROGRAMS tools/AGGLEditor.py DESTINATION ${INST_BIN_PATH}/ RENAME AGGLEditor)
INSTALL(PROGRAMS tools/aggl2pddl DESTINATION ${INST_BIN_PATH}/ )
INSTALL(PROGRAMS tools/aggl2agglpy DESTINATION ${INST_BIN_PATH}/ )
INSTALL(PROGRAMS "AGGLPlanner/agglplanner.py" DESTINATION ${INST_BIN_PATH}/ RENAME agglplanner )
INSTALL(PROGRAMS "AGGLPlanner/agglplanner.py" DESTINATION ${INST_SHARE_PATH}/ RENAME agglplanner.py )
INSTALL(PROGRAMS "AGGLPlanner/agglplanchecker.py" DESTINATION ${INST_BIN_PATH}/ RENAME agglplanchecker )
INSTALL(PROGRAMS "AGGLPlanner/agglplanchecker.py" DESTINATION ${INST_SHARE_PATH}/ RENAME agglplanchecker.py )
INSTALL(PROGRAMS "AGGLPlanner/agglplan.py" DESTINATION ${INST_BIN_PATH}/ RENAME agglplan )
INSTALL(PROGRAMS "AGGLPlanner/agglplan.py" DESTINATION ${INST_SHARE_PATH}/ RENAME agglplan.py )

if (ROBOCOMP_SUPPORT)
	INSTALL(FILES AGMWorldModel.h DESTINATION ${INST_INCL_PATH}/ )
endif (ROBOCOMP_SUPPORT)

INSTALL(PROGRAMS python/parseAGGL.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS python/parseQuantifiers.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS python/pddlAGGL.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS python/xmlModelParser.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS python/generateAGGLPlannerCode.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS python/AGMModule.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS python/AGGL.py DESTINATION ${INST_SHARE_PATH})

INSTALL(PROGRAMS tools/ui/ui_guiAGGLEditor.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS tools/ui/ui_guiGraphViewer.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS tools/ui/ui_appearance.py DESTINATION ${INST_SHARE_PATH})
INSTALL(PROGRAMS tools/ui/resource_rc.py DESTINATION ${INST_SHARE_PATH})

INSTALL(PROGRAMS tools/aggl_completion.bash DESTINATION /etc/bash_completion.d/ RENAME AGGLEditor)


