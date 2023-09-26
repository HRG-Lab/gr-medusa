/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_OPENCV_ARUCO_CORNER_SOURCE_H
#define INCLUDED_MEDUSA_OPENCV_ARUCO_CORNER_SOURCE_H

#include <opencv2/aruco.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>

#include <gnuradio/medusa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
namespace medusa {

class MEDUSA_API opencv_aruco_corner_source : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<opencv_aruco_corner_source> sptr;

    static sptr make(int video_source,
                     int width,
                     int height,
                     int dictionary,
                     float marker_side_length,
                     std::string calibration_file,
                     bool draw_markers,
                     bool draw_poses,
                     double adaptiveThreshConstant,
                     int adaptiveThreshWinSizeMax,
                     int adaptiveThreshWinSizeMin,
                     int adaptiveThreshWinSizeStep,
                     int cornerRefinementMaxIterations,
                     int cornerRefinementMethod,
                     double cornerRefinementMinAccuracy,
                     int cornerRefinementWinSize,
                     bool detectInvertedMarker,
                     double errorCorrectionRate,
                     int markerBorderBits,
                     double maxErroneousBitsInBorderRate,
                     double maxMarkerPerimeterRate,
                     double minCornerDistanceRate,
                     int minDistanceToBorder,
                     double minMarkerDistanceRate,
                     float minMarkerLengthRatioOriginalImg,
                     double minMarkerPerimeterRate,
                     double minOtsuStdDev,
                     int minSideLengthCanonicalImg,
                     double perspectiveRemoveIgnoredMarginPerCell,
                     double perspectiveRemovePixelPerCell,
                     double polygonalApproxAccuracyRate,
                     bool useAruco3Detection
                     );
};

} // namespace medusa
} // namespace gr


#endif /* INCLUDED_MEDUSA_OPENCV_ARUCO_CORNER_SOURCE_H */
