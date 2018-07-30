package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;
import java.util.Date;
import java.util.List;

@Getter
@Setter
public class Detection {
    //巡检表主键ID
    private int id;
    //巡检表单号
    private String orderNum;
    //设备ID
    private int equipmentId;
    //操作员ID
    private int operatorId;
    //外勤员ID
    private int workerId;
    //派单时间
    private Date createtime;
    //出勤时间
    private Date worktime;
    //完成时间
    private Date finishtime;
    //异常情况
    private String exception;
    //情况备注
    private String remark;
    //现场图片
    private String imgurl;
    //出勤定位
    private String location;
    //审核状态
    private int state;
    /** 表关联 **/
    //外勤员名字
    private String workerName;
    //操作员名字
    private String operatorName;
    //设备名称
    private String equipmentName;
    //设备编号
    private String equipmentCode;
    //设备位置
    private String equipmentLocation;
    /** 异常关联 **/
    private int type;
    /** 上传图片 **/
    private List<String> imgarr;
    /** 维修说明 **/
    private String explain;
    /** 批量派单 **/
    private List<Integer> equipmentIds;
}
