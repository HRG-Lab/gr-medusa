/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "opencv_aruco_corner_source_impl.h"
#include <gnuradio/io_signature.h>
#include <pmt/pmt.h>
#include <stdexcept>

namespace gr {
namespace medusa {

opencv_aruco_corner_source::sptr
opencv_aruco_corner_source::make(int video_source,
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
                                 bool useAruco3Detection)
{
    return gnuradio::make_block_sptr<opencv_aruco_corner_source_impl>(
        video_source,
        width,
        height,
        dictionary,
        marker_side_length,
        calibration_file,
        draw_markers,
        draw_poses,
        adaptiveThreshConstant,
        adaptiveThreshWinSizeMax,
        adaptiveThreshWinSizeMin,
        adaptiveThreshWinSizeStep,
        cornerRefinementMaxIterations,
        cornerRefinementMethod,
        cornerRefinementMinAccuracy,
        cornerRefinementWinSize,
        detectInvertedMarker,
        errorCorrectionRate,
        markerBorderBits,
        maxErroneousBitsInBorderRate,
        maxMarkerPerimeterRate,
        minCornerDistanceRate,
        minDistanceToBorder,
        minMarkerDistanceRate,
        minMarkerLengthRatioOriginalImg,
        minMarkerPerimeterRate,
        minOtsuStdDev,
        minSideLengthCanonicalImg,
        perspectiveRemoveIgnoredMarginPerCell,
        perspectiveRemovePixelPerCell,
        polygonalApproxAccuracyRate,
        useAruco3Detection);
}


opencv_aruco_corner_source_impl::opencv_aruco_corner_source_impl(
    int video_source,
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
    bool useAruco3Detection)
    : gr::sync_block("opencv_aruco_corner_source",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(1, 1, width * height * 3)),
      d_width(width),
      d_height(height),
      d_marker_side_length(marker_side_length),
      d_draw_markers(draw_markers),
      d_draw_poses(draw_poses)
{
    d_params = cv::aruco::DetectorParameters();
    d_params.adaptiveThreshConstant = adaptiveThreshConstant;
    d_params.adaptiveThreshWinSizeMax = adaptiveThreshWinSizeMax;
    d_params.adaptiveThreshWinSizeMin = adaptiveThreshWinSizeMin;
    d_params.adaptiveThreshWinSizeStep = adaptiveThreshWinSizeStep;
    d_params.cornerRefinementMaxIterations = cornerRefinementMaxIterations;
    d_params.cornerRefinementMethod =
        cv::aruco::CornerRefineMethod(cornerRefinementMethod);
    d_params.cornerRefinementMinAccuracy = cornerRefinementMinAccuracy;
    d_params.cornerRefinementWinSize = cornerRefinementWinSize;
    d_params.detectInvertedMarker = detectInvertedMarker;
    d_params.errorCorrectionRate = errorCorrectionRate;
    d_params.markerBorderBits = markerBorderBits;
    d_params.maxErroneousBitsInBorderRate = maxErroneousBitsInBorderRate;
    d_params.maxMarkerPerimeterRate = maxMarkerPerimeterRate;
    d_params.minCornerDistanceRate = minCornerDistanceRate;
    d_params.minDistanceToBorder = minDistanceToBorder;
    d_params.minMarkerDistanceRate = minMarkerDistanceRate;
    d_params.minMarkerLengthRatioOriginalImg = minMarkerLengthRatioOriginalImg;
    d_params.minMarkerPerimeterRate = minMarkerPerimeterRate;
    d_params.minOtsuStdDev = minOtsuStdDev;
    d_params.minSideLengthCanonicalImg = minSideLengthCanonicalImg;
    d_params.perspectiveRemoveIgnoredMarginPerCell =
        perspectiveRemoveIgnoredMarginPerCell;
    d_params.perspectiveRemovePixelPerCell = perspectiveRemovePixelPerCell;
    d_params.polygonalApproxAccuracyRate = polygonalApproxAccuracyRate;
    d_params.useAruco3Detection = useAruco3Detection;

    d_video_source = cv::VideoCapture(video_source);
    d_dictionary = cv::aruco::getPredefinedDictionary(dictionary);
    d_detector = cv::aruco::ArucoDetector(d_dictionary, d_params);

    cv::FileStorage cal_file(calibration_file, cv::FileStorage::Mode::READ);
    cal_file["camera_matrix"] >> d_cam_mtx;
    cal_file["distortion_coefficients"] >> d_dist_coeffs;

    float sl = d_marker_side_length;
    d_marker_pts = { { -sl / 2, sl / 2, 0 },
                     { sl / 2, sl / 2, 0 },
                     { sl / 2, -sl / 2, 0 },
                     { -sl / 2, -sl / 2, 0 } };

    d_video_source.open(video_source);
    if (!d_video_source.isOpened())
        throw std::runtime_error("Failed to open camera");

    d_video_source.set(cv::CAP_PROP_FRAME_WIDTH, width);
    d_video_source.set(cv::CAP_PROP_FRAME_HEIGHT, height);

    int actual_width = d_video_source.get(cv::CAP_PROP_FRAME_WIDTH);
    int actual_height = d_video_source.get(cv::CAP_PROP_FRAME_HEIGHT);
    if ((width != actual_width) || (height != actual_height)) {
        throw std::runtime_error("Camera does not support specified resolution. It "
                                 "automatically set itself to " +
                                 std::to_string(actual_width) + "x" +
                                 std::to_string(actual_height));
    }

    d_video_source.set(cv::CAP_PROP_FPS, 30);
    std::cout << "Framerate: " << d_video_source.get(cv::CAP_PROP_FPS) << std::endl;

    message_port_register_out(pmt::mp("frame_info"));
}

opencv_aruco_corner_source_impl::~opencv_aruco_corner_source_impl() {}

int opencv_aruco_corner_source_impl::work(int noutput_items,
                                          gr_vector_const_void_star& input_items,
                                          gr_vector_void_star& output_items)
{
    size_t block_size = output_signature()->sizeof_stream_item(0);
    uint8_t* out_frame = reinterpret_cast<uint8_t*>(output_items[0]);
    cv::Mat frames[noutput_items];

    std::vector<int32_t> ids;
    std::vector<std::vector<cv::Point2f>> corners, rejected;

    for (int i = 0; i < noutput_items; i++) {
        d_video_source >> frames[i];

        if (frames[i].empty())
            throw std::runtime_error("Stream broken");

        d_detector.detectMarkers(frames[i], corners, ids, rejected);
        if (d_draw_markers)
            cv::aruco::drawDetectedMarkers(frames[i], corners, ids);

        int nMarkers = corners.size();
        std::vector<cv::Vec3d> rvecs(nMarkers), tvecs(nMarkers);

        for (int j = 0; j < nMarkers; j++) {
            cv::solvePnP(d_marker_pts,
                         corners.at(j),
                         d_cam_mtx,
                         d_dist_coeffs,
                         rvecs.at(j),
                         tvecs.at(j),
                         false,
                         cv::SOLVEPNP_IPPE_SQUARE);
        }

        if (d_draw_poses) {
            for (size_t j = 0; j < rvecs.size(); j++)
                cv::drawFrameAxes(
                    frames[i], d_cam_mtx, d_dist_coeffs, rvecs.at(j), tvecs.at(j), 0.05);
        }

        pmt::pmt_t frame_info = pmt::make_dict();
        pmt::pmt_t ids_pmt = pmt::init_s32vector(ids.size(), ids.data());
        pmt::pmt_t rvecs_pmt = pmt::make_vector(rvecs.size(), pmt::PMT_NIL);
        pmt::pmt_t tvecs_pmt = pmt::make_vector(tvecs.size(), pmt::PMT_NIL);
        for (size_t idx=0; idx < rvecs.size(); idx++) {
            double tmp_r[3] = {rvecs[idx][0], rvecs[idx][1], rvecs[idx][2]};
            double tmp_t[3] = {tvecs[idx][0], tvecs[idx][1], tvecs[idx][2]};
            pmt::vector_set(rvecs_pmt, idx, pmt::init_f64vector(3, tmp_r));
            pmt::vector_set(tvecs_pmt, idx, pmt::init_f64vector(3, tmp_t));
        }

        frame_info = pmt::dict_add(frame_info, pmt::mp("ids"), ids_pmt);
        frame_info = pmt::dict_add(frame_info, pmt::mp("rvecs"), rvecs_pmt);
        frame_info = pmt::dict_add(frame_info, pmt::mp("tvecs"), tvecs_pmt);

        message_port_pub(pmt::mp("frame_info"), frame_info);
        memcpy(&out_frame[i * block_size], &frames[i].data[0], block_size);
    }

    return noutput_items;
}

} /* namespace medusa */
} /* namespace gr */
