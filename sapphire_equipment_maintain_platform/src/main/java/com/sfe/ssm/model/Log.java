package com.sfe.ssm.model;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  24 2017,16:12
 * 日志的实体 不能使用lombok 横向切入比注入早
 */
public class Log {

    private int id;//
    private String userId;//登陆账号
    private String module;//执行模块
    private String method;//执行的方法
    private String responseData;//响应时间
    private String ip;//IP地址
    private String data;//执行时间
    private String description;//执行描述

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getuserId() {
        return userId;
    }

    public void setuserId(String userName) {
        this.userId = userId;
    }

    public String getModule() {
        return module;
    }

    public void setModule(String module) {
        this.module = module;
    }

    public String getMethod() {
        return method;
    }

    public void setMethod(String method) {
        this.method = method;
    }

    public String getResponseData() {
        return responseData;
    }

    public void setResponseData(String responseData) {
        this.responseData = responseData;
    }

    public String getIP() {
        return ip;
    }

    public void setIP(String ip) {
        this.ip = ip;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String commite) {
        this.description = description;
    }


}
