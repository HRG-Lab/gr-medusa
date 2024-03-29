# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT medusa_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT medusa_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND medusa_python_files
    opencv_source_python.cc
    aruco_detector_python.cc
    estimate_poses_python.cc
    preamble_to_pdu_python.cc
    opencv_aruco_corner_source_python.cc python_bindings.cc)

GR_PYBIND_MAKE_OOT(medusa
   ../../..
   gr::medusa
   "${medusa_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET medusa_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:medusa_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/medusa/
)

install(TARGETS medusa_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/medusa COMPONENT pythonapi)
