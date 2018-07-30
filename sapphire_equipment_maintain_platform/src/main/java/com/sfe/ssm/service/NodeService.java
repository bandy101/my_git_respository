package com.sfe.ssm.service;

import com.sfe.ssm.model.Node;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface NodeService {

    int createNode (Node node);

    int updateNode(Node node);

    int deleteNode(int id);

    List<Node> getNode(String ordernum);

    Node getNodeid(int id );

    List<Node>getAllNode();


}