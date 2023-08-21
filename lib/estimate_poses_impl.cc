/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "estimate_poses_impl.h"
#include <gnuradio/io_signature.h>
#include <gnuradio/tags.h>
#include <opencv2/calib3d.hpp>
#include <opencv2/core/matx.hpp>
#include <pmt/pmt.h>
#include <cstddef>
#include <cstdint>

namespace gr {
namespace medusa {

estimate_poses::sptr estimate_poses::make(std::string calibration_file,
                                          float marker_side_length,
                                          int width,
                                          int height)
{
    return gnuradio::make_block_sptr<estimate_poses_impl>(
        calibration_file, marker_side_length, width, height);
}


estimate_poses_impl::estimate_poses_impl(std::string calibration_file,
                                         float marker_side_length,
                                         int width,
                                         int height)
    : gr::sync_block("estimate_poses",
                     gr::io_signature::make(1, 1, width * height * 3 * sizeof(uint8_t)),
                     gr::io_signature::make(1, 1, width * height * 3 * sizeof(uint8_t))),
      d_marker_len(marker_side_length),
      d_width(width),
      d_height(height)
{
    FileStorage cal_file(calibration_file, cv::FileStorage::Mode::READ);
    cal_file["camera_matrix"] >> d_cam_mtx;
    cal_file["distortion_coefficients"] >> d_dist_coeffs;

    /*
    point 0: [-squareLength / 2, squareLength / 2, 0]
    point 1: [ squareLength / 2, squareLength / 2, 0]
    point 2: [ squareLength / 2, -squareLength / 2, 0]
    point 3: [-squareLength / 2, -squareLength / 2, 0]
    */

    float sl = marker_side_length;
    d_marker_pts = { { -sl / 2, sl / 2, 0 },
                     { sl / 2, sl / 2, 0 },
                     { sl / 2, -sl / 2, 0 },
                     { -sl / 2, -sl / 2, 0 } };
}

estimate_poses_impl::~estimate_poses_impl() {}

int estimate_poses_impl::work(int noutput_items,
                              gr_vector_const_void_star& input_items,
                              gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);
    auto out = static_cast<uint8_t*>(output_items[0]);
    size_t block_size = output_signature()->sizeof_stream_item(0);
    Mat frame(d_height, d_width, CV_8UC3);

    for (int i = 0; i < noutput_items; i++) {
        std::vector<gr::tag_t> tags;
        get_tags_in_window(tags, 0, 0, i);
        if (tags.size() > 0) {
            std::memcpy(frame.data, &in[i * block_size], block_size);
            std::vector<int> ids =
                boost::any_cast<std::vector<int>>(pmt::any_ref(tags[0].value));
            std::vector<std::vector<Point2f>> corners =
                boost::any_cast<std::vector<std::vector<Point2f>>>(
                    pmt::any_ref(tags[1].value));

            std::vector<Mat> rvecs(ids.size());
            std::vector<Mat> tvecs(ids.size());

            for (size_t k = 0; k < corners.size(); k++) {
                solvePnP(d_marker_pts,
                         corners.at(k),
                         d_cam_mtx,
                         d_dist_coeffs,
                         rvecs.at(k),
                         tvecs.at(k),
                         false,
                         SOLVEPNP_IPPE_SQUARE);
                drawFrameAxes(
                    frame, d_cam_mtx, d_dist_coeffs, rvecs.at(k), tvecs.at(k), 0.1);
            }
        }
        memcpy(&out[i * block_size], &frame.data[0], block_size);
    }


    return noutput_items;
}

} /* namespace medusa */
} /* namespace gr */
