package com.sfe.ssm.listener;

import com.sfe.ssm.initialization.QuartzInit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  18 2017,9:25
 * spring 加载时 初始化自定义监听器
 */
public class StartInitListener implements ServletContextListener {
    static final Logger logger = LoggerFactory.getLogger(StartInitListener.class);


    /**
     * 系统初始化执行方法
     * @param e
     */
    @Override
    public void contextDestroyed(ServletContextEvent e) {
        logger.info("系统停止...");
    }

    @Override
    public void contextInitialized(ServletContextEvent e) {
        logger.info("系统初始化开始...");

        //region 要初始化的操作

        // 获取项目根目录
        String rootPath  = e.getServletContext().getRealPath("/");
        logger.info("application path : {}",rootPath);

        //初始化定时统计任务
        QuartzInit.init();

        //endregion
        logger.info("系统初始化结束...");
    }

}
