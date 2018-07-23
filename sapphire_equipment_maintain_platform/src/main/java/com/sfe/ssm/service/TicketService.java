package com.sfe.ssm.service;

import com.sfe.ssm.model.Ticket;

public interface TicketService {

    Ticket getTicket(String name);

    int updateTicket(Ticket ticket);

}
