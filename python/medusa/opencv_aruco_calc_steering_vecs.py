#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import pmt

import cv2 as cv
from cv2 import aruco

from PyQt5.QtCore import QObject, pyqtSignal, QThread


class VideoThreadWorker(QObject):
    newFrame = pyqtSignal(object)

    def __init__(self, video_device, resolution):
        QObject.__init__(self)
        self.video_device = video_device
        self.cap = cv.VideoCapture(self.video_device)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
        if not self.cap.isOpened():
            raise RuntimeError("Couldn't open camera")

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # self.newFrame.emit(np.transpose(frame_rgb, (1, 0, 2)))
            self.newFrame.emit(frame)


class opencv_aruco_calc_steering_vecs(gr.sync_block):
    """
    docstring for block opencv_aruco_calc_steering_vecs
    """

    def __init__(
        self,
        video_source=0,
        calibration_file="",
        dictionary="DICT_4X4_50",
        element_ids=None,
        origin_id=0,
        marker_length=0.05,
        resolution=(640, 480),
        draw_markers=True,
        draw_poses=True,
    ):
        gr.sync_block.__init__(
            self, name="opencv_aruco_calc_steering_vecs", in_sig=None, out_sig=None
        )

        self.video_source = video_source
        self.dictionary = aruco.getPredefinedDictionary(dictionary)
        self.params = aruco.DetectorParameters()
        self.cal_file = cv.FileStorage(calibration_file, flags=cv.FileStorage_READ)
        self.cam_mtx = self.cal_file.getNode("camera_matrix").mat()
        self.dist_coeffs = self.cal_file.getNode("distortion_coefficients").mat()
        self.marker_length = marker_length
        self.marker_pts = np.array(
            [
                [-marker_length / 2, marker_length / 2, 0],
                [marker_length / 2, marker_length / 2, 0],
                [marker_length / 2, -marker_length / 2, 0],
                [-marker_length / 2, -marker_length / 2, 0],
            ],
            dtype=np.float32,
        )
        self.marker_ids = element_ids
        self.origin_id = origin_id
        self.draw_markers = draw_markers
        self.draw_poses = draw_poses

        self.detector = cv.aruco.ArucoDetector(self.dictionary, self.params)

        self.message_port_register_out(pmt.intern("frame"))
        self.message_port_register_out(pmt.intern("positions"))
        self.message_port_register_out(pmt.intern("frame_info"))
        self.message_port_register_out(pmt.intern("steering_vecs"))

        self.thread = QThread()
        self.worker = VideoThreadWorker(video_source, resolution)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.newFrame.connect(self.onNewFrame)

        self.thread.start()

    def onNewFrame(self, frame):
        frame = cv.undistort(frame, self.cam_mtx, self.dist_coeffs)
        # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # corners, ids, rejected = self.detector.detectMarkers(gray)

        # ret = {}
        # if self.draw_markers:
        #     aruco.drawDetectedMarkers(gray, corners, ids)
        # if len(corners) > 0:
        #     for id, c in zip(ids, corners):
        #         _, rvec, tvec = cv.solvePnP(
        #             self.marker_pts,
        #             c,
        #             self.cam_mtx,
        #             self.dist_coeffs,
        #             False,
        #             cv.SOLVEPNP_IPPE_SQUARE,
        #         )
        #         ret[int(id[0])] = {
        #             "rvec": rvec,
        #             "tvec": tvec,
        #         }
        #         if self.draw_poses:
        #             cv.drawFrameAxes(
        #                 frame, self.cam_mtx, self.dist_coeffs, rvec, tvec, 0.075
        #             )

        # frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # info = self.get_vecs_relative_to_origin(ret)

        self.message_port_pub(
            pmt.intern("frame"), pmt.cons(pmt.to_pmt(frame.shape), pmt.to_pmt(frame))
        )
        raise RuntimeError()
        # self.message_port_pub(pmt.intern("frame_info"), pmt.to_pmt(info))

    def positions_to_array(self):
        return np.array([pos for pos in self.positions.values()])

    def handle_positions(self, msg):
        d = pmt.to_python(msg)
        ids = d["ids"]
        rvecs = d["rvecs"]
        tvecs = d["tvecs"]
        markers = self.process(ids, rvecs, tvecs)
        if markers is None:
            return

        markers = [
            m for m in markers if (m.id != self.origin) and (m.id in self.element_ids)
        ]

        if len(markers) == 0:
            return

        for m in markers:
            self.positions[m.id] = m.se3_relative_to_origin.tvec

        all_v = v(self.all_k, self.positions_to_array().T)

        self.message_port_pub(
            pmt.intern("positions"),
            pmt.cons(
                pmt.to_pmt(self.positions_to_array().shape),
                pmt.to_pmt(self.positions_to_array()),
            ),
        )

        self.message_port_pub(
            pmt.intern("steering vecs"),
            pmt.cons(pmt.to_pmt(all_v.shape), pmt.to_pmt(all_v)),
        )

    def process(self, ids, rvecs, tvecs):
        ids = ids.tolist()

        try:
            o_idx = ids.index(self.origin)
        except ValueError:
            return None
        else:
            o = marker.Marker(
                self.origin, self.marker_length, rvecs[o_idx], tvecs[o_idx], origin=None
            )
            ret = [
                marker.Marker(num, self.marker_length, rvec, tvec, o)
                for num, rvec, tvec in zip(ids, rvecs, tvecs)
            ]

        return ret
