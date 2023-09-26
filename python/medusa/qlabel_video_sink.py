#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy, QApplication


from gnuradio import gr
import pmt


class VideoSinkWidget(QLabel):
    def __init__(self, width, height, parent=None):
        QLabel.__init__(self)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignCenter)

        self.width = width
        self.height = height
        self.len = width * height * 3

    def onNewFrame(self, frame):
        img = QImage(
            frame.data,
            self.width,
            self.height,
            self.width * 3,
            QImage.Format_BGR888,
        )
        pixmap = QPixmap.fromImage(img)
        self.setPixmap(
            pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


class qlabel_video_sink(gr.sync_block, QObject):
    """
    docstring for block qlabel_video_sink
    """

    newFrame = pyqtSignal(object)

    def __init__(self, width, height):
        gr.sync_block.__init__(
            self,
            name="QLabel Video Sink",
            in_sig=[(np.uint8, width * height * 3)],
            out_sig=None,
        )
        QObject.__init__(self)

        self.width = width
        self.height = height
        self.len = width * height * 3

    def work(self, input_items, output_items):
        frames = [f for f in input_items[0] if len(f) == self.len]
        for frame in frames:
            self.newFrame.emit(frame)

        return len(input_items[0])
