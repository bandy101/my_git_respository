package com.sfe.ssm.initialization;

import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;

/**
 * @author 廖志群
 * @version 1.00
 * @date 八月  02 2017,11:41
 * Spring容器将所有的Bean都初始化完成之后，做一些操作
 */
public class InstantiationTracingBeanPostProcessor implements ApplicationListener<ContextRefreshedEvent> {
    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
            //初始化定时统计任务
            QuartzInit.init();
//        }
    }
}