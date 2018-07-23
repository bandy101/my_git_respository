package com.sfe.ssm.dao;

import com.sfe.ssm.model.Ticket;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface TicketDao {

    Ticket getTicket(@Param("name") String name);

    int updateTicket(Ticket ticket);

}
