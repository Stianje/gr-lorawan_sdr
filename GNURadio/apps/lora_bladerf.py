#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lora Bladerf
# Author: Tapparel Joachim@EPFL,TCL
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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading
import gnuradio.lora_sdr as lora_sdr
import numpy as np
import osmosdr
import time



from gnuradio import qtgui

class lora_bladerf(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lora Bladerf", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lora Bladerf")
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

        self.settings = Qt.QSettings("GNU Radio", "lora_bladerf")

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
        self.soft_decoding = soft_decoding = True
        self.sink_sf2 = sink_sf2 = 7
        self.sink_freq2 = sink_freq2 = 868100000
        self.sf = sf = 12
        self.samp_rate = samp_rate = 2000000
        self.pay_len = pay_len = 11
        self.impl_head = impl_head = False
        self.has_crc = has_crc = False
        self.cr = cr = 1
        self.center_freq = center_freq = 868100000.0
        self.bw = bw = 125000

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0_1 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5559', 100, False, -1)
        self.zeromq_push_sink_0_0_1 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5560', 100, False, -1)
        self.zeromq_push_sink_0_0_0_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5558', 100, False, -1)
        self.zeromq_push_sink_0_0_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5561', 100, False, -1)
        self.zeromq_push_sink_0_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5557', 100, False, -1)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5556', 100, False, -1)
        self.zeromq_pull_source_0_0 = zeromq.pull_source(gr.sizeof_char, 1, 'tcp://127.0.0.1:5554', 100, False, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_char, 1, 'tcp://127.0.0.1:5555', 100, False, -1)
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8089), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            2000000, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            2000000, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_win)
        self.osmosdr_source_1 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'bladerf=0'
        )
        self.osmosdr_source_1.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_1.set_sample_rate(2000000)
        self.osmosdr_source_1.set_center_freq(868000000, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(False, 0)
        self.osmosdr_source_1.set_gain(10, 0)
        self.osmosdr_source_1.set_if_gain(20, 0)
        self.osmosdr_source_1.set_bb_gain(20, 0)
        self.osmosdr_source_1.set_antenna('', 0)
        self.osmosdr_source_1.set_bandwidth(2000000, 0)
        self.osmosdr_sink_0_0_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + 'bladerf=0'
        )
        self.osmosdr_sink_0_0_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0_0_0.set_sample_rate(2000000)
        self.osmosdr_sink_0_0_0.set_center_freq(sink_freq2, 0)
        self.osmosdr_sink_0_0_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0_0_0.set_gain(10, 0)
        self.osmosdr_sink_0_0_0.set_if_gain(20, 0)
        self.osmosdr_sink_0_0_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0_0_0.set_antenna('', 0)
        self.osmosdr_sink_0_0_0.set_bandwidth(bw, 0)
        self.osmosdr_sink_0_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + 'bladerf=0'
        )
        self.osmosdr_sink_0_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0_0.set_sample_rate(2000000)
        self.osmosdr_sink_0_0.set_center_freq(sink_freq2, 0)
        self.osmosdr_sink_0_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0_0.set_gain(10, 0)
        self.osmosdr_sink_0_0.set_if_gain(20, 0)
        self.osmosdr_sink_0_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0_0.set_antenna('', 0)
        self.osmosdr_sink_0_0.set_bandwidth(bw, 0)
        self.low_pass_filter_0_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                1000000,
                77500,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0_0.set_min_output_buffer(65568)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                1000000,
                77500,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0.set_min_output_buffer(65568)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                1000000,
                77500,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0.set_min_output_buffer(65568)
        self.lora_sdr_whitening_0_0 = lora_sdr.whitening(True,',')
        self.lora_sdr_whitening_0 = lora_sdr.whitening(True,',')
        self.lora_sdr_modulate_0_0 = lora_sdr.modulate(sf, 2000000, bw, [0x34], int(20*2**sf*samp_rate/bw),8)
        self.lora_sdr_modulate_0 = lora_sdr.modulate(sink_sf2, 2000000, bw, [0x34], int(20*2**sink_sf2*samp_rate/bw),8)
        self.lora_sdr_interleaver_0_0 = lora_sdr.interleaver(cr, sf, 2, bw)
        self.lora_sdr_interleaver_0 = lora_sdr.interleaver(cr, sink_sf2, 2, bw)
        self.lora_sdr_header_decoder_0_1 = lora_sdr.header_decoder(impl_head, 3, 255, False, 2, False)
        self.lora_sdr_header_decoder_0_0_1 = lora_sdr.header_decoder(impl_head, 3, 255, False, 2, False)
        self.lora_sdr_header_decoder_0_0_0_0 = lora_sdr.header_decoder(impl_head, 3, 255, False, 2, True)
        self.lora_sdr_header_decoder_0_0_0 = lora_sdr.header_decoder(impl_head, 3, 255, False, 2, False)
        self.lora_sdr_header_decoder_0_0 = lora_sdr.header_decoder(impl_head, 3, 255, False, 2, True)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(impl_head, 3, 255, False, 2, True)
        self.lora_sdr_header_0_0 = lora_sdr.header(False, False, cr)
        self.lora_sdr_header_0 = lora_sdr.header(False, False, cr)
        self.lora_sdr_hamming_enc_0_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_hamming_enc_0 = lora_sdr.hamming_enc(cr, sink_sf2)
        self.lora_sdr_hamming_dec_0_1 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_hamming_dec_0_0_1 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_hamming_dec_0_0_0_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_hamming_dec_0_0_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_hamming_dec_0_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(soft_decoding)
        self.lora_sdr_gray_mapping_0_1 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_mapping_0_0_1 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_mapping_0_0_0_0 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_mapping_0_0_0 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_mapping_0_0 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping( soft_decoding)
        self.lora_sdr_gray_demap_0_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_gray_demap_0 = lora_sdr.gray_demap(sink_sf2)
        self.lora_sdr_frame_sync_0_1 = lora_sdr.frame_sync(868000000, 125000, 7, impl_head, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_0_1 = lora_sdr.frame_sync(868000000, bw, 7, impl_head, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_0_0_0 = lora_sdr.frame_sync(868000000, bw, 12, impl_head, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_0_0 = lora_sdr.frame_sync(868000000, bw, 7, impl_head, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_0 = lora_sdr.frame_sync(868000000, bw, 12, impl_head, [0x34], 16,8)
        self.lora_sdr_frame_sync_0 = lora_sdr.frame_sync(868000000, 125000, 12, impl_head, [0x34], 16,8)
        self.lora_sdr_fft_demod_0_1 = lora_sdr.fft_demod( soft_decoding, True)
        self.lora_sdr_fft_demod_0_0_1 = lora_sdr.fft_demod( soft_decoding, True)
        self.lora_sdr_fft_demod_0_0_0_0 = lora_sdr.fft_demod( soft_decoding, True)
        self.lora_sdr_fft_demod_0_0_0 = lora_sdr.fft_demod( soft_decoding, True)
        self.lora_sdr_fft_demod_0_0 = lora_sdr.fft_demod( soft_decoding, True)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod( soft_decoding, True)
        self.lora_sdr_dewhitening_0_1 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_0_1 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_0_0_0 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_0_0 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_0 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0_1 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_deinterleaver_0_0_1 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_deinterleaver_0_0_0_0 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_deinterleaver_0_0_0 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_deinterleaver_0_0 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver( soft_decoding)
        self.lora_sdr_crc_verif_0_1 = lora_sdr.crc_verif( False, False)
        self.lora_sdr_crc_verif_0_0_1 = lora_sdr.crc_verif( False, False)
        self.lora_sdr_crc_verif_0_0_0_0 = lora_sdr.crc_verif( True, False)
        self.lora_sdr_crc_verif_0_0_0 = lora_sdr.crc_verif( False, False)
        self.lora_sdr_crc_verif_0_0 = lora_sdr.crc_verif( True, False)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif( True, False)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0_0.set_min_output_buffer(65568)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0.set_min_output_buffer(65568)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0.set_min_output_buffer(65568)
        self.blocks_conjugate_cc_0_0 = blocks.conjugate_cc()
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -500000, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -300000, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -100000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_frame_sync_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_0, 'frame_info'), (self.lora_sdr_frame_sync_0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_0_0, 'frame_info'), (self.lora_sdr_frame_sync_0_0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_0_0_0, 'frame_info'), (self.lora_sdr_frame_sync_0_0_0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_0_1, 'frame_info'), (self.lora_sdr_frame_sync_0_0_1, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_1, 'frame_info'), (self.lora_sdr_frame_sync_0_1, 'frame_info'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.osmosdr_sink_0_0, 0))
        self.connect((self.blocks_conjugate_cc_0_0, 0), (self.osmosdr_sink_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.lora_sdr_crc_verif_0, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_0, 0), (self.zeromq_push_sink_0_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_0_0, 0), (self.zeromq_push_sink_0_0_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_0_0_0, 0), (self.zeromq_push_sink_0_0_0_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_0_1, 0), (self.zeromq_push_sink_0_0_1, 0))
        self.connect((self.lora_sdr_crc_verif_0_1, 0), (self.zeromq_push_sink_0_1, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_0, 0), (self.lora_sdr_hamming_dec_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_0_0, 0), (self.lora_sdr_hamming_dec_0_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_0_0_0, 0), (self.lora_sdr_hamming_dec_0_0_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_0_1, 0), (self.lora_sdr_hamming_dec_0_0_1, 0))
        self.connect((self.lora_sdr_deinterleaver_0_1, 0), (self.lora_sdr_hamming_dec_0_1, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_0, 0), (self.lora_sdr_crc_verif_0_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_0_0, 0), (self.lora_sdr_crc_verif_0_0_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_0_0_0, 0), (self.lora_sdr_crc_verif_0_0_0_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_0_1, 0), (self.lora_sdr_crc_verif_0_0_1, 0))
        self.connect((self.lora_sdr_dewhitening_0_1, 0), (self.lora_sdr_crc_verif_0_1, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_mapping_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_0, 0), (self.lora_sdr_gray_mapping_0_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_0_0, 0), (self.lora_sdr_gray_mapping_0_0_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_0_0_0, 0), (self.lora_sdr_gray_mapping_0_0_0_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_0_1, 0), (self.lora_sdr_gray_mapping_0_0_1, 0))
        self.connect((self.lora_sdr_fft_demod_0_1, 0), (self.lora_sdr_gray_mapping_0_1, 0))
        self.connect((self.lora_sdr_frame_sync_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_0, 0), (self.lora_sdr_fft_demod_0_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_0_0, 0), (self.lora_sdr_fft_demod_0_0_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_0_0_0, 0), (self.lora_sdr_fft_demod_0_0_0_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_0_1, 0), (self.lora_sdr_fft_demod_0_0_1, 0))
        self.connect((self.lora_sdr_frame_sync_0_1, 0), (self.lora_sdr_fft_demod_0_1, 0))
        self.connect((self.lora_sdr_gray_demap_0, 0), (self.lora_sdr_modulate_0, 0))
        self.connect((self.lora_sdr_gray_demap_0_0, 0), (self.lora_sdr_modulate_0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_0, 0), (self.lora_sdr_deinterleaver_0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_0_0, 0), (self.lora_sdr_deinterleaver_0_0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_0_0_0, 0), (self.lora_sdr_deinterleaver_0_0_0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_0_1, 0), (self.lora_sdr_deinterleaver_0_0_1, 0))
        self.connect((self.lora_sdr_gray_mapping_0_1, 0), (self.lora_sdr_deinterleaver_0_1, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_0, 0), (self.lora_sdr_header_decoder_0_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_0_0, 0), (self.lora_sdr_header_decoder_0_0_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_0_0_0, 0), (self.lora_sdr_header_decoder_0_0_0_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_0_1, 0), (self.lora_sdr_header_decoder_0_0_1, 0))
        self.connect((self.lora_sdr_hamming_dec_0_1, 0), (self.lora_sdr_header_decoder_0_1, 0))
        self.connect((self.lora_sdr_hamming_enc_0, 0), (self.lora_sdr_interleaver_0, 0))
        self.connect((self.lora_sdr_hamming_enc_0_0, 0), (self.lora_sdr_interleaver_0_0, 0))
        self.connect((self.lora_sdr_header_0, 0), (self.lora_sdr_hamming_enc_0, 0))
        self.connect((self.lora_sdr_header_0_0, 0), (self.lora_sdr_hamming_enc_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_0, 0), (self.lora_sdr_dewhitening_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_0_0, 0), (self.lora_sdr_dewhitening_0_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_0_0_0, 0), (self.lora_sdr_dewhitening_0_0_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_0_1, 0), (self.lora_sdr_dewhitening_0_0_1, 0))
        self.connect((self.lora_sdr_header_decoder_0_1, 0), (self.lora_sdr_dewhitening_0_1, 0))
        self.connect((self.lora_sdr_interleaver_0, 0), (self.lora_sdr_gray_demap_0, 0))
        self.connect((self.lora_sdr_interleaver_0_0, 0), (self.lora_sdr_gray_demap_0_0, 0))
        self.connect((self.lora_sdr_modulate_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.lora_sdr_modulate_0_0, 0), (self.blocks_conjugate_cc_0_0, 0))
        self.connect((self.lora_sdr_whitening_0, 0), (self.lora_sdr_header_0, 0))
        self.connect((self.lora_sdr_whitening_0_0, 0), (self.lora_sdr_header_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.lora_sdr_frame_sync_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.lora_sdr_frame_sync_0_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.lora_sdr_frame_sync_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.lora_sdr_frame_sync_0_0_1, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.lora_sdr_frame_sync_0_0_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.lora_sdr_frame_sync_0_0_0_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.osmosdr_source_1, 0), (self.qtgui_freq_sink_x_0_1, 0))
        self.connect((self.osmosdr_source_1, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.zeromq_pull_source_0, 0), (self.lora_sdr_whitening_0, 0))
        self.connect((self.zeromq_pull_source_0_0, 0), (self.lora_sdr_whitening_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lora_bladerf")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_soft_decoding(self):
        return self.soft_decoding

    def set_soft_decoding(self, soft_decoding):
        self.soft_decoding = soft_decoding

    def get_sink_sf2(self):
        return self.sink_sf2

    def set_sink_sf2(self, sink_sf2):
        self.sink_sf2 = sink_sf2
        self.lora_sdr_gray_demap_0.set_sf(self.sink_sf2)
        self.lora_sdr_hamming_enc_0.set_sf(self.sink_sf2)
        self.lora_sdr_interleaver_0.set_sf(self.sink_sf2)
        self.lora_sdr_modulate_0.set_sf(self.sink_sf2)

    def get_sink_freq2(self):
        return self.sink_freq2

    def set_sink_freq2(self, sink_freq2):
        self.sink_freq2 = sink_freq2
        self.osmosdr_sink_0_0.set_center_freq(self.sink_freq2, 0)
        self.osmosdr_sink_0_0_0.set_center_freq(self.sink_freq2, 0)

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.lora_sdr_gray_demap_0_0.set_sf(self.sf)
        self.lora_sdr_hamming_enc_0_0.set_sf(self.sf)
        self.lora_sdr_interleaver_0_0.set_sf(self.sf)
        self.lora_sdr_modulate_0_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr
        self.lora_sdr_hamming_enc_0.set_cr(self.cr)
        self.lora_sdr_hamming_enc_0_0.set_cr(self.cr)
        self.lora_sdr_header_0.set_cr(self.cr)
        self.lora_sdr_header_0_0.set_cr(self.cr)
        self.lora_sdr_interleaver_0.set_cr(self.cr)
        self.lora_sdr_interleaver_0_0.set_cr(self.cr)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0_1.set_frequency_range(self.center_freq, 2000000)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, 2000000)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.osmosdr_sink_0_0.set_bandwidth(self.bw, 0)
        self.osmosdr_sink_0_0_0.set_bandwidth(self.bw, 0)




def main(top_block_cls=lora_bladerf, options=None):

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
