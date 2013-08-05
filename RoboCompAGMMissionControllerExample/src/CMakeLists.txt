cmake_minimum_required(VERSION 2.6)
PROJECT( agmmissionexample )

# Sources set
SET ( SOURCES
  gualzru_visualizerComp.cpp
  worker.cpp
  $ENV{ROBOCOMP}/Classes/rapplication/rapplication.cpp
  $ENV{ROBOCOMP}/Classes/qlog/qlog.cpp
  $ENV{ROBOCOMP}/Classes/rcdraw/rcdraw.cpp
)

# Headers set
SET ( HEADERS
  worker.h
  $ENV{ROBOCOMP}/Classes/rcdraw/rcdraw.h
  /opt/robocomp/include/agm_modelDrawer.h
)

INCLUDE_DIRECTORIES(../../../../Classes)
INCLUDE_DIRECTORIES( $ENV{ROBOCOMP}/Classes)

# OpenMP
find_package(OpenMP)
if(OPENMP_FOUND)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif(OPENMP_FOUND)

# RoboComp
INCLUDE( $ENV{ROBOCOMP}/CMake/robocomp.cmake )
ROBOCOMP_INITIALIZE( $ENV{ROBOCOMP}/ )
ROBOCOMP_WRAP_ICE( AGMAgent AGMCommonBehavior AGMExecutive Planning )
QT4_WRAP_UI( UI_HEADERS guiDlg.ui )

# Qt4
ADD_DEFINITIONS( -Wall -DQT_DLL -DQT_GUI_LIB -DQT_CORE_LIB )
FIND_PACKAGE( Qt4 REQUIRED )
SET( QT_USE_QTGUI TRUE )
SET( QT_USE_QTOPENGL TRUE )
SET( QT_USE_QTXML TRUE )
INCLUDE( ${QT_USE_FILE} )
QT4_WRAP_CPP( MOC_SOURCES ${HEADERS} )



# Specify construction and link process
SET (EXECUTABLE_OUTPUT_PATH ../bin)
ADD_EXECUTABLE( agmmissionexample ${SOURCES} ${MOC_SOURCES} ${RC_SOURCES} ${UI_HEADERS} )
TARGET_LINK_LIBRARIES( agmmissionexample ${LIBS} ${QT_LIBRARIES} -lagm )
INSTALL(FILES ${EXECUTABLE_OUTPUT_PATH}/agmmissionexample DESTINATION /opt/robocomp/bin/ PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE )
