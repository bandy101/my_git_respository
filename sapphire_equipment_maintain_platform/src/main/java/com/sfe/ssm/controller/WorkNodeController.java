package com.sfe.ssm.controller;

import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.model.Area;
import com.sfe.ssm.model.Item;
import com.sfe.ssm.model.Node;
import com.sfe.ssm.service.*;
import com.sfe.ssm.util.BaseToolUtil;
import com.sfe.ssm.util.WxUtil;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.apache.shiro.session.Session;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

/**
 * 2018-07-23  JoeLyZH
 * 作业流程节点控制类
 * 
 */
@RestController
@RequiresRoles(value = {"admin","operator"},logical = Logical.OR)
@RequestMapping("/api/node/")
public class WorkNodeController {

    @Autowired
    private AreaService areaService;
    @Autowired
    private UserService userService;
    @Autowired
    private NodeService nodeService;


    /**
     * 编辑节点信息
     *
     * @param node
     * @return
     */
    @RequestMapping(value = "nodeinfo", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> editNode(@RequestBody Node node) throws ParseException {
//        node.setContent("content");
//        node.setId(0);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        ResultMsg resultMsg;
        int result = 0;
        if (node.getId() > 0) {
            result = nodeService.updateNode(node);
        } else {
            int uid = Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString());
            node.setNodetime(new Date());
            node.setPartiesid(uid);
            String  name = userService.getUserById(uid).getName();
            node.setParties(name);
            result = nodeService.createNode(node);
        }
        if (result > 0) {
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "节点信息更新成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        } else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "节点信息更新失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 获取节点列表
     *
     * @return
     */
    @RequestMapping(value = "nodelist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getNodeList() {
        ResultMsg resultMsg;
        List<Node> lstData = nodeService.getAllNode();
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取关联节点
     *
     * @return
     */
    @RequestMapping(value = "nodedata/{ordernum}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getNode(@PathVariable("ordernum") String ordernum) {
        ResultMsg resultMsg;
        Node lstData = nodeService.getNode(ordernum);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取节点
     *
     * @return
     */
    @RequestMapping(value = "nodedataNode/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getNodeid(@PathVariable("id") int id) {
        ResultMsg resultMsg;
        Node lstData = nodeService.getNodeid(id);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 删除节点
     *
     * @param id
     * @return
     */
    @RequestMapping(value = "deletenode/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> deleteNode(@PathVariable("id") int id) {
        ResultMsg resultMsg;
        int result = nodeService.deleteNode(id);
        if (result > 0) {
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "删除节点成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        } else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "删除节点失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

}