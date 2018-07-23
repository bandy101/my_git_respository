package com.sfe.ssm.common.log;

import java.lang.annotation.*;
/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  24 2017,16:06
 * 日志类型
 */

@Target({ElementType.PARAMETER, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface SystemLog {
    String module()  default "";
    String methods()  default "";
}
