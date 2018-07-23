package com.sfe.ssm.controller;

import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.common.tool.GenerateAuthcode;
import com.sfe.ssm.model.Area;
import com.sfe.ssm.model.Equipment;
import com.sfe.ssm.model.Permission;
import com.sfe.ssm.model.User;
import com.sfe.ssm.otheroperation.DataTransfer;
import com.sfe.ssm.service.AreaService;
import com.sfe.ssm.service.DetectionService;
import com.sfe.ssm.service.EquipmentService;
import com.sfe.ssm.service.UserService;
import com.sfe.ssm.util.WxUtil;
import org.apache.shiro.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.*;

/**
 * 2018-01-26  JoeLyZH
 * 公共控制
 */
@RestController
@RequestMapping("/api/")
public class CommonController {

    @Autowired
    private DetectionService detectionService;
    @Autowired
    private AreaService areaService;
    @Autowired
    private UserService userService;
    @Autowired
    private EquipmentService equipmentService;
    @Autowired
    private DataTransfer dataTransfer;
    @Autowired
    private WxUtil wxUtil;

    /**
     * 根据权限开放首页展示内容
     * @return
     */
    @RequestMapping(value = "gohome/{code}", method = RequestMethod.GET, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> gohome(@PathVariable("code") String code){

        ResultMsg resultMsg;
        Map info = new HashMap();
        Equipment currEquipment = null;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        if(code.length()>10){
            currEquipment = equipmentService.getEquipmentByCode(code);
        }else{
            List<Area> areaAirEquipment = areaService.getAreaAirEquipmentList(areaIds);
            Map areaAir = new HashMap();
            for (Area area : areaAirEquipment) {
                areaAir.put(Integer.toString(area.getId()),area.getEquipmentList().get(0).getAirCode());
            }
            info.put("areaAir",areaAir);
        }
        List<Area> areaEquipment = areaService.getAreaEquipmentList(areaIds);
        info.put("areaEquipment",areaEquipment);
        info.put("currEquipment",currEquipment);
        String role = SecurityUtils.getSubject().getSession().getAttribute("USERROLE").toString();
        int uid = Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString());
        if(role.equals("worker")){
            //System.out.println(detectionService.getCountForWorker(uid));
        }
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 授权区域列表
     * @return
     */
    @RequestMapping(value = "general", method = RequestMethod.GET, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> general(){
        ResultMsg resultMsg;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        List<Area> arealist = areaService.getAreaList(areaIds);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), arealist);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 新版首页展示
     * @return
     */
    @RequestMapping(value = "welcome", method = RequestMethod.GET, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> welcome(){
        ResultMsg resultMsg;
        User user = userService.getUserById(Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString()));
        Map info = new HashMap();
        info.put("name",user.getName());
        info.put("role",user.getRole());
        info.put("logintime",user.getLogintime());
        info.put("unmark1",user.getUnmark1());
        info.put("unmark2",user.getUnmark2());
        info.put("unmark3",user.getUnmark3());
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 根据角色授权相应功能模块
     * @return
     */
    @RequestMapping(value = "showlist", method = RequestMethod.GET, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> showlist(){
        ResultMsg resultMsg;
        List<String> showlist=new ArrayList<String>();
        List<Permission> permissions = (List<Permission>) SecurityUtils.getSubject().getSession().getAttribute("USERPERMISSION");
        for (Permission permission:permissions) {
            String permissionsign = permission.getPermissionSign();
            if (permissionsign.indexOf(":show:")!=-1){
                showlist.add(permissionsign.replace(":show:","_"));
            }
        }
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), showlist);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 根据角色判断跳转巡检界面
     * @param request
     * @param response
     * @throws IOException
     */
    @RequestMapping(value = "detection")
    public void detection(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String role = SecurityUtils.getSubject().getSession().getAttribute("USERROLE").toString();
        if (role.equals("worker")||role=="worker") {
            response.sendRedirect(wxUtil.getDomain() + "/detection_list.html");
        }else{
            response.sendRedirect(wxUtil.getDomain() + "/detection_sketch.html");
        }
    }

    /**
     * 获取JSSDK数字签名串
     * @return
     * @throws IOException
     */
    @RequestMapping(value = "getsign", method = RequestMethod.GET, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getSign() throws IOException {
        ResultMsg resultMsg;
        Map signPackage = wxUtil.getSignPackage();
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), signPackage);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 个人账号绑定信息
     * @return
     */
    @RequestMapping(value = "personalinfo", method = RequestMethod.GET, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getPersonalInfo() throws IOException {
        ResultMsg resultMsg;
        int uid = Integer.parseInt(SecurityUtils.getSubject().getSession().getAttribute("USERID").toString());
        User user = userService.getUserById(uid);
        user.setAuthcode(GenerateAuthcode.randomAuthcode());
        Map info = new HashMap();
        info.put("user",user);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取全部设备地理位置 + 授权区域标识
     * @return
     */
    @RequestMapping(value = "getequipmentlocation", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getEquipmentLocation(){
        ResultMsg resultMsg;
        List<Equipment> equipmentList = equipmentService.selectEquipmentLocation();
        Map info = new HashMap();
        info.put("equipmentList",equipmentList);
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        info.put("areaIds",areaIds);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 根据授权区域获取全部设备[遥测+空气站]地理位置
     * @return
     */
    @RequestMapping(value = "getareaequipmentlocation", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaEquipmentLocation(){
        ResultMsg resultMsg;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        List<Equipment> equipmentList = equipmentService.selectAreaEquipmentLocation(areaIds);
        List<Equipment> airequipmentList = equipmentService.selectAirEquipmentLocation(areaIds);
        Map info = new HashMap();
        info.put("equipmentList",equipmentList);
        info.put("airequipmentList",airequipmentList);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取远端平台遥测设备数据
     * @param code
     * @return
     */
    @RequestMapping(value = "getequipmentdata/{code}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getEquipmentData(@PathVariable("code") String code){
        ResultMsg resultMsg;
        Map data = dataTransfer.getStatusExhaustData(code);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), data);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 通过区域ID获取该区域设备当天状态
     * @param aid
     * @return
     */
    @RequestMapping(value = "getareaequipment/{aid}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaEquipment(@PathVariable("aid") int aid){
        ResultMsg resultMsg;
        List<Equipment> equipmentlist = equipmentService.selectByAreaid(aid);
        Date date =new Date();
        SimpleDateFormat hh =new SimpleDateFormat("HH");
        int time=Integer.parseInt(hh.format(date));
        if (time < 6){
            time = 6;
        }
        int[] timeLabel={time-6,time-5,time-4,time-3,time-2,time-1};

        String utemp,itemp;
        for (Equipment equipment : equipmentlist) {
            int[] uvIntenHr={0,0,0,0,0,0};
            int[] irIntenHr={0,0,0,0,0,0};
            Map exhaustDay = dataTransfer.getStatusExhaustDay(equipment.getCode());
            equipment.setMonthPassCount(exhaustDay.get("monthPassCount").toString());
            equipment.setMonthNopassCount(exhaustDay.get("monthNopassCount").toString());
            equipment.setPassCount(exhaustDay.get("passCount").toString());
            equipment.setNopassCount(exhaustDay.get("nopassCount").toString());
            equipment.setInsideTemperature(exhaustDay.get("insideTemperature").toString());
            equipment.setInsideHumidity(exhaustDay.get("insideHumidity").toString());
            equipment.setWithoutTemperature(exhaustDay.get("withoutTemperature").toString());
            equipment.setWithoutHumidity(exhaustDay.get("withoutHumidity").toString());
            for (int i = 0; i < 6; i++) {
                if(timeLabel[i]<10){
                    utemp = "uvIntenHr0"+timeLabel[i];
                    itemp = "irIntenHr0"+timeLabel[i];
                }else{
                    utemp = "uvIntenHr"+timeLabel[i];
                    itemp = "irIntenHr"+timeLabel[i];
                }
                uvIntenHr[i] = Integer.parseInt(exhaustDay.get(utemp).toString());
                irIntenHr[i] = Integer.parseInt(exhaustDay.get(itemp).toString());
            }
            equipment.setUvIntenHr(uvIntenHr);
            equipment.setIrIntenHr(irIntenHr);
            equipment.setTimeLabel(timeLabel);
        }
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), equipmentlist);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     *通过设备编号获取该设备三天状态
     * @param code
     * @return
     */
    @RequestMapping(value = "getStatus3day/{code}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getStatus3day(@PathVariable("code") String code){
        ResultMsg resultMsg;
        List<Map> exhaust3day = dataTransfer.getStatusExhaust3d(code);
        String utemp,itemp,ihtemp,ohtemp,ittemp,ottemp;
        int[] uvIntenHr = new int[72];
        int[] irIntenHr = new int[72];
        float[] insideHumidityHr = new float[72];
        float[] withoutHumidityHr = new float[72];
        float[] insideTemperatureHr = new float[72];
        float[] withoutTemperatureHr = new float[72];
        int h = 0;
        float tmax = 0;
        float tmin = 0;
        float hmax = 0;
        float hmin = 0;
        for (Map exhaustData:exhaust3day) {
            for (int i = h; i < (23 + h); i++) {
                int j = i%23;
                if(j<10){
                    utemp = "uvIntenHr0"+j;
                    itemp = "irIntenHr0"+j;
                    ihtemp = "insideHumidityHr0"+j;
                    ohtemp = "withoutHumidityHr0"+j;
                    ittemp = "insideTemperatureHr0"+j;
                    ottemp = "withoutTemperatureHr0"+j;
                }else{
                    utemp = "uvIntenHr"+j;
                    itemp = "irIntenHr"+j;
                    ihtemp = "insideHumidityHr"+j;
                    ohtemp = "withoutHumidityHr"+j;
                    ittemp = "insideTemperatureHr"+j;
                    ottemp = "withoutTemperatureHr"+j;
                }
                uvIntenHr[i] = Integer.parseInt(exhaustData.get(utemp).toString());
                irIntenHr[i] = Integer.parseInt(exhaustData.get(itemp).toString());
                insideHumidityHr[i] = Float.parseFloat(exhaustData.get(ihtemp).toString());
                withoutHumidityHr[i] = Float.parseFloat(exhaustData.get(ohtemp).toString());
                insideTemperatureHr[i] = Float.parseFloat(exhaustData.get(ittemp).toString());
                withoutTemperatureHr[i] = Float.parseFloat(exhaustData.get(ottemp).toString());
                if(insideHumidityHr[i]>hmax){
                    hmax = insideHumidityHr[i];
                }else if(insideHumidityHr[i]<hmin){
                    hmin = insideHumidityHr[i];
                }
                if(withoutHumidityHr[i]>hmax){
                    hmax = withoutHumidityHr[i];
                }else if(withoutHumidityHr[i]<hmin){
                    hmin = withoutHumidityHr[i];
                }
                if(insideTemperatureHr[i]>tmax){
                    tmax = insideTemperatureHr[i];
                }else if(insideTemperatureHr[i]<tmin){
                    tmin = insideTemperatureHr[i];
                }
                if(withoutTemperatureHr[i]>tmax){
                    tmax = withoutTemperatureHr[i];
                }else if(withoutTemperatureHr[i]<tmin){
                    tmin = withoutTemperatureHr[i];
                }
            }
            h += 23;
        }
        Map sensingTotal = dataTransfer.getSensingTotal(code);
        int monthNopassCount = 0;
        int monthPassCount = 0;
        int nopassCount = 0;
        int passCount = 0;
        if (sensingTotal.containsKey("monthNopassCount")) {
            monthNopassCount = Integer.parseInt(sensingTotal.get("monthNopassCount").toString());
        }
        if (sensingTotal.containsKey("monthPassCount")) {
            monthPassCount = Integer.parseInt(sensingTotal.get("monthPassCount").toString());
        }
        if (sensingTotal.containsKey("nopassCount")) {
            nopassCount = Integer.parseInt(sensingTotal.get("nopassCount").toString());
        }
        if (sensingTotal.containsKey("nopassCount")) {
            passCount = Integer.parseInt(sensingTotal.get("passCount").toString());
        }
        int mupercent = 0;
        if ((monthNopassCount + monthPassCount) > 0) {
            mupercent = (monthNopassCount* 80) / (monthNopassCount + monthPassCount);
        }
        if (monthNopassCount>0 && mupercent<10){
            mupercent = 10;
        }
        int mppercent = 80-mupercent;
        int dupercent = 0;
        if ((nopassCount + passCount)>0) {
            dupercent = (nopassCount*80) / (nopassCount + passCount);
        }
        if (nopassCount>0 && dupercent<10){
            dupercent = 10;
        }
        int dppercent = 80-dupercent;
        int tz = (int)(tmax-tmin)/3;
        int hz = (int)(hmax-hmin)/3;
        Map<String, Object> info = new HashMap<String, Object>();
        info.put("uvIntenHr",uvIntenHr);
        info.put("irIntenHr",irIntenHr);
        info.put("insideHumidityHr",insideHumidityHr);
        info.put("withoutHumidityHr",withoutHumidityHr);
        info.put("insideTemperatureHr",insideTemperatureHr);
        info.put("withoutTemperatureHr",withoutTemperatureHr);
        info.put("monthNopassCount",monthNopassCount);
        info.put("monthPassCount",monthPassCount);
        info.put("nopassCount",nopassCount);
        info.put("passCount",passCount);
        info.put("mppercent",mppercent);
        info.put("mupercent",mupercent);
        info.put("dppercent",dppercent);
        info.put("dupercent",dupercent);
        info.put("minTemperature",(int)tmin);
        info.put("minHumidity",(int)hmin);
        info.put("tinterval",tz);
        info.put("hinterval",hz);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 通过设备编号获取远端平台空气站设备最新数据
     * @param code
     * @return
     */
    @RequestMapping(value = "getairquality/{code}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAirQuality(@PathVariable("code") String code){
        ResultMsg resultMsg;
        Map data = dataTransfer.getAirQuality(code);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), data);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 通过设备编号获取远端平台空气站设备当天24小时数据
     * @param code
     * @return
     */
    @RequestMapping(value = "getairqualityday/{code}/{date}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAirQualityDay(@PathVariable("code") String code,@PathVariable("date") String date) {
        ResultMsg resultMsg;
        float[] so2Hr = new float[24];
        float[] no2Hr = new float[24];
        float[] o3Hr = new float[24];
        float[] pm10Hr = new float[24];
        float[] pm25Hr = new float[24];
        float[] coHr = new float[24];
        Map airqualityday = dataTransfer.getAirQualityDay(code,date);
        for (int i = 0;i < 23;i++){
            so2Hr[i] = Float.parseFloat(airqualityday.get("so2Hr"+i).toString());
            no2Hr[i] = Float.parseFloat(airqualityday.get("no2Hr"+i).toString());
            o3Hr[i] = Float.parseFloat(airqualityday.get("o3Hr"+i).toString());
            pm10Hr[i] = Float.parseFloat(airqualityday.get("pm10Hr"+i).toString());
            pm25Hr[i] = Float.parseFloat(airqualityday.get("pm25Hr"+i).toString());
            coHr[i] = Float.parseFloat(airqualityday.get("coHr"+i).toString());
        }
        Map<String, Object> info = new HashMap<String, Object>();
        info.put("so2",so2Hr);
        info.put("no2",no2Hr);
        info.put("o3",o3Hr);
        info.put("pm10",pm10Hr);
        info.put("pm25",pm25Hr);
        info.put("co",coHr);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), info);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 获取所在区域及空气站设备列表
     * @return
     */
    @RequestMapping(value = "getareaairequipment", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> getAreaAirEquipment() {
        ResultMsg resultMsg;
        String areaIds = SecurityUtils.getSubject().getSession().getAttribute("AREAIDS").toString();
        List<Area> areaAirEquipment = areaService.getAreaAirEquipmentList(areaIds);
        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), areaAirEquipment);
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }
}
