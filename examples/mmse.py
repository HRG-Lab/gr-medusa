#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: MMSE Beamforming
# Author: gaylybailey
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
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
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import default_epy_block_0 as epy_block_0  # embedded python block
import numpy as np
import random
import sip



class mmse(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "MMSE Beamforming", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("MMSE Beamforming")
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

        self.settings = Qt.QSettings("GNU Radio", "mmse")

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
        self.sps = sps = 4
        self.excess_bw = excess_bw = 0.35
        self.constel = constel = digital.constellation_qpsk().base()
        self.rxmod = rxmod = digital.generic_mod(constel, False, sps, True, excess_bw, False, False)
        self.preamble = preamble = [0x27,0x2F,0x18,0x5D,0x5B,0x2A,0x3F,0x71,0x63,0x3C,0x17,0x0C,0x0A,0x41,0xD6,0x1F,0x4C,0x23,0x65,0x68,0xED,0x1C,0x77,0xA7,0x0E,0x0A,0x9E,0x47,0x82,0xA4,0x57,0x24,]
        self.modulated_sync_word_pre = modulated_sync_word_pre = digital.modulate_vector_bc(rxmod.to_basic_block(),  preamble+preamble, [1])
        self.modulated_sync_word = modulated_sync_word = modulated_sync_word_pre[86:(512+86)]
        self.payload_size = payload_size = 992
        self.corr_thresh = corr_thresh = 3e6
        self.corr_max = corr_max = np.abs(np.dot(modulated_sync_word,np.conj(modulated_sync_word)))
        self.symbols_per_byte = symbols_per_byte = 4
        self.samp_rate = samp_rate = 32000
        self.gap = gap = 20000
        self.data = data = [0]*4+[random.getrandbits(8) for i in range(payload_size)]
        self.corr_calc = corr_calc = corr_thresh/(corr_max*corr_max)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            80000, #size
            1, #samp_rate
            "", #name
            4, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'black', 'cyan', 'magenta',
            'yellow', 'dark red', 'dark green', 'dark green', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, 1, 1]


        for i in range(8):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 4, 0, 4, 1)
        for r in range(4, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            80000, #size
            1, #samp_rate
            'Correlation Squared Magnitude', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', 'Squared Magnitude')

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.epy_block_0 = epy_block_0.ula_sim(num_elements=, sep_lambda=, angle_degrees=, log_response=)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(modulated_sync_word, sps, 1, corr_calc, digital.THRESHOLD_ABSOLUTE)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=constel,
            differential=False,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self._corr_thresh_range = Range(0.1, 5e6, 1.0, 3e6, 200)
        self._corr_thresh_win = RangeWidget(self._corr_thresh_range, self.set_corr_thresh, "Absolute Corr Thresh (Mag Sq)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._corr_thresh_win)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_gr_complex*1, 4)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b(preamble+data, True, 1, [])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, ((len(preamble)+len(data))*symbols_per_byte*sps, gap-(len(preamble)+len(data))*symbols_per_byte*sps))
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, 86)
        self.blocks_null_source_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, len(modulated_sync_word))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_delay_0, 1), (self.qtgui_time_sink_x_1, 2))
        self.connect((self.blocks_delay_0, 2), (self.qtgui_time_sink_x_1, 3))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.blocks_null_source_0_0, 0), (self.blocks_stream_mux_0_0, 1))
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_stream_mux_0_0, 0))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 3), (self.blocks_delay_0, 2))
        self.connect((self.blocks_vector_to_streams_0, 1), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 2), (self.blocks_delay_0, 1))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.digital_corr_est_cc_0, 1), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_vector_to_streams_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "mmse")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rxmod(digital.generic_mod(self.constel, False, self.sps, True, self.excess_bw, False, False))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rxmod(digital.generic_mod(self.constel, False, self.sps, True, self.excess_bw, False, False))

    def get_constel(self):
        return self.constel

    def set_constel(self, constel):
        self.constel = constel
        self.set_rxmod(digital.generic_mod(self.constel, False, self.sps, True, self.excess_bw, False, False))

    def get_rxmod(self):
        return self.rxmod

    def set_rxmod(self, rxmod):
        self.rxmod = rxmod

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.blocks_vector_source_x_0_0.set_data(self.preamble+self.data, [])

    def get_modulated_sync_word_pre(self):
        return self.modulated_sync_word_pre

    def set_modulated_sync_word_pre(self, modulated_sync_word_pre):
        self.modulated_sync_word_pre = modulated_sync_word_pre
        self.set_modulated_sync_word(self.modulated_sync_word_pre[86:(512+86)])

    def get_modulated_sync_word(self):
        return self.modulated_sync_word

    def set_modulated_sync_word(self, modulated_sync_word):
        self.modulated_sync_word = modulated_sync_word
        self.set_corr_max(np.abs(np.dot(self.modulated_sync_word,np.conj(self.modulated_sync_word))))
        self.blocks_delay_0.set_dly(int(len(self.modulated_sync_word)))

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size
        self.set_data([0]*4+[random.getrandbits(8) for i in range(self.payload_size)])

    def get_corr_thresh(self):
        return self.corr_thresh

    def set_corr_thresh(self, corr_thresh):
        self.corr_thresh = corr_thresh
        self.set_corr_calc(self.corr_thresh/(self.corr_max*self.corr_max))

    def get_corr_max(self):
        return self.corr_max

    def set_corr_max(self, corr_max):
        self.corr_max = corr_max
        self.set_corr_calc(self.corr_thresh/(self.corr_max*self.corr_max))

    def get_symbols_per_byte(self):
        return self.symbols_per_byte

    def set_symbols_per_byte(self, symbols_per_byte):
        self.symbols_per_byte = symbols_per_byte

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_gap(self):
        return self.gap

    def set_gap(self, gap):
        self.gap = gap

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.blocks_vector_source_x_0_0.set_data(self.preamble+self.data, [])

    def get_corr_calc(self):
        return self.corr_calc

    def set_corr_calc(self, corr_calc):
        self.corr_calc = corr_calc
        self.digital_corr_est_cc_0.set_threshold(self.corr_calc)




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
