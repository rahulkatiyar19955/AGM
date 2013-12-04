cmake_minimum_required (VERSION 2.6)
add_library(_thisisjustafakelibrary SHARED fake.cpp)

add_custom_command(
    TARGET _thisisjustafakelibrary
    POST_BUILD
    COMMAND bash runaftercompilation.sh ${ROBOCOMP_SUPPORT}
    COMMAND rm -f lib_thisisjustafakelibrary.so
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

