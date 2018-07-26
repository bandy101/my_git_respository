package com.sfe.ssm.service;

import com.sfe.ssm.model.Node;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface NodeService {

    int createNode (Node node);

    int updateNode(Node node);

    int deleteNode(int id);

    Node getNode(@Param("ordernum") String ordernum);

    List<Node>getAllNode();


}
