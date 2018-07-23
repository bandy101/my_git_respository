package com.sfe.ssm.model;

import lombok.Data;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  19 2017,9:32
 * 认证信息类
 */
@Data
public class LoginPara {

    private String clientId;//客户端id
    private String userName;//用户名
    private String password;//密码
    private String captchaCode;//验证码 暂时不用
    private String captchaValue;//验证码值 暂时不用

}
