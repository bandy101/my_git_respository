package com.sfe.ssm.service.impl;

import com.sfe.ssm.dao.TicketDao;
import com.sfe.ssm.model.Ticket;
import com.sfe.ssm.service.TicketService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service("TicketService")
public class TicketServiceImpl implements TicketService {

    @Resource
    private TicketDao ticketDao;

    @Override
    public Ticket getTicket(String name) {
        return ticketDao.getTicket(name);
    }

    @Override
    public int updateTicket(Ticket ticket) {
        return ticketDao.updateTicket(ticket);
    }
}
