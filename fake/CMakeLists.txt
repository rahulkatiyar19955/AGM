cmake_minimum_required (VERSION 2.6)
project(fake CXX)
add_library(${PROJECT_NAME} SHARED fake.cpp)



add_custom_command(
    TARGET fake
    POST_BUILD
    COMMAND sh runaftercompilation.sh ${ROBOCOMP_SUPPORT}
    COMMAND rm -f ${ROOT_BIN_DIR}/libfake.so
    COMMAND rm -f ../libfake.so
    COMMAND rm -f libfake.so
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

