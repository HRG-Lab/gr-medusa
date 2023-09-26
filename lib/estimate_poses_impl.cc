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

    message_port_register_out(pmt::mp("positions"));
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
            std::vector<uint32_t> ids =pmt::u32vector_elements(tags[0].value);
            std::vector<std::vector<Point2f>> corners;

            corners.resize(pmt::length(tags[1].value));
            for (size_t j=0; j < pmt::length(tags[1].value); j++) {
                corners[j].resize(4);
                pmt::pmt_t four_corners = pmt::vector_ref(tags[1].value, j);
                for (int k=0; k < 4; k++) {
                    pmt::pmt_t point = pmt::vector_ref(four_corners, k);
                    corners[j][k] = Point2f(pmt::to_float(pmt::car(point)), pmt::to_float(pmt::cdr(point)));
                }
            }
            std::vector<Vec3d> rvecs(ids.size()), tvecs(ids.size());

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

            pmt::pmt_t dict = pmt::make_dict();
            dict = pmt::dict_add(dict, pmt::mp("ids"), pmt::init_u32vector(ids.size(), ids));
            pmt::pmt_t rvecs_pmt = pmt::make_vector(rvecs.size(), pmt::PMT_NIL);
            pmt::pmt_t tvecs_pmt = pmt::make_vector(tvecs.size(), pmt::PMT_NIL);
            for (size_t idx=0; idx < rvecs.size(); idx++) {
                double tmp_r[3] = {rvecs[idx][0], rvecs[idx][1], rvecs[idx][2]};
                double tmp_t[3] = {tvecs[idx][0], tvecs[idx][1], tvecs[idx][2]};
                pmt::vector_set(rvecs_pmt, idx, pmt::init_f64vector(3, tmp_r));
                pmt::vector_set(tvecs_pmt, idx, pmt::init_f64vector(3, tmp_t));
            }
            dict = pmt::dict_add(dict, pmt::mp("rvecs"), rvecs_pmt);
            dict = pmt::dict_add(dict, pmt::mp("tvecs"), tvecs_pmt);
            message_port_pub(pmt::mp("positions"), dict);
        }
        memcpy(&out[i * block_size], &frame.data[0], block_size);
    }


    return noutput_items;
}

} /* namespace medusa */
} /* namespace gr */
