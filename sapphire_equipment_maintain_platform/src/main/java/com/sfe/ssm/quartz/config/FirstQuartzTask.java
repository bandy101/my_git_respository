package com.sfe.ssm.quartz.config;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  12 2017,14:34
 * 第一个任务类
 */
public class FirstQuartzTask {

    public void test(){
        DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        System.out.println(sdf.format(new Date())+"*********FirstQuartzTask" +
                "A任务每5秒执行一次进入测试");
    }

    public void testTwo(){
        DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        System.out.println(sdf.format(new Date())+"*********FirstQuartzTask" +
                "AA任务每5秒执行一次进入测试");
    }

}
