/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "opencv_source_impl.h"
#include <gnuradio/io_signature.h>
#include <cstdint>
#include <stdexcept>
#include <iostream>
#include <string>

namespace gr {
namespace medusa {

opencv_source::sptr opencv_source::make(int video_source, int width, int height)
{
    return gnuradio::make_block_sptr<opencv_source_impl>(video_source, width, height);
}

opencv_source_impl::opencv_source_impl(int video_source, int width, int height)
    : gr::sync_block("OpenCV Source",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(
                         1, 1, width * height * 3 * sizeof(uint8_t))),
    d_width(width),
    d_height(height),
    d_len(width*height*3)
{
    d_video.open(video_source);
    if (!d_video.isOpened())
        throw std::runtime_error("Failed to open camera");

    d_video.set(cv::CAP_PROP_FRAME_WIDTH, width);
    d_video.set(cv::CAP_PROP_FRAME_HEIGHT, height);

    int actual_width = d_video.get(cv::CAP_PROP_FRAME_WIDTH);
    int actual_height = d_video.get(cv::CAP_PROP_FRAME_HEIGHT);
    if ((width != actual_width) || (height != actual_height)) {
        throw std::runtime_error("Camera does not support specified resolution. It automatically set itself to " + std::to_string(actual_width) + "x" + std::to_string(actual_height));
    }

    d_video.set(cv::CAP_PROP_FPS, 30);
    std::cout << "Framerate: " << d_video.get(cv::CAP_PROP_FPS) << std::endl;
}

opencv_source_impl::~opencv_source_impl() {}

int opencv_source_impl::work(int noutput_items,
                                 gr_vector_const_void_star& input_items,
                                 gr_vector_void_star& output_items)
{
    size_t block_size = output_signature()->sizeof_stream_item(0);
    uint8_t* out = reinterpret_cast<uint8_t*>(output_items[0]);
    Mat frames[noutput_items];

    for (int i=0; i < noutput_items; i++) {
        d_video >> frames[i];
        if (frames[i].empty())
            throw std::runtime_error("Stream broken");
        memcpy(&out[i*d_len], &frames[i].data[0], block_size);
    }

    return noutput_items;
}

} /* namespace medusa */
} /* namespace gr */
