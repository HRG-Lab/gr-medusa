/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_ARUCO_DETECTOR_H
#define INCLUDED_MEDUSA_ARUCO_DETECTOR_H

#include <opencv2/aruco.hpp>
#include <opencv2/core.hpp>

#include <gnuradio/medusa/api.h>
#include <gnuradio/sync_block.h>
#include <string>

namespace gr {
namespace medusa {

/*!
 * \brief <+description of block+>
 * \ingroup medusa
 *
 */
class MEDUSA_API aruco_detector : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<aruco_detector> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of medusa::aruco_detector.
     *
     * To avoid accidental use of raw pointers, medusa::aruco_detector's
     * constructor is in a private implementation
     * class. medusa::aruco_detector::make is the public interface for
     * creating new instances.
     */
    static sptr make(int dictionary, int width, int height);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_ARUCO_DETECTOR_H */
