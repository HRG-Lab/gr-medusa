/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_ARUCO_DETECTOR_IMPL_H
#define INCLUDED_MEDUSA_ARUCO_DETECTOR_IMPL_H

#include <gnuradio/medusa/aruco_detector.h>

namespace gr {
namespace medusa {

class aruco_detector_impl : public aruco_detector
{
private:
    int d_width;
    int d_height;

    cv::aruco::Dictionary d_dictionary;
    cv::aruco::DetectorParameters d_params;
    cv::aruco::ArucoDetector d_detector;

public:
    aruco_detector_impl(int dictionary, int width, int height);
    ~aruco_detector_impl();

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_ARUCO_DETECTOR_IMPL_H */
