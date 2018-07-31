package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;
import java.util.List;

@Getter
@Setter
public class Repair {
    //主键ID
    private int id;
    //设备编号
    private int eid;
    //出单员ID
    private int oid;
    //出勤人员ID
    private int wid;
    //类型 1：检修  2：报修  3：维护  4：返厂  5：升级
    private int type;
    //事件ID
    private int eventid;
    //异常情况
    private String exception;
    //跟进结果
    private String result;
    //出单时间
    private Date createtime;
    //审核时间
    private Date checktime;
    //完成时间
    private Date finishtime;
    //现场图片
    private String imgurl;
    //状态 0：未处理(外勤)  1：待审核(内勤)  2：已解决  3：未解决  4：待后台核复(内勤)  5：待现场确认(外勤)
    private int state;
    /** 上传图片 **/
    private List<String> imgarr;
    /** 表关联 **/
    //外勤员名字
    private String workerName;
    //设备名称
    private String equipmentName;
    //设备编号
    private String equipmentCode;
    //关联单号
    private  String ordernum;
}
