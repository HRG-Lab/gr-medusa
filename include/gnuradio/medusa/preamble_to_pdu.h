/* -*- c++ -*- */
/*
 * Copyright 2023 Bailey Campbell.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MEDUSA_PREAMBLE_TO_PDU_H
#define INCLUDED_MEDUSA_PREAMBLE_TO_PDU_H

#include <gnuradio/medusa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
namespace medusa {

class MEDUSA_API preamble_to_pdu : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<preamble_to_pdu> sptr;

    static sptr
    make(int num_elements, const unsigned int data_length, const std::string& corr_tag);
};

} // namespace medusa
} // namespace gr

#endif /* INCLUDED_MEDUSA_PREAMBLE_TO_PDU_H */
