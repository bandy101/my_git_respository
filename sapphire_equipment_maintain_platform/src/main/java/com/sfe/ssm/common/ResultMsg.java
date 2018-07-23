package com.sfe.ssm.common;



import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  19 2017,10:31
 * api返回数据统一格式
 */
@Setter
@Getter
public class ResultMsg implements Serializable {

    /**
     * 返回代码
     */
    private int errcode;
    /**
     *返回代码内容
     */
    private String errmsg;
    /**
     *返回内容
     */
    private Object content;

    public ResultMsg(int errCode, String errMsg, Object content)
    {
        this.errcode = errCode;
        this.errmsg = errMsg;
        this.content = content;
    }
}
