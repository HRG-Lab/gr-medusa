/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "preamble_to_pdu_impl.h"
#include <gnuradio/io_signature.h>


namespace gr {
namespace medusa {

preamble_to_pdu::sptr preamble_to_pdu::make(int num_elements,
                                            const unsigned int data_length,
                                            const std::string& corr_tag)
{
    return gnuradio::make_block_sptr<preamble_to_pdu_impl>(
        num_elements, data_length, corr_tag);
}


preamble_to_pdu_impl::preamble_to_pdu_impl(int num_elements,
                                           const unsigned int data_length,
                                           const std::string& corr_tag)
    : gr::sync_block("preamble_to_pdu",
                     gr::io_signature::make(1, 1, num_elements * sizeof(gr_complex)),
                     gr::io_signature::make(0, 0, 0)),
      d_num_elements(num_elements),
      d_corr_tag(corr_tag)
{
    d_preamble_size = data_length;
    mute_until_offset = 0;

    message_port_register_out(pmt::mp("pdus"));
}

preamble_to_pdu_impl::~preamble_to_pdu_impl() {}

void preamble_to_pdu_impl::publish()
{
    pmt::pmt_t vecpmt(pmt::init_c32vector(d_rx_preamble.size(), &d_rx_preamble[0]));
    pmt::pmt_t pdu(pmt::cons(pmt::PMT_NIL, vecpmt));
    message_port_pub(pmt::mp("pdus"), pdu);

    d_rx_preamble.resize(0);
}

int preamble_to_pdu_impl::work(int noutput_items,
                               gr_vector_const_void_star& input_items,
                               gr_vector_void_star& output_items)
{
    auto in = static_cast<const gr_complex*>(input_items[0]);

    std::vector<tag_t> tags;
    get_tags_in_window(tags, 0, 0, noutput_items, pmt::intern(d_corr_tag));

    unsigned long int nread = nitems_read(0);

    // If we have a partially received preamble, add to it
    if (d_rx_preamble.size() > 0 &&
        d_rx_preamble.size() < d_preamble_size * d_num_elements) {
        int samples_stored_already = d_rx_preamble.size() / d_num_elements;
        int samples_remaining = d_preamble_size - samples_stored_already;
        samples_remaining =
            (samples_remaining <= noutput_items) ? samples_remaining : noutput_items;
        d_rx_preamble.resize(d_rx_preamble.size() + samples_remaining * d_num_elements);
        std::copy(&in[0],
                  &in[samples_remaining * d_num_elements],
                  &d_rx_preamble[d_num_elements * samples_stored_already]);
    }

    if (d_rx_preamble.size() >= d_preamble_size * d_num_elements)
        publish();


    for (unsigned t = 0; t < tags.size(); t++) {
        uint64_t offset = tags[t].offset - nread;

        if (tags[t].offset < mute_until_offset)
            continue;

        mute_until_offset = tags[t].offset + d_preamble_size;

        unsigned int samples_in_window = noutput_items - offset;
        if (samples_in_window >= d_preamble_size)
            d_rx_preamble.assign(in + offset * d_num_elements,
                                 in + offset * d_num_elements +
                                     d_num_elements * d_preamble_size);
        else {
            d_rx_preamble.assign(in + offset * d_num_elements,
                                 in + offset * d_num_elements +
                                     d_num_elements * samples_in_window);
        }

        if (d_rx_preamble.size() >= d_preamble_size * d_num_elements)
            publish();
    }

    return noutput_items;
}

} /* namespace medusa */
} /* namespace gr */
