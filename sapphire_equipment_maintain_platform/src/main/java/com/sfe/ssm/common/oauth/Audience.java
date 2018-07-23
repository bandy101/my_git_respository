package com.sfe.ssm.common.oauth;


import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;


/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  19 2017,13:39
 * 令牌读取配置类
 */
@Configuration
@Setter
@Getter
public class Audience {

    /**
     * 客户端Id
     */
    @Value("#{configProperties['clientId']}")
    private String clientId;

    /**
     *加密钥匙
     */
    @Value("#{configProperties['base64Secret']}")
    public String base64Secret;

    /**
     * 名字
     */
    @Value("#{configProperties['name']}")
    private String name;

    /**
     * 过期时间
     */
    @Value("#{configProperties['expiresSecond']}")
    private int expiresSecond;

    /**
     * apiKey
     */
    @Value("#{configProperties['apiKey']}")
    private String apiKey;

    /**
     * 自用设备平台IP
     */
    @Value("#{configProperties['serverIP_self']}")
    private String serverIP_self;

}
