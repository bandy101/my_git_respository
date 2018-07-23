package com.sfe.ssm.common.oauth;

import lombok.Data;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  19 2017,9:41
 * token返回结果类
 */
@Data
public class AccessToken {
    private String accessToken;
    private String tokenType;
    private long expiresIn;

}
