package com.sfe.ssm.otheroperation;

import com.alibaba.fastjson.JSONObject;
import com.sfe.ssm.common.oauth.Audience;
import com.sfe.ssm.common.tool.HttpGetEmulator;
import com.sfe.ssm.common.tool.HttpPostEmulator;
import com.sfe.ssm.model.Ticket;
import com.sfe.ssm.service.TicketService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component
public class DataTransfer {

    @Autowired
    private Audience audience;
    @Autowired
    private TicketService ticketService;

    public String getToken(){
        JSONObject jsonObject=new JSONObject();
        jsonObject.put("clientId","098f6bcd4621d373cade4e832627b4f6");
        jsonObject.put("userName","admin");
        jsonObject.put("password","sfe5188");
        jsonObject.put("captchaCode","232");
        jsonObject.put("captchaValue","232");

        String requestUrl=audience.getServerIP_self()+"/api/1/oauth/token";
        String token=null;
        try {
            HttpPostEmulator hpe = new HttpPostEmulator();
            String response = hpe.sendPost(requestUrl, token, jsonObject);
            if (response != null && response.length() > 0) {
                jsonObject = JSONObject.parseObject(response);
                if (jsonObject.containsKey("errmsg")) {
                    if (jsonObject.getString("errmsg").equals("OK")) {
                        JSONObject content = JSONObject.parseObject(jsonObject.getString("content"));
                        if (content.containsKey("accessToken")) {
                            token = content.getString("accessToken");
                            Ticket ticket = new Ticket();
                            ticket.setName("self_token");
                            ticket.setValue(token);
                            ticketService.updateTicket(ticket);
                        }
                    }
                }
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return token;
    }

    public Map getStatusExhaustDay(String code){
        Map exhaustDay = new HashMap();
        String token = ticketService.getTicket("self_token").getValue();
        String requestUrl=audience.getServerIP_self()+"/api/1/equipmentStatusExhaustDay?tsNo=";
        try {
            HttpGetEmulator hge = new HttpGetEmulator();
            String response = hge.sendGet(requestUrl, code, token);
            if (response != null && response.length() > 0) {
                JSONObject jsonObject = JSONObject.parseObject(response);
                if (jsonObject.containsKey("errmsg")) {
                    if (jsonObject.getString("errmsg").equals("OK")) {
                        exhaustDay = JSONObject.parseObject(jsonObject.getString("content"));
                    }
                }
            }else {
                getToken();
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return exhaustDay;
    }

    /**
     * [数据接口] - [遥测设备] - 获取设备当天数据
     * @param code
     * @return
     */
    public Map getStatusExhaustData(String code){
        Map exhaustData = new HashMap();
        String token = ticketService.getTicket("self_token").getValue();
        String requestUrl=audience.getServerIP_self()+"/api/1/eqp?tsNo=";
        try {
            HttpGetEmulator hge = new HttpGetEmulator();
            String response = hge.sendGet(requestUrl, code, token);
            if (response != null && response.length() > 0) {
                JSONObject jsonObject = JSONObject.parseObject(response);
                if (jsonObject.containsKey("errmsg")) {
                    if (jsonObject.getString("errmsg").equals("OK")) {
                        exhaustData = JSONObject.parseObject(jsonObject.getString("content"));
                    }
                }
            }else {
                getToken();
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return exhaustData;
    }

    /**
     * [数据接口] - [遥测设备] - 获取3天数据
     * @param code
     * @return
     */
    public List getStatusExhaust3d(String code){
        List exhaust3day = new ArrayList<Map>();
        String token = ticketService.getTicket("self_token").getValue();
        String requestUrl=audience.getServerIP_self()+"/api/1/equipmentStatus3Day?tsNo=";
        try {
            HttpGetEmulator hge = new HttpGetEmulator();
            String response = hge.sendGet(requestUrl, code, token);
            if (response != null && response.length() > 0) {
                JSONObject jsonObject = JSONObject.parseObject(response);
                if (jsonObject.containsKey("errmsg")) {
                    if (jsonObject.getString("errmsg").equals("OK")) {
                        exhaust3day = JSONObject.parseArray(jsonObject.getString("content"));

                    }
                }
            }else {
                getToken();
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return exhaust3day;
    }

    /**
     * [数据接口] - 获取月合格日合格统计数据
     * @param code
     * @return
     */
    public Map getSensingTotal(String code){
        Map sensingTotal = new HashMap();
        String token = ticketService.getTicket("self_token").getValue();
        String requestUrl=audience.getServerIP_self()+"/api/1/remoteSensingTotal?tsNo=";
        try {
            HttpGetEmulator hge = new HttpGetEmulator();
            String response = hge.sendGet(requestUrl, code, token);
            if (response != null && response.length() > 0) {
                JSONObject jsonObject = JSONObject.parseObject(response);
                if (jsonObject.containsKey("errmsg")) {
                    if (jsonObject.getString("errmsg").equals("OK")) {
                        sensingTotal = JSONObject.parseObject(jsonObject.getString("content"));
                    }
                }
            }else {
                getToken();
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return sensingTotal;
    }

    /**
     * [数据接口] - [空气站] - 获取设备最新数据
     * {{ip}}/api/{{version}}/airQuality?tsNo=AQM65180401
     * @param code
     * @return
     */
    public Map getAirQuality(String code){
        Map airQuality = new HashMap();
        String token = ticketService.getTicket("self_token").getValue();
        String requestUrl=audience.getServerIP_self()+"/api/1/airQuality?tsNo=";
        try {
            HttpGetEmulator hge = new HttpGetEmulator();
            String response = hge.sendGet(requestUrl, code, token);
            if (response != null && response.length() > 0) {
                JSONObject jsonObject = JSONObject.parseObject(response);
                if (jsonObject.containsKey("errmsg")) {
                    if (jsonObject.getString("errmsg").equals("OK")) {
                        airQuality = JSONObject.parseObject(jsonObject.getString("content"));
                    }
                }
            }else {
                getToken();
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return airQuality;
    }

    /**
     * [数据接口] - [空气站] - 获取当天24小时数据
     * {{ip}}/api/{{version}}/airQualityDay?tsNo=AQM65-G22W2772&date=2018-07-09
     * @param code
     * @return
     */
    public Map getAirQualityDay(String code,String date){
        Map airqualityday = new HashMap();
        String token = ticketService.getTicket("self_token").getValue();
        String requestUrl=audience.getServerIP_self()+"/api/1/airQualityDay?tsNo=";
        try {
            HttpGetEmulator hge = new HttpGetEmulator();
            String param = code+"&date="+date;
            String response = hge.sendGet(requestUrl, param, token);
            if (response != null && response.length() > 0) {
                JSONObject jsonObject = JSONObject.parseObject(response);
                if (jsonObject.containsKey("errmsg")) {
                    if (jsonObject.getString("errmsg").equals("OK")) {
                        airqualityday = JSONObject.parseObject(jsonObject.getString("content"));

                    }
                }
            }else {
                getToken();
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return airqualityday;
    }
}
