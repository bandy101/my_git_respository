package com.sfe.ssm.controller;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.model.Area;
import com.sfe.ssm.model.Detection;
import com.sfe.ssm.model.Item;
import com.sfe.ssm.model.Repair;
import com.sfe.ssm.service.*;
import com.sfe.ssm.util.BaseToolUtil;
import com.sfe.ssm.util.ImageUtil;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpServletRequest;
import java.util.*;

/**
 * 2017-12-27 JoeLyZH
 * 外勤作业信息管理
 */
@RestController
@RequiresRoles(value = "worker")
@RequestMapping("/api/work/")
public class WorkController {

    @Autowired
    private UserService userService;
    @Autowired
    private DetectionService detectionService;
    @Autowired
    private RepairService repairService;
    @Autowired
    private ItemService itemService;
    @Autowired
    private AreaService areaService;
    @Autowired
    private ImageUtil imageUtil;
    @Autowired
    private BaseToolUtil baseToolUtil;

    /**
     * 外勤人员获取未巡检列表
     * @param pn
     * @param ps
     * @return
     */
    @RequestMapping(value = "detectionlist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getDetectionPageList(@RequestParam boolean done, @RequestParam int pn, @RequestParam int ps){
        ResultMsg resultMsg;
        int wid = Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString());
        int unmark = userService.getUserById(wid).getUnmark1();
        PageInfo lstData = detectionService.getDetectionPageList(wid , done , pn , ps);
        int count = detectionService.getCountForWorker(wid);
        if(count != unmark){
            userService.updateUnmark1(wid , count);
        }
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取巡检信息
     * @param id
     * @return
     */
    @RequestMapping(value = "detectioninfo/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getDetectionInfo(@PathVariable("id") int id){
        ResultMsg resultMsg;
        Map info = new HashMap();
        Detection detection = detectionService.getDetectionById(id);
        info.put("detection",detection);
        List<Item> items = itemService.getAllItem();
        info.put("items",items);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 巡检信息表-填单
     * @param detection
     * @return
     */
    @RequestMapping(value = "filldetection", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> fillInDetection(@RequestBody Detection detection,HttpServletRequest request){
        ResultMsg resultMsg;
        int result = 0;
        detection.setWorktime(new Date());
        detection.setState(2);
        List<String> imgarr = detection.getImgarr();
        if (!imgarr.isEmpty()){
            String imgurl = imageUtil.SaveIMGbyBASE64(imgarr,request);
            detection.setImgurl(imgurl);
        }
        if(detection.getRemark().isEmpty()){
            String remark;
            if(detection.getException()!=null&&detection.getException().length()>0) {
                remark = baseToolUtil.joinByList("、",itemService.getExceptionItem(detection.getException()));
                switch (detection.getType()) {
                    case 1 : remark += " 现场已处理";
                        break;
                    case 2 : remark += " 需要报修";
                        break;
                    case 3 : remark += " 需要维护";
                        break;
                    case 4 : remark += " 需要返厂";
                        break;
                }
            }else {
                remark = "设备正常运行";
            }
            detection.setRemark(remark);
        }
        result = detectionService.fillinDetection(detection);
        if(result > 0){
            int repairid = 0;
            //判断处理类型
            if (detection.getType()>1) {
                //创建维修信息表
                Repair repair = new Repair();
                repair.setEid(detection.getEquipmentId());
                repair.setWid(detection.getWorkerId());
                repair.setType(detection.getType());
                repair.setEventid(detection.getId());
                repair.setException(detection.getException());
                repair.setResult(detection.getExplain());
                repair.setCreatetime(new Date());
                repair.setState(4);
                repairService.createRepair(repair);
                repairid = repair.getId();
            }

            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), repairid);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "巡检信息更新失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 读取维修表列表
     * @param type
     * @param pn
     * @param ps
     * @return
     */
    @RequestMapping(value = "repairlist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getRepairListByPage(@RequestParam int type,@RequestParam int pn, @RequestParam int ps){
        ResultMsg resultMsg;
        String workerId = SecurityUtils.getSubject().getSession().getAttribute("USERID").toString();
        PageInfo lstData = repairService.selectByPageList(null, workerId, type , pn , ps);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 读取维修表信息
     * @param id
     * @return
     */
    @RequestMapping(value = "repairdisposeinfo/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> repairDisposeInfo(@PathVariable("id") int id){
        ResultMsg resultMsg;
        Repair repair = repairService.getRepairInfoById(id);
        if(repair!=null){
            String exception = repair.getException();
            if (exception!=null && exception.trim().length()>0){
                repair.setException(baseToolUtil.joinByList("、",itemService.getExceptionItem(exception)));
            }
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), repair);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "维修表信息错误");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 维修表 - 填单
     * @param repair
     * @return
     */
    @RequestMapping(value = "fillinrepair", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> fillinRepair(@RequestBody Repair repair){
        ResultMsg resultMsg;
        int result = 0;
        repair.setChecktime(new Date());
        repair.setState(1);
        result = repairService.fillinRepair(repair);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "维修表信息更新成功");
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "维修表信息更新失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取维修表相关选项
     * @return
     */
    @RequestMapping(value = "getrepairreleva", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getRepairReleva(){
        ResultMsg resultMsg;
        Map releva = new HashMap();
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        List<Area> areas = areaService.getAreaEquipmentList(areaIds);
        releva.put("areas",areas);
        List<Item> items = itemService.getAllItem();
        releva.put("items",items);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), releva);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 创建维修表
     * @param repair
     * @return
     */
    @RequestMapping(value = "createrepair", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> createRepair(@RequestBody Repair repair,HttpServletRequest request){
        ResultMsg resultMsg;
        int result = 0;
        repair.setWid(Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString()));
        repair.setCreatetime(new Date());
        List<String> imgarr = repair.getImgarr();
        if (!imgarr.isEmpty()){
            String imgurl = imageUtil.SaveIMGbyBASE64(imgarr,request);
            repair.setImgurl(imgurl);
        }
        result = repairService.createRepair(repair);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "维修表创建成功");
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "维修表创建失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 维修信息表 - 现场确认
     * @param repair
     * @return
     */
    @RequestMapping(value = "finishrepair", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> finishRepair(@RequestBody Repair repair){
        ResultMsg resultMsg;
        int result = 0;
        repair.setFinishtime(new Date());
        result = repairService.finishRepair(repair);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "维修表确认成功");
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "维修表确认失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

}
