/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_ESTIMATE_POSES_H
#define INCLUDED_MEDUSA_ESTIMATE_POSES_H

#include <opencv2/core.hpp>
#include <opencv2/aruco.hpp>
#include <opencv2/calib3d.hpp>

#include <gnuradio/medusa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
namespace medusa {

/*!
 * \brief <+description of block+>
 * \ingroup medusa
 *
 */
class MEDUSA_API estimate_poses : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<estimate_poses> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of medusa::estimate_poses.
     *
     * To avoid accidental use of raw pointers, medusa::estimate_poses's
     * constructor is in a private implementation
     * class. medusa::estimate_poses::make is the public interface for
     * creating new instances.
     */
    static sptr
    make(std::string calibration_file, float marker_side_length, int width, int height);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_ESTIMATE_POSES_H */
