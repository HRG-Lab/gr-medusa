#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: gaylybailey
# GNU Radio version: v3.11.0.0git-528-g9b3183ae

from PyQt5 import Qt
from pyqtgraph.dockarea import Dock, DockArea
from gnuradio import qtgui
from gnuradio import digital
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
from cv2 import aruco
import numpy as np
import random
import test_epy_block_0 as epy_block_0  # embedded python block



class test(gr.top_block, Qt.QMainWindow):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QMainWindow.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)

        self.dockarea = DockArea()
        self.setCentralWidget(self.dockarea)

        # self.top_scroll_layout = Qt.QVBoxLayout()
        # self.setLayout(self.top_scroll_layout)
        # self.top_scroll = Qt.QScrollArea()
        # self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        # self.top_scroll_layout.addWidget(self.top_scroll)
        # self.top_scroll.setWidgetResizable(True)
        # self.top_widget = Qt.QWidget()
        # self.top_scroll.setWidget(self.top_widget)
        # self.top_layout = Qt.QVBoxLayout(self.top_widget)
        # self.top_grid_layout = Qt.QGridLayout()
        # self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "test")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.symbols_per_byte = symbols_per_byte = 4
        self.sps = sps = 4
        self.samp_rate = samp_rate = 2**16
        self.num_elems = num_elems = 32
        self.excess_bw = excess_bw = 0.35
        self.constel = constel = digital.constellation_qpsk().base()
        self.constel.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        self.medusa_qlabel_video_sink_0_0 = _label_video_sink_medusa_qlabel_video_sink_0_0 = medusa.VideoSinkWidget(1280, 720, self)
        self.medusa_qlabel_video_sink_0_0 = medusa.qlabel_video_sink(1280, 720)
        self.medusa_qlabel_video_sink_0_0.newFrame.connect(_label_video_sink_medusa_qlabel_video_sink_0_0.onNewFrame)

        dock = Dock("Widget")
        dock.addWidget(_label_video_sink_medusa_qlabel_video_sink_0_0)
        self.dockarea.addDock(dock)
        self.medusa_positions_to_steering_vecs_0_0 = medusa.positions_to_steering_vecs(0.05, 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], 1)
        self.medusa_plot_3d_positions_0_0 = _3d_plot_medusa_plot_3d_positions_0_0 = medusa.plot_3d_positions(self)
        self.medusa_plot_3d_positions_0_0 = _3d_plot_medusa_plot_3d_positions_0_0

        dock = Dock("Widget")
        dock.addWidget(_3d_plot_medusa_plot_3d_positions_0_0)
        self.dockarea.addDock(dock)
        self.medusa_opencv_aruco_corner_source_0 = medusa.opencv_aruco_corner_source(
            0,
            1280,
            720,
            0,
            0.10,
            '/home/gaylybailey/Documents/Programming/OpenCVSandbox/logitech_brio.yaml',
            True,
            True,
            7.0,
            23,
            3,
            10,
            30,
            0,
            0.1,
            5,
            False,
            0.6,
            1,
            0.35,
            4.0,
            0.05,
            3,
            0.05,
            0.0,
            0.03,
            5.0,
            32,
            0.13,
            4,
            0.03,
            True
        )
        self.epy_block_0 = epy_block_0.msg_blk()


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.medusa_opencv_aruco_corner_source_0, 'frame_info'), (self.medusa_positions_to_steering_vecs_0_0, 'frame_info'))
        self.msg_connect((self.medusa_positions_to_steering_vecs_0_0, 'steering vecs'), (self.epy_block_0, 'msg'))
        self.msg_connect((self.medusa_positions_to_steering_vecs_0_0, 'positions'), (self.medusa_plot_3d_positions_0_0, 'positions'))
        self.connect((self.medusa_opencv_aruco_corner_source_0, 0), (self.medusa_qlabel_video_sink_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbols_per_byte(self):
        return self.symbols_per_byte

    def set_symbols_per_byte(self, symbols_per_byte):
        self.symbols_per_byte = symbols_per_byte

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_num_elems(self):
        return self.num_elems

    def set_num_elems(self, num_elems):
        self.num_elems = num_elems

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_constel(self):
        return self.constel

    def set_constel(self, constel):
        self.constel = constel




def main(top_block_cls=test, options=None):

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
