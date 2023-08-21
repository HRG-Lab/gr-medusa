/*
 * Copyright 2023 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(estimate_poses.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(181b25399dde96012e27b6660f21c844)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/medusa/estimate_poses.h>
// pydoc.h is automatically generated in the build directory
#include <estimate_poses_pydoc.h>

void bind_estimate_poses(py::module& m)
{

    using estimate_poses = ::gr::medusa::estimate_poses;


    py::class_<estimate_poses,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<estimate_poses>>(m, "estimate_poses", D(estimate_poses))

        .def(py::init(&estimate_poses::make),
             py::arg("calibration_file"),
             py::arg("marker_side_length"),
             py::arg("width"),
             py::arg("height"),
             D(estimate_poses, make))


        ;
}
