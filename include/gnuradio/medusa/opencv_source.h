/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_OPENCV_SOURCE_H
#define INCLUDED_MEDUSA_OPENCV_SOURCE_H

#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>

#include <gnuradio/medusa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
namespace medusa {

/*!
 * \brief <+description of block+>
 * \ingroup medusa
 *
 */
class MEDUSA_API opencv_source : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<opencv_source> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of medusa::opencv_source.
     *
     * To avoid accidental use of raw pointers, medusa::opencv_source's
     * constructor is in a private implementation
     * class. medusa::opencv_source::make is the public interface for
     * creating new instances.
     */
    static sptr make(int video_source, int width, int height);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_OPENCV_SOURCE_H */
