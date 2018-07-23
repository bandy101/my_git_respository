package com.sfe.ssm.common;

import lombok.Getter;
import lombok.Setter;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  19 2017,10:20
 * 返回错误代码 不能使用lombok 枚举
 */

public enum ResultStatusCode {


    /**
     * ok
     */
    OK(0, "OK"),

    /**
     * 系统错误
     */
    SYSTEM_ERR(30001, "System error"),
    /**
     * 登录错误
     */
    FALSE_LOGIN(30002, "False login"),
    /**
     * 参数错误
     */
    PARAMETER_ERR(30003, "Parameter error"),
    /**
     * 用户名或密码不正确
     */
    INVALID_PASSWORD(30004, "User name or password is incorrect"),
    /**
     * 验证码或验证码无效逾期
     */
    INVALID_CAPTCHA(30005, "Invalid captcha or captcha overdue"),
    /**
     * 令牌无效
     */
    INVALID_TOKEN(30006, "Invalid token"),
    /**
     * 查找不到
     */
    INVALID_NOT_FOUND(30007, "Not Found"),
    /**
     * 已登出
     */
    CHECK_OUT(3008, "Check Out"),
    /**
     * 越权
     */
    CHECK_BACK(3301, "Check Back"),
    /**
     * 自动登录 - 无效
     */
    INVALID_AUTO_LOGIN(3009, "Invalid Auto");

    //成员变量
    @Setter
    @Getter
    private int errcode;

    @Setter
    @Getter
    private String errmsg;



    private ResultStatusCode(int errCode, String errMsg)
    {
        this.errcode = errCode;
        this.errmsg = errMsg;
    }
}
