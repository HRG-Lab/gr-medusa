#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: gaylybailey
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import medusa
from sig import sig  # grc-generated hier_block
import mmse_epy_block_0 as epy_block_0  # embedded python block
import numpy as np



from gnuradio import qtgui

class mmse(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "mmse")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.thetas = thetas = np.linspace(-np.pi, np.pi, 361)
        self.soi_angle = soi_angle = (40, 0)
        self.sig_amplitude = sig_amplitude = 1
        self.samp_rate = samp_rate = 100000
        self.phis = phis = np.linspace(0, np.pi, 181)
        self.noise_power = noise_power = 0.1
        self.intf_angle = intf_angle = (-40, 0)
        self.intf_amplitude = intf_amplitude = 0.2
        self.freq = freq = 1000
        self.N = N = 8

        ##################################################
        # Blocks
        ##################################################
        self.sig_0_0 = sig(
            freq=freq,
            n_elems=N,
            noise_power=noise_power,
            samp_rate=samp_rate,
            soi_angle=soi_angle,
        )
        self.sig_0 = sig(
            freq=freq,
            n_elems=N,
            noise_power=noise_power,
            samp_rate=samp_rate,
            soi_angle=intf_angle,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.medusa_calc_steering_vec_0 = medusa.calc_steering_vec(thetas, phis, freq)
        self.medusa_array_plot_3d_0 = medusa.array_plot_3d()
        self._medusa_array_plot_3d_0_win = self.medusa_array_plot_3d_0
        self.top_grid_layout.addWidget(self._medusa_array_plot_3d_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.epy_block_0 = epy_block_0.blk(n_elems=N, freq=freq)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_gr_complex*1, N)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.to_pmt(""), 1000)
        self.blocks_add_xx_0 = blocks.add_vcc(N)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, intf_amplitude, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, sig_amplitude, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_0, 'trigger'))
        self.msg_connect((self.epy_block_0, 'positions'), (self.medusa_array_plot_3d_0, 'positions'))
        self.msg_connect((self.epy_block_0, 'positions'), (self.medusa_calc_steering_vec_0, 'positions'))
        self.msg_connect((self.medusa_calc_steering_vec_0, 'vecs'), (self.sig_0, 'steering_vectors'))
        self.msg_connect((self.medusa_calc_steering_vec_0, 'vecs'), (self.sig_0_0, 'steering_vectors'))
        self.connect((self.analog_sig_source_x_0, 0), (self.sig_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.sig_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_vector_to_streams_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 5), (self.blocks_null_sink_0, 3))
        self.connect((self.blocks_vector_to_streams_0, 4), (self.blocks_null_sink_0, 2))
        self.connect((self.blocks_vector_to_streams_0, 2), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 3), (self.blocks_null_sink_0, 1))
        self.connect((self.blocks_vector_to_streams_0, 6), (self.blocks_null_sink_0, 4))
        self.connect((self.blocks_vector_to_streams_0, 7), (self.blocks_null_sink_0, 5))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 1), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.sig_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.sig_0_0, 0), (self.blocks_add_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "mmse")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_thetas(self):
        return self.thetas

    def set_thetas(self, thetas):
        self.thetas = thetas

    def get_soi_angle(self):
        return self.soi_angle

    def set_soi_angle(self, soi_angle):
        self.soi_angle = soi_angle
        self.sig_0_0.set_soi_angle(self.soi_angle)

    def get_sig_amplitude(self):
        return self.sig_amplitude

    def set_sig_amplitude(self, sig_amplitude):
        self.sig_amplitude = sig_amplitude
        self.analog_sig_source_x_0.set_amplitude(self.sig_amplitude)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.sig_0.set_samp_rate(self.samp_rate)
        self.sig_0_0.set_samp_rate(self.samp_rate)

    def get_phis(self):
        return self.phis

    def set_phis(self, phis):
        self.phis = phis

    def get_noise_power(self):
        return self.noise_power

    def set_noise_power(self, noise_power):
        self.noise_power = noise_power
        self.sig_0.set_noise_power(self.noise_power)
        self.sig_0_0.set_noise_power(self.noise_power)

    def get_intf_angle(self):
        return self.intf_angle

    def set_intf_angle(self, intf_angle):
        self.intf_angle = intf_angle
        self.sig_0.set_soi_angle(self.intf_angle)

    def get_intf_amplitude(self):
        return self.intf_amplitude

    def set_intf_amplitude(self, intf_amplitude):
        self.intf_amplitude = intf_amplitude
        self.analog_sig_source_x_0_0.set_amplitude(self.intf_amplitude)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0.set_frequency(self.freq)
        self.analog_sig_source_x_0_0.set_frequency(self.freq)
        self.epy_block_0.freq = self.freq
        self.sig_0.set_freq(self.freq)
        self.sig_0_0.set_freq(self.freq)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.epy_block_0.n_elems = self.N
        self.sig_0.set_n_elems(self.N)
        self.sig_0_0.set_n_elems(self.N)




def main(top_block_cls=mmse, options=None):

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
