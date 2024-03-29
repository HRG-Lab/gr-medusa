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
/* BINDTOOL_HEADER_FILE(preamble_to_pdu.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(f50de71058cf73adb5ecf7c7d48e2c97)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/medusa/preamble_to_pdu.h>
// pydoc.h is automatically generated in the build directory
#include <preamble_to_pdu_pydoc.h>

void bind_preamble_to_pdu(py::module& m)
{

    using preamble_to_pdu = ::gr::medusa::preamble_to_pdu;


    py::class_<preamble_to_pdu,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<preamble_to_pdu>>(m, "preamble_to_pdu", D(preamble_to_pdu))

        .def(py::init(&preamble_to_pdu::make),
             py::arg("num_elements"),
             py::arg("data_length"),
             py::arg("corr_tag"),
             D(preamble_to_pdu, make))


        ;
}
