package com.sfe.ssm.controller;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.common.tool.GenerateAuthcode;
import com.sfe.ssm.model.*;
import com.sfe.ssm.service.*;
import com.sfe.ssm.util.BaseToolUtil;
import com.sfe.ssm.util.WxUtil;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.apache.shiro.session.Session;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.*;

/**
 * 2017-11-28 JoeLyZH
 * 系统信息管理
 */
@RestController
@RequiresRoles(value = {"admin","operator"},logical = Logical.OR)
@RequestMapping("/api/manage/")
public class ManageController {

    @Autowired
    private AreaService areaService;
    @Autowired
    private UserService userService;
    @Autowired
    private EquipmentService equipmentService;
    @Autowired
    private ItemService itemService;
    @Autowired
    private DetectionService detectionService;
    @Autowired
    private RepairService repairService;
    @Autowired
    private BaseToolUtil baseTool;
    @Autowired
    private WxUtil wxUtil;

    /**
     * 编辑区域信息
     * @param area
     * @return
     */
    @RequestMapping(value = "areainfo", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> editArea(@RequestBody Area area){
        ResultMsg resultMsg;
        int result = 0;
        if(area.getId()>0){
            result = areaService.updateArea(area);
        }else {
            result = areaService.createArea(area);
            int id = area.getId();
            if(id > 0){
                int uid = Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString());
                int res = userService.addArea(id,uid);
                if(res > 0){
                    Session session = SecurityUtils.getSubject().getSession();
                    session.setAttribute("AREAIDS",id+","+SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString());
                }
            }
        }
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "区域信息更新成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "区域信息更新失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 获取区域信息
     * @param id
     * @return
     */
    @RequiresPermissions("area:read")
    @RequestMapping(value = "areainfo/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getArea(@PathVariable("id") int id){
        ResultMsg resultMsg;
        Area area = areaService.getAreaById(id);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), area);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取区域列表
     * [pn] - 页数 [ps] - 条数 <不传查全部>
     * [areaIds] 授权区域
     * @param request
     * @return
     */

