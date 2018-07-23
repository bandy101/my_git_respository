package com.sfe.ssm.quartz.achieve;

import com.sfe.ssm.common.cache.redis.RedisCacheService;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.stereotype.Component;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  17 2017,14:59
 * 自定义定时任务类 继承org.quartz.Job
 */
@Component
public class MyJob implements Job {

    private static int i = 0;

    @Autowired
    private RedisCacheService redisCacheService;//redis 缓存服务类

    @Override
    public void execute(JobExecutionContext jobExecutionContext) throws JobExecutionException {
        DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        System.out.println(sdf.format(new Date())+"*********doing something...");

        redisCacheService.putSessionObject("123"+i++,"wwwwwww"+i++);
    }
}
