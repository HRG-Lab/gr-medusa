/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_PREAMBLE_TO_PDU_IMPL_H
#define INCLUDED_MEDUSA_PREAMBLE_TO_PDU_IMPL_H

#include <gnuradio/medusa/preamble_to_pdu.h>
#include <vector>
#include <string>

namespace gr {
namespace medusa {

class preamble_to_pdu_impl : public preamble_to_pdu
{
private:
    int d_num_elements;
    std::string d_corr_tag;
    unsigned int d_preamble_size;
    std::vector<gr_complex> d_rx_preamble;

    uint64_t mute_until_offset;
    void publish();

public:
    preamble_to_pdu_impl(int num_elements,
                         const unsigned int data_length,
                         const std::string& corr_tag);
    ~preamble_to_pdu_impl();

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_PREAMBLE_TO_PDU_IMPL_H */