    @RequestMapping(value = "arealist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaListByPage(HttpServletRequest request){
        ResultMsg resultMsg;
        int pn = request.getParameter("pn")!=null?Integer.parseInt(request.getParameter("pn")):0;
        int ps = request.getParameter("ps")!=null?Integer.parseInt(request.getParameter("ps")):0;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        if(pn > 0 && ps > 0) {
            PageInfo lstData = areaService.selectByPageList(areaIds, pn, ps);
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), lstData);
        }else {
            List<Area> areas = areaService.getAreaList(areaIds);
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), areas);
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 删除区域
     * @param id
     * @return
     */
    @RequiresPermissions("area:delete")
    @RequestMapping(value = "deletearea/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> deleteArea(@PathVariable("id") int id){
        ResultMsg resultMsg;
        int result = areaService.deleteArea(id);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "删除区域成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "删除区域失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }


    /**
     * 编辑设备信息
     * @param equipment
     * @return
     */
    @RequestMapping(value = "equipmentinfo", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public  ResponseEntity<ResultMsg> editArea(@RequestBody Equipment equipment){
        ResultMsg resultMsg;
        int result = 0;

        // 检查设备编码是否与数据库冲突
        if(equipmentService.isExistEquipment(equipment) ){
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "\"设备编码\" 重复！");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }

        if(equipment.getId()>0){
            result = equipmentService.updateEquipment(equipment);
        }else {
            result = equipmentService.createEquipment(equipment);
        }
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "设备信息更新成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "设备信息更新失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 获取设备信息
     * @param id
     * @return
     */
    @RequestMapping(value = "equipmentinfo/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getEquipment(@PathVariable("id") int id){
        ResultMsg resultMsg;
        Equipment equipment = equipmentService.getEquipmentById(id);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), equipment);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取设备列表
     * @param pn
     * @param ps
     * @return
     */
    @RequestMapping(value = "equipmentlist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getEquipmentListByPage(@RequestParam int pn, @RequestParam int ps){
        ResultMsg resultMsg;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        PageInfo lstData = equipmentService.selectByPageList(areaIds , pn , ps);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 删除设备
     * @param id
     * @return
     */
    @RequestMapping(value = "deleteequipment/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> deleteEquipment(@PathVariable("id") int id){
        ResultMsg resultMsg;
        int result = equipmentService.deleteEquipment(id);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "删除设备成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "删除设备失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 编辑用户信息
     * @param user
     * @return
     */
    @RequestMapping(value = "userinfo", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public  ResponseEntity<ResultMsg> editUser(@RequestBody User user){
        ResultMsg resultMsg;
        int result = 0;

        // 检查usr中的telephone是否与数据库中的记录冲突
        if(userService.isExistPhoneNumber(user) ){
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "\"联系手机\" 重复！");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }

        if(user.getId()>0){
            result = userService.updateUser(user);
        }else {
            user.setAuthcode(GenerateAuthcode.randomAuthcode());    //向待创建数据添加邀请码
            result = userService.createUser(user);
        }
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "人员信息更新成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "人员信息更新失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 获取用户信息
     * @param id
     * @return
     */
    @RequestMapping(value = "userinfo/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getUser(@PathVariable("id") int id) throws IOException {
        ResultMsg resultMsg;
        User user = userService.getUserById(id);
        List<Area> arealist = areaService.getAreaList(null);
        String[] userArea = (user.getArea()).split(",");
        List<String> userArealist = new ArrayList();
        for (Area area:arealist) {
            if(baseTool.findByList(area.getId(),userArea)){
                userArealist.add(area.getName());
                area.setAuth(true);
            }
        }
        if(userArealist.size() != 0) {
            user.setAreaname(baseTool.joinByList("、",userArealist));
        }
        Map info = new HashMap();
        info.put("user",user);
        info.put("arealist",arealist);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取用户列表
     * @param pn
     * @param ps
     * @return
     */
    @RequestMapping(value = "userlist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getUserListByPage(@RequestParam int pn, @RequestParam int ps){

        String roleType = SecurityUtils.getSubject().getSession().getAttribute("USERROLE").toString();
        String areaIDs = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        PageInfo lstData = null;

        // 根据登陆者角色不同选择显示其管辖范围内的其他人员~~~
        if(roleType.equals("admin")){
            lstData = userService.getPageInfoByINTArea(areaIDs, "1,2,3", pn , ps);
        }else if(roleType.equals("operator")){
            lstData = userService.getPageInfoByINTArea(areaIDs, "3", pn , ps);
        }else{
            //TODO:外勤人员,当前无处理~~~
        }

        ResultMsg resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取区域外勤人员列表
     * @param id
     * @return
     */
    @RequestMapping(value = "areaworker/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaWorker(@PathVariable("id") int id){
        ResultMsg resultMsg;
        List<User> users = userService.getAreaWorker(id);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), users);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 删除用户
     * @param id
     * @return
     */
    @RequestMapping(value = "deleteuser/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> deleteUser(@PathVariable("id") int id){
        ResultMsg resultMsg;
        int result = userService.deleteUser(id);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "删除人员成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "删除人员失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 编辑事项信息
     * @param item
     * @return
     */
    @RequestMapping(value = "iteminfo", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public  ResponseEntity<ResultMsg> editItem(@RequestBody Item item){
        ResultMsg resultMsg;
        int result = 0;
        if(item.getId()>0){
            result = itemService.updateItem(item);
        }else {
            result = itemService.createItem(item);
        }
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "事项信息更新成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "事项信息更新失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 获取事项列表
     * @return
     */
    @RequestMapping(value = "itemlist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getItemList(){
        ResultMsg resultMsg;
        List<Item> lstData = itemService.getAllItem();
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 删除事项
     * @param id
     * @return
     */
    @RequestMapping(value = "deleteitem/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> deleteItem(@PathVariable("id") int id){
        ResultMsg resultMsg;
        int result = itemService.deleteItem(id);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "删除事项成功");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "删除事项失败");
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.NO_CONTENT);
        }
    }

    /**
     * 获取授权区域设备列表
     * @return
     */
    @RequestMapping(value = "areaequipmentlist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaEquipmentList(){
        ResultMsg resultMsg;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        List<Area> area = areaService.getAreaEquipmentList(areaIds);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), area);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取授权区域设备列表以及已派单（周）设备列表
     * @return
     */
    @RequestMapping(value = "areaequlistandassign", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaEqulistAndAssign(){
        ResultMsg resultMsg;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        List<Area> equlist = areaService.getAreaEquipmentList(areaIds);
        Map map = new HashMap();
        map.put("equlist",equlist);
        List<Integer> assignequids = detectionService.getWeekAssigneEqu(areaIds);
        map.put("assignequids",assignequids);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), map);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取区域巡检信息表
     * @param id
     * @param pn
     * @param ps
     * @return
     */
    @RequestMapping(value = "areadetectionlist", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaDetectionList(@RequestParam int id, @RequestParam int pn, @RequestParam int ps, @RequestParam String week){
        ResultMsg resultMsg;
        if(week.isEmpty() || week==""){
            Calendar cal = Calendar.getInstance();
            week = cal.get(Calendar.YEAR)+"-"+cal.get(Calendar.WEEK_OF_YEAR);
        }
        PageInfo lstData = detectionService.getAreaWeekDetectionList(id, week , pn , ps);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取巡检信息总括
     * @return
     */
    @RequestMapping(value = "getdetectionsketch", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getDetectionSketch(){
        int state1=0;
        int state2=0;
        int state3=0;
        int ucount=0;
        ResultMsg resultMsg;
        Map sketch = new HashMap();
        Calendar cal = Calendar.getInstance();
        String year = String.valueOf(cal.get(Calendar.YEAR));
        String month = String.valueOf(cal.get(Calendar.MONTH)+1);
        String week = String.valueOf(cal.get(Calendar.WEEK_OF_MONTH));
        sketch.put("week",year+"年"+month+"月第"+week+"周");
        sketch.put("thisweek",year+"-"+cal.get(Calendar.WEEK_OF_YEAR));
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        int acount = equipmentService.getCountInArea(areaIds);
        sketch.put("acount",acount);
        List<Integer> detectionNums = detectionService.getWeekDetectionNums(areaIds);
        for (int state:detectionNums) {
            ucount++;
            switch (state){
                case 1 : state1++;
                    break;
                case 2 : state2++;
                    break;
                case 3 : state3++;
                    break;
            }
        }
        sketch.put("ucount",acount - ucount);
        sketch.put("state1",state1);
        sketch.put("state2",state2);
        sketch.put("state3",state3);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), sketch);
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
        Equipment equipment = equipmentService.getEquipmentAssign(detection.getEquipmentId());
        info.put("equipment",equipment);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取设备巡检指派信息
     * @param id
     * @return
     */
    @RequestMapping(value = "equipmentassign/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getEquipmentAssign(@PathVariable("id") int id){
        ResultMsg resultMsg;
        Equipment equipment = equipmentService.getEquipmentAssign(id);
        if(equipment!=null){
            Map info = new HashMap();
            info.put("equipment",equipment);
            Detection detection = detectionService.getWeekDetectionById(id);
            if(detection!=null){
                info.put("detection",detection);
            }
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), info);
        }else{
            resultMsg = new ResultMsg(ResultStatusCode.PARAMETER_ERR.getErrcode(),
                    ResultStatusCode.PARAMETER_ERR.getErrmsg(), equipment);
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 巡检信息表-派单
     * @param detection
     * @return
     */
    @RequestMapping(value = "assigninfo", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public  ResponseEntity<ResultMsg> editAssign(@RequestBody Detection detection) throws IOException {
        ResultMsg resultMsg;
        int result = 0;
        detection.setOperatorId(Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString()));
        Date date = new Date();
        detection.setOrderNum((date.getTime()+detection.getEquipmentId())+"7");
        detection.setCreatetime(date);
        detection.setState(1);
        result = detectionService.createDetection(detection);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "巡检派单成功");
            userService.addUnmark1(detection.getWorkerId(), 1);
            String accessToken = wxUtil.getAccessToken();
            User user = userService.getUserById(detection.getWorkerId());
            Equipment equipment = equipmentService.getEquipmentById(detection.getEquipmentId());
            DateFormat bf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Calendar cal = Calendar.getInstance();
            URL url = new URL("https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="+accessToken);
            HttpURLConnection urlConnection = (HttpURLConnection)url.openConnection();
            urlConnection.setDoOutput(true);
            urlConnection.setDoInput(true);
            urlConnection.setRequestMethod("POST");
            urlConnection.setUseCaches(false);
            urlConnection.setInstanceFollowRedirects(true);
            urlConnection.setRequestProperty("Content-Type","application/x-www-form-urlencoded");
            urlConnection.setRequestProperty("Charset", "UTF-8");
            urlConnection.connect();
            DataOutputStream out = new DataOutputStream(urlConnection.getOutputStream());
            String params="{"+
                    "\"touser\":\""+user.getAuthcode()+"\","+
                    "\"template_id\":\"MN7ncnSZaJUiQmk5d1A73RvRZ7skkUEDWMLuJYcFScE\","+
                    "\"url\":\"http://gd.etc-cn.com/\","+
                    "\"topcolor\":\"#FF0000\","+
                    "\"data\":{"+
                    "\"first\": {"+
                    "\"value\":\""+user.getName()+"，您收到一条设备巡检通知\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword1\":{"+
                    "\"value\":\""+equipment.getName()+"\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword2\":{"+
                    "\"value\":\""+equipment.getCode()+"\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword3\":{"+
                    "\"value\":\""+bf.format(date)+"\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword4\":{"+
                    "\"value\":\""+cal.get(Calendar.YEAR)+"年"+cal.get(Calendar.MONTH)+"月份第"+cal.get(Calendar.WEEK_OF_MONTH)+"周\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"remark\":{"+
                    "\"value\":\"请尽快安排站点日常巡检，谢谢！\","+
                    "\"color\":\"#173177\""+
                    "}"+
                    "}"+
                    "}";
            out.write(params.getBytes("UTF-8"));
            out.flush();
            out.close();
            BufferedReader reader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),"UTF-8"));
            reader.close();
            urlConnection.disconnect();
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "巡检派单失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 巡检信息表-批量派单
     * @param detection
     * @return
     */
    @RequestMapping(value = "assignbatch", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public  ResponseEntity<ResultMsg> assignBatch(@RequestBody Detection detection) throws IOException {
        ResultMsg resultMsg;
        int result = 0;
        int count = 0;
        detection.setOperatorId(Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString()));
        Date date = new Date();
        detection.setCreatetime(date);
        detection.setState(1);
        List<Integer> equipmentIds = detection.getEquipmentIds();
        for (int eid:equipmentIds) {
            detection.setEquipmentId(eid);
            detection.setOrderNum((date.getTime()+eid)+"6");
            result = detectionService.createDetection(detection);
            count++;
        }

        if(count > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "巡检派单成功");
            userService.addUnmark1(detection.getWorkerId(), count);
            String accessToken = wxUtil.getAccessToken();
            User user = userService.getUserById(detection.getWorkerId());
            String operator = userService.getUserById(detection.getOperatorId()).getName();
            List<String> equipmentNames = equipmentService.selectNameList(baseTool.joinByIntList(",",equipmentIds));
            DateFormat bf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Calendar cal = Calendar.getInstance();

            URL url = new URL("https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="+accessToken);
            HttpURLConnection urlConnection = (HttpURLConnection)url.openConnection();
            urlConnection.setDoOutput(true);
            urlConnection.setDoInput(true);
            urlConnection.setRequestMethod("POST");
            urlConnection.setUseCaches(false);
            urlConnection.setInstanceFollowRedirects(true);
            urlConnection.setRequestProperty("Content-Type","application/x-www-form-urlencoded");
            urlConnection.setRequestProperty("Charset", "UTF-8");
            urlConnection.connect();
            DataOutputStream out = new DataOutputStream(urlConnection.getOutputStream());
            String params="{"+
                    "\"touser\":\""+user.getAuthcode()+"\","+
                    "\"template_id\":\"ojMMaJXonkwaIjeDW2Csi7eOyRDsij6z-vgHVEOr2Qs\","+
                    "\"url\":\"http://gd.etc-cn.com/\","+
                    "\"topcolor\":\"#FF0000\","+
                    "\"data\":{"+
                    "\"first\": {"+
                    "\"value\":\""+user.getName()+"，您有"+count+"处设备需要进行巡检\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword1\":{"+
                    "\"value\":\""+cal.get(Calendar.YEAR)+"年"+cal.get(Calendar.MONTH)+"月份第"+cal.get(Calendar.WEEK_OF_MONTH)+"周\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword2\":{"+
                    "\"value\":\""+bf.format(date)+"\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword3\":{"+
                    "\"value\":\""+operator+"\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword4\":{"+
                    "\"value\":\""+user.getAddress()+"\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"keyword5\":{"+
                    "\"value\":\"日常巡检\","+
                    "\"color\":\"#173177\""+
                    "},"+
                    "\"remark\":{"+
                    "\"value\":\""+baseTool.joinByList("、",equipmentNames)+"\","+
                    "\"color\":\"#173177\""+
                    "}"+
                    "}"+
                    "}";
            out.write(params.getBytes("UTF-8"));
            out.flush();
            out.close();
            BufferedReader reader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),"UTF-8"));
            reader.close();
            urlConnection.disconnect();
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "巡检派单失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 巡检信息表-撤单
     * @param id
     * @return
     */
    @RequestMapping(value = "deletedetection/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> deleteDetection(@PathVariable("id") int id){
        ResultMsg resultMsg;
        int result = detectionService.deleteDetection(id);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "巡检撤单成功");
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "巡检撤单失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 巡检信息表-结单
     * @param id
     * @return
     */
    @RequestMapping(value = "finishdetection/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> finishDetection(@PathVariable("id") int id){
        ResultMsg resultMsg;
        Detection detection = new Detection();
        detection.setId(id);
        detection.setFinishtime(new Date());
        detection.setState(3);
        int result = detectionService.finishDetection(detection);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "巡检结单成功");
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "巡检结单失败");
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
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        PageInfo lstData = repairService.selectByPageList(areaIds, null, type , pn , ps);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstData);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 创建维修表
     * @param repair
     * @return
     */
    @RequestMapping(value = "createrepair", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> createRepair(@RequestBody Repair repair){
        ResultMsg resultMsg;
        int result = 0;
        repair.setOid(Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString()));
        repair.setCreatetime(new Date());
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
     * 获取设备维修指派信息
     * @param id
     * @return
     */
    @RequestMapping(value = "repairdisposeinfo/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> repairDisposeInfo(@PathVariable("id") int id){
        ResultMsg resultMsg;
        Repair repair = repairService.getRepairById(id);
        if(repair!=null){
            Map info = new HashMap();
            String exception = repair.getException();
            if (exception!=null && exception.trim().length()>0){
                repair.setException(baseTool.joinByList("、",itemService.getExceptionItem(exception)));
            }
            info.put("repair",repair);
            Equipment equipment = equipmentService.getEquipmentAssign(repair.getEid());
            info.put("equipment",equipment);
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), info);
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "维修表信息错误");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 维修信息表-撤单
     * @param id
     * @return
     */
    @RequiresRoles(value = {"admin","operator","worker"},logical = Logical.OR)
    @RequestMapping(value = "deleterepair/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> deleteRepair(@PathVariable("id") int id){
        ResultMsg resultMsg;
        int result = repairService.deleteRepair(id);
        if(result > 0){
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), "维修撤单成功");
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "维修撤单失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 维修信息表-结单
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
                    ResultStatusCode.OK.getErrmsg(), "维修表结单成功");
        }else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "维修表结单失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 维修表 - 核复
     * @param repair
     * @return
     */
    @RequestMapping(value = "fillinrepair", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> fillinRepair(@RequestBody Repair repair){
        ResultMsg resultMsg;
        int result = 0;
        repair.setOid(Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString()));
        repair.setChecktime(new Date());
        repair.setState(5);
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

}
