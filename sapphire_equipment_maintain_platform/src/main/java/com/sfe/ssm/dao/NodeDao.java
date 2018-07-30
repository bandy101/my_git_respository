package com.sfe.ssm.dao;

import com.sfe.ssm.model.Item;
import com.sfe.ssm.model.Node;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface NodeDao {

    List<Node> getAllNode();

    List<Node> getNode(@Param("ordernum") String ordernum);

    Node getNodeid(@Param("id") int id );

    int createNode (Node node);

    int updateNode(Node node);

    int deleteNode(@Param("id") int id);
}
