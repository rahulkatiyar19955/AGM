cmake_minimum_required( VERSION 2.6 )


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

WRAP_PYTHON_UI( guiAGGLEditor appearance )



set(CMAKE_CXX_FLAGS "-Wall -Wfatal-errors " )

INCLUDE_DIRECTORIES ( . )


# get boost
set(Boost_USE_STATIC_LIBS   OFF)
set(Boost_USE_MULTITHREADED ON)
find_package(Boost COMPONENTS system thread python REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

# get python
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
link_directories(${PYTHON_LIBRARIES})


SET (AGM_CODE
  agm.cpp
  agm_python.cpp
  agm_behavior.cpp
  agm_model.cpp
  agm_modelEdge.cpp
  agm_modelPrinter.cpp
  agm_modelSymbols.cpp
)


add_library(agm SHARED ${AGM_CODE} )
target_link_libraries(agm ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})


# add_executable ( testagm testagm.cpp  )
# target_link_libraries ( testagm  -L. -lagm )
