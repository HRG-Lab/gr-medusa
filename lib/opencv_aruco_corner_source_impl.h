/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_OPENCV_ARUCO_CORNER_SOURCE_IMPL_H
#define INCLUDED_MEDUSA_OPENCV_ARUCO_CORNER_SOURCE_IMPL_H

#include <gnuradio/medusa/opencv_aruco_corner_source.h>

namespace gr {
namespace medusa {

class opencv_aruco_corner_source_impl : public opencv_aruco_corner_source
{
private:
    int d_width;
    int d_height;

    float d_marker_side_length;
    std::vector<cv::Point3f> d_marker_pts;
    cv::Mat d_cam_mtx;
    cv::Mat d_dist_coeffs;

    bool d_draw_markers;
    bool d_draw_poses;

    cv::VideoCapture d_video_source;
    cv::aruco::Dictionary d_dictionary;
    cv::aruco::DetectorParameters d_params;
    cv::aruco::ArucoDetector d_detector;

public:
    opencv_aruco_corner_source_impl(int video_source,
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
                                    bool useAruco3Detection);
    ~opencv_aruco_corner_source_impl();

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_OPENCV_ARUCO_CORNER_SOURCE_IMPL_H */
