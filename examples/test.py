#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: gaylybailey
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import medusa
import numpy as np



class test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 245760000

        ##################################################
        # Blocks
        ##################################################

        self.medusa_qlabel_video_sink_0_0 = _label_video_sink_medusa_qlabel_video_sink_0_0 = medusa.VideoSinkWidget(640, 480, self)
        self.medusa_qlabel_video_sink_0_0 = medusa.qlabel_video_sink(640, 480)
        self.medusa_qlabel_video_sink_0_0.newFrame.connect(_label_video_sink_medusa_qlabel_video_sink_0_0.onNewFrame)

        self.top_grid_layout.addWidget(_label_video_sink_medusa_qlabel_video_sink_0_0, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.medusa_qlabel_video_sink_0 = _label_video_sink_medusa_qlabel_video_sink_0 = medusa.VideoSinkWidget(640, 480, self)
        self.medusa_qlabel_video_sink_0 = medusa.qlabel_video_sink(640, 480)
        self.medusa_qlabel_video_sink_0.newFrame.connect(_label_video_sink_medusa_qlabel_video_sink_0.onNewFrame)

        self.top_grid_layout.addWidget(_label_video_sink_medusa_qlabel_video_sink_0, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.medusa_opencv_source_0 = medusa.opencv_source(0, 640, 480)
        self.medusa_estimate_poses_0 = medusa.estimate_poses('/home/gaylybailey/Documents/Programming/OpenCVSandbox/logitech_brio.yaml', 0.1, 640, 480)
        self.medusa_aruco_detector_0 = medusa.aruco_detector(0, 640, 480)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.medusa_aruco_detector_0, 0), (self.medusa_estimate_poses_0, 0))
        self.connect((self.medusa_aruco_detector_0, 0), (self.medusa_qlabel_video_sink_0_0, 0))
        self.connect((self.medusa_estimate_poses_0, 0), (self.medusa_qlabel_video_sink_0, 0))
        self.connect((self.medusa_opencv_source_0, 0), (self.medusa_aruco_detector_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
