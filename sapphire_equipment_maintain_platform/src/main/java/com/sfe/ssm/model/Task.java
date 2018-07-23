package com.sfe.ssm.model;

import lombok.Data;

import java.io.Serializable;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  17 2017,16:15
 * 定时任务类
 */
@Data
public class Task implements Serializable {

    private Long id;
    private String jobName;//任务名
    private String jobGroupName;//任务组名
    private String triggerName;//触发器名
    private String triggerGroupName;//触发器组名
    private String jobClass;//任务类  //完整类名 com.sfe.ssm.quartz.achieve.xxx
    private String cron;//时间设置，参考quartz说明文档
    private String remark;

}
