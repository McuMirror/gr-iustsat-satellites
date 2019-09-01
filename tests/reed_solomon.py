#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Test Reed-Solomon encoding and decoding
# Author: Daniel Estevez
# GNU Radio version: 3.7.13.4
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt
import satellites


class reed_solomon(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Test Reed-Solomon encoding and decoding")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.satellites_encode_rs_0 = satellites.encode_rs(0)
        self.satellites_decode_rs_0 = satellites.decode_rs(True, 0)
        self.blocks_random_pdu_0 = blocks.random_pdu(1, 223, chr(0xFF), 1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)
        self.blocks_message_debug_0 = blocks.message_debug()



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.satellites_encode_rs_0, 'in'))
        self.msg_connect((self.satellites_decode_rs_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.satellites_encode_rs_0, 'out'), (self.satellites_decode_rs_0, 'in'))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=reed_solomon, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
