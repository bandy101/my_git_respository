package com.sfe.ssm.quartz.config;

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
 * @date 七月  12 2017,13:45
 */
public class TaskOneDemo extends QuartzJobBean {

    private static int i = 0;
    @Autowired
    private RedisCacheService redisCacheService;//redis 缓存服务类

    @Override
    protected void executeInternal(JobExecutionContext context) throws JobExecutionException {

        DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        System.out.println(sdf.format(new Date())+"*********A任务每10秒执行一次进入测试"+i++);
        redisCacheService.putSessionObject("123"+i++,"wwwwwww"+i++);
    }


}
