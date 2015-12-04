
set(PROJECT_NAME CACHE STRING "Module")

cmake_minimum_required (VERSION 2.6)
project (${PROJECT_NAME})
set(CMAKE_BUILD_TYPE "Release")
set(PYTHON_EXECUTABLE CACHE STRING "python")
set(INTERROGATE_LIB CACHE STRING "p3interrogatedb")


if (WIN32)
  
  set(PYTHONVER CACHE STRING "27")
  
  # Find panda path
  EXECUTE_PROCESS(
    COMMAND "${PYTHON_EXECUTABLE}" "-B" "Scripts/common.py" "--print-sdk-path"
    OUTPUT_VARIABLE WIN_PANDA_PATH
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

  # Find thirdparty directory
  IF(CMAKE_CL_32)
    set(THIRDPARTY_DIR "${WIN_PANDA_PATH}/../thirdparty/win-libs-vc10")
    IF(NOT (EXISTS "${THIRDPARTY_DIR}"))
      set(THIRDPARTY_DIR "${WIN_PANDA_PATH}/thirdparty/win-libs-vc10")
    ENDIF()
  ELSE()
    set(THIRDPARTY_DIR "${WIN_PANDA_PATH}/../thirdparty/win-libs-vc10-x64")
    IF(NOT (EXISTS "${THIRDPARTY_DIR}"))
      set(THIRDPARTY_DIR "${WIN_PANDA_PATH}/thirdparty/win-libs-vc10-x64")
    ENDIF()
  ENDIF()

  # These vars are based on the WIN_PANDA_PATH and usually are correct
  set(PANDA_LIBRARY_DIRS "${WIN_PANDA_PATH}/lib")
  set(PANDA_INCLUDE_DIR "${WIN_PANDA_PATH}/include") 
  set(PYTHON_LIBRARIES "${WIN_PANDA_PATH}/python/libs/python${PYTHONVER}.lib")
  set(PYTHON_INCLUDE_DIRS "${WIN_PANDA_PATH}/python/include")

  set(BULLET_LIBRARIES "")
  set(BULLET_INCLUDE_DIRS "${THIRDPARTY_DIR}/bullet/include")
  set(EIGEN_INCLUDE_DIRS "${THIRDPARTY_DIR}/eigen/include")

  # Check if all supplied files exist
  set(CHECK_PATHS ${PANDA_LIBRARY_DIRS} ${PANDA_INCLUDE_DIR} ${PYTHON_LIBRARIES} ${PYTHON_INCLUDE_DIRS})
  foreach(PATH ${CHECK_PATHS})
    if(NOT (EXISTS "${PATH}"))
        message(FATAL_ERROR "The supplied path '${PATH}' could not be found!")
    endif()
  endforeach()

  # Link panda libraries
  set(PANDA_LIBRARIES "libp3framework;libpanda;libpandaexpress;libp3dtool;libp3dtoolconfig;libp3direct;lib${INTERROGATE_LIB}")
  link_directories("${PANDA_LIBRARY_DIRS}")

else()

  find_package(PythonLibs REQUIRED)
  find_package(PythonInterp REQUIRED)
  find_package(Bullet)

  set(EIGEN_INCLUDE_DIRS "/usr/include/eigen3")

  # Locate the headers
  find_path(PANDA_INCLUDE_DIR dtoolbase.h PATH_SUFFIXES panda3d)

  # Locate the libraries
  set(PANDA_LIBRARIES "")
  foreach(lib pandabullet p3framework panda pandaexpress p3dtool p3dtoolconfig p3direct ${INTERROGATE_LIB})
    find_library(PANDA_LIBRARY_${lib} ${lib} PATH_SUFFIXES panda3d)
    set(PANDA_LIBRARIES "${PANDA_LIBRARIES};${PANDA_LIBRARY_${lib}}")
  endforeach()

  find_package_handle_standard_args(Panda DEFAULT_MSG
                                    PANDA_LIBRARIES PANDA_INCLUDE_DIR)

  if(NOT EXISTS ${PANDA_INCLUDE_DIR})
    message(FATAL_ERROR "Could not find panda3d headers!")
  endif()

endif()


# Link panda includes / libraries
include_directories("${PANDA_INCLUDE_DIR}")

# Also link python includes / libraries
include_directories("${PYTHON_INCLUDE_DIRS}")
include_directories("${BULLET_INCLUDE_DIRS}")
include_directories("${EIGEN_INCLUDE_DIRS}")

# Run interrogate over the files
EXECUTE_PROCESS(
    COMMAND "${PYTHON_EXECUTABLE}" "-B" "Scripts/interrogate.py" "${PROJECT_NAME}"
    OUTPUT_VARIABLE output
    ERROR_VARIABLE errors
    RESULT_VARIABLE return_code
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

if(NOT ("${return_code}" STREQUAL "0"))
    message(FATAL_ERROR "Interrogate failed: ${output} ${errors}")
endif()

# Collect sources for compiling
file(GLOB_RECURSE SOURCES Source/*.cpp)
include_directories("Source/")
set(SOURCES ${SOURCES_H} ${SOURCES})

# Collect subdirs for compiling
file(GLOB_RECURSE POSSIBLE_DIRS Source/*)
FOREACH(PDIR ${POSSIBLE_DIRS})
  IF(IS_DIRECTORY Source/${PDIR})
    INCLUDE_DIRECTORIES("Source/${PDIR}")
  ENDIF()
ENDFOREACH()



# Set compiler flags
IF(MSVC)

    IF(CMAKE_CL_64)
      ADD_DEFINITIONS("/favor:blend /DWIN64_VC /DWIN64")
    ENDIF()

    ADD_DEFINITIONS("/wd4996")
    ADD_DEFINITIONS("/wd4275")
    ADD_DEFINITIONS("/wd4267")
    ADD_DEFINITIONS("/wd4101")
    ADD_DEFINITIONS("/wd4018")
    ADD_DEFINITIONS("/wd4273")
    # ADD_DEFINITIONS("/DWINVER=0x601")
    ADD_DEFINITIONS("/GR-")
    # ADD_DEFINITIONS("/O2")
    ADD_DEFINITIONS("/MD /Zi /GS- /Ob2 /Oi /Ot /fp:fast")
    ADD_DEFINITIONS("/Zm300 /DWIN32_VC /DWIN32")

    IF(CMAKE_CL_32)
      ADD_DEFINITIONS("/DWIN64_VC /DWIN64")
      ADD_DEFINITIONS("/machine:x86")
    ENDIF()

    ADD_DEFINITIONS("/W3")
    ADD_DEFINITIONS("/DEBUG")

    set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} /PDB /DEBUG /OPT:REF /OPT:ICF")
    set(CMAKE_SHARED_LINKER_FLAGS_MINSIZEREL "${CMAKE_SHARED_LINKER_FLAGS_MINSIZEREL} /PDB /DEBUG /OPT:REF /OPT:ICF")
    set(CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO "${CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO} /PDB /DEBUG /OPT:REF /OPT:ICF")

ELSE()
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native -march=native -std=c++11")
ENDIF()

# Define the module name
ADD_DEFINITIONS("/DPB_MODULE=${PROJECT_NAME}")
ADD_DEFINITIONS("/DPB_CFG_MODULE=${PROJECT_NAME}")

# Build library
add_library(${PROJECT_NAME} MODULE ${SOURCES})

# Don't add lib prefix on Linux
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")


FOREACH (flags_var_to_scrub
    CMAKE_CXX_FLAGS_RELEASE
    CMAKE_CXX_FLAGS_RELWITHDEBINFO
    CMAKE_CXX_FLAGS_MINSIZEREL
    CMAKE_C_FLAGS_RELEASE
    CMAKE_C_FLAGS_RELWITHDEBINFO
    CMAKE_C_FLAGS_MINSIZEREL)
  string (REGEX REPLACE "(^| )[/-]D *NDEBUG($| )" " "
    "${flags_var_to_scrub}" "${${flags_var_to_scrub}}")
ENDFOREACH()

# Add the required libraries
target_link_libraries(${PROJECT_NAME} ${PYTHON_LIBRARIES} ${PANDA_LIBRARIES} ${BULLET_LIBRARIES})


# After building, copy the file to the current directory
add_custom_command(
    TARGET ${PROJECT_NAME}
    POST_BUILD
    COMMAND "${PYTHON_EXECUTABLE}" "-B" "${CMAKE_CURRENT_LIST_DIR}/Scripts/finalize.py" "${PROJECT_NAME}"
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})


