/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_OPENCV_SOURCE_IMPL_H
#define INCLUDED_MEDUSA_OPENCV_SOURCE_IMPL_H

#include <gnuradio/medusa/opencv_source.h>

using namespace cv;

namespace gr {
namespace medusa {

class opencv_source_impl : public opencv_source
{

private:
    VideoCapture d_video;
    int d_width;
    int d_height;
    size_t d_len;

public:
    opencv_source_impl(int video_source, int width, int height);
    ~opencv_source_impl();

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_OPENCV_SOURCE_IMPL_H */
