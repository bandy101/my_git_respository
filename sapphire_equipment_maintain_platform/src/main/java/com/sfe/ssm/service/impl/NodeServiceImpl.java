package com.sfe.ssm.service.impl;

import com.sfe.ssm.dao.NodeDao;
import com.sfe.ssm.model.Node;
import com.sfe.ssm.service.NodeService;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class NodeServiceImpl implements NodeService {

    @Resource
    NodeDao nodeDao;

    @Override
    public int createNode(Node node) {
        return nodeDao.createNode(node);
    }

    @Override
    public int updateNode(Node node) {
        return nodeDao.updateNode(node);
    }

    @Override
    public int deleteNode(int id) {
        return nodeDao.deleteNode(id);
    }

    @Override
    public Node getNode(String ordernum) {
        return nodeDao.getNode(ordernum);
    }

    @Override
    public Node getNodeid(int id){
        return nodeDao.getNodeid(id);
    }

    @Override
    public List<Node> getAllNode() {
        return nodeDao.getAllNode();
    }

}
