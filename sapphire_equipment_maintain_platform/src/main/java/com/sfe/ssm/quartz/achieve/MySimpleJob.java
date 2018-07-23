package com.sfe.ssm.quartz.achieve;

import com.sfe.ssm.common.cache.redis.RedisCacheService;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.scheduling.quartz.QuartzJobBean;


import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  17 2017,14:59
 * SimpleTrigger 类型定时器 支持毫秒
 */
public class MySimpleJob extends QuartzJobBean {

    private static int i = 0;

    @Autowired
    private RedisCacheService redisCacheService;//redis 缓存服务类

    @Override
    protected void executeInternal(JobExecutionContext context) throws JobExecutionException {


        DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        System.out.println(sdf.format(new Date())+"*********MySimpleJob" +
                "任务每10毫秒执行一次进入测试"+i++);

        redisCacheService.putSessionObject("123Simple"+i++,"wwwwwww"+i++);
    }
}
