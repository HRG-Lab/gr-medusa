/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "aruco_detector_impl.h"
#include <gnuradio/io_signature.h>
#include <opencv2/aruco.hpp>
#include <opencv2/core/hal/interface.h>
#include <opencv2/highgui.hpp>
#include <opencv2/objdetect/aruco_detector.hpp>
#include <opencv2/objdetect/aruco_dictionary.hpp>
#include <pmt/pmt.h>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <stdexcept>

using namespace cv;

namespace gr {
namespace medusa {

aruco_detector::sptr aruco_detector::make(int dictionary, int width, int height)
{
    return gnuradio::make_block_sptr<aruco_detector_impl>(dictionary, width, height);
}


aruco_detector_impl::aruco_detector_impl(int dictionary, int width, int height)
    : gr::sync_block("aruco_detector",
                     gr::io_signature::make(
                         1, 1, width * height * 3 * sizeof(uint8_t)),
                     gr::io_signature::make(
                         1, 1, width * height * 3 * sizeof(uint8_t))),
    d_width(width),
    d_height(height),
    d_dictionary(aruco::getPredefinedDictionary(dictionary)),
    d_params(aruco::DetectorParameters())
{
    d_params.useAruco3Detection = true;
    d_detector = aruco::ArucoDetector(d_dictionary, d_params);
}

aruco_detector_impl::~aruco_detector_impl() {}

int aruco_detector_impl::work(int noutput_items,
                              gr_vector_const_void_star& input_items,
                              gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);
    auto out = static_cast<uint8_t*>(output_items[0]);
    size_t block_size = output_signature()->sizeof_stream_item(0);
    Mat frame(d_height, d_width, CV_8UC3);

    for (int i=0; i < noutput_items; i++) {
        std::memcpy(frame.data, &in[i * block_size], block_size);
        
        std::vector<int> ids;
        std::vector<std::vector<cv::Point2f>> corners, rejected;
        d_detector.detectMarkers(frame, corners, ids, rejected);

        std::vector<uint32_t> ids_to_send(ids.begin(), ids.end());
        pmt::pmt_t corners_pmt = pmt::make_vector(corners.size(), pmt::PMT_NIL);

        if (ids.size() > 0) {
            pmt::pmt_t ids_pmt = pmt::init_u32vector(ids.size(), ids_to_send);
            for (size_t j=0; j < ids.size(); j++) {
                auto marker = corners.at(j);
                auto marker_pmt = pmt::make_vector(4, pmt::PMT_NIL);
                for (int k=0; k < 4; k++) {
                    auto corner = marker.at(k);
                    pmt::vector_set(marker_pmt, k, pmt::cons(pmt::mp(corner.x), pmt::mp(corner.y)));
                }
                pmt::vector_set(corners_pmt, j, marker_pmt);
            }
            add_item_tag(0, nitems_written(0), pmt::intern("ids"), ids_pmt);
            add_item_tag(0, nitems_written(0), pmt::intern("corners"), corners_pmt);

            cv::aruco::drawDetectedMarkers(frame, corners, ids);
        }

        memcpy(&out[i*block_size], &frame.data[0], block_size);
    }

    return noutput_items;
}

} /* namespace medusa */
} /* namespace gr */
