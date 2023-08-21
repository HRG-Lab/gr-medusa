/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_ESTIMATE_POSES_IMPL_H
#define INCLUDED_MEDUSA_ESTIMATE_POSES_IMPL_H

#include <gnuradio/medusa/estimate_poses.h>
#include <opencv2/core/types.hpp>

using namespace cv;

namespace gr {
namespace medusa {

class estimate_poses_impl : public estimate_poses
{
private:
    float d_marker_len;
    int d_width;
    int d_height;
    Mat d_cam_mtx;
    Mat d_dist_coeffs;
    std::vector<Point3f> d_marker_pts;

public:
    estimate_poses_impl(std::string calibration_file,
                        float marker_side_length,
                        int width,
                        int height);
    ~estimate_poses_impl();

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_ESTIMATE_POSES_IMPL_H */
