package com.sfe.ssm.util;

import com.sfe.ssm.model.Ticket;
import com.sfe.ssm.service.TicketService;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.Charset;
import java.util.*;

@Service("WxUtil")
public class WxUtil {

    @Autowired
    private TicketService ticketService;
    @Autowired
    private HttpServletRequest request;


    private String APPID  = "wx178e0152cc690d71";
    private String SECRET = "d708d9fd6d6496599758b878917d3998";
    private String DOMAIN = "http://gd.etc-cn.com";

    public String getDomain(){
        return this.DOMAIN;
    }

    /**
     * 2017-11-14 JoeLyZH
     * 通过code换取网页授权access_token
     * 获取code后，请求以下链接获取access_token：
     * https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
     * 如果网页授权的作用域为snsapi_base，则本步骤中获取到网页授权access_token的同时，也获取到了openid，snsapi_base式的网页授权流程即到此为止
     * 参数定义【type: 1-返回openid； 2-返回access_token】
     */
    public String getauth(String code , int type) throws IOException {
        String auth;
        // 拼接请求地址
        String requestUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?"
                +"appid=" + APPID
                +"&secret=" + SECRET
                +"&code=" + code
                +"&grant_type=authorization_code";
        JSONObject json = readJsonFromUrl(requestUrl);
        if(type == 1) {
            auth = json.optString("openid");
        }else {
            auth = json.optString("access_token");
        }
        return auth;
    }

    /**
     * 用户同意授权，获取code
     * 授权地址https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
     * 应用授权作用域，snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid），
     * snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）
     */
    public void getcode(String servletpath , String scope , HttpServletResponse resp) throws IOException {

        resp.setContentType("text/html;charset=utf-8");
        resp.setCharacterEncoding("utf-8");

        String contextpath = DOMAIN + servletpath;
        // 授权后重定向的回调链接地址，请使用urlencode对链接进行处理
        String redirect_uri = URLEncoder.encode(contextpath, "utf-8");
        // 拼接授权地址
        String url = "https://open.weixin.qq.com/connect/oauth2/authorize?"
                + "appid=" + APPID
                + "&redirect_uri=" + redirect_uri
                + "&response_type=code"
                + "&scope=" + scope
                + "&state=STATE#wechat_redirect";
        resp.sendRedirect(url);
    }

    public Map getSignPackage() throws IOException{
        Map signPackage = new HashMap();
        String url = request.getHeader("referer");
        String nonceStr = createNonceStr(16);
        String timestamp = String.valueOf(System.currentTimeMillis());
        String shaString = "jsapi_ticket="+getJsApiTicket()+"&noncestr="+nonceStr+"&timestamp="+timestamp+"&url="+url;
        signPackage.put("appId",this.APPID);
        signPackage.put("timestamp",timestamp);
        signPackage.put("nonceStr",nonceStr);
        signPackage.put("signature",SHA1.encode(shaString));
        return signPackage;
    }

    /**
     * 解析微信URL返回JSON
     * @param url
     * @return
     * @throws IOException
     * @throws JSONException
     */
    public static JSONObject readJsonFromUrl(String url) throws IOException, JSONException {
        InputStream is = new URL(url).openStream();
        try {
            BufferedReader rd = new BufferedReader(new InputStreamReader(is, Charset.forName("UTF-8")));
            String jsonText = readAll(rd);
            JSONObject json = new JSONObject(jsonText);
            return json;
        } finally {
            is.close();
        }
    }

    /**
     * 读取字符
     * @param rd
     * @return
     * @throws IOException
     */
    private static String readAll(Reader rd) throws IOException {
        StringBuilder stringBuilder = new StringBuilder();
        int cp;
        while ((cp = rd.read()) != -1) {
            stringBuilder.append((char) cp);
        }
        return stringBuilder.toString();
    }

    private static String createNonceStr(int length){
        String chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        String str = "";
        Random rand = new Random();
        for (int i = 0; i < length; ++i) {
            int j= rand.nextInt(chars.length());
            str += chars.substring(j,j+1);
        }
        return str;
    }

    public String getAccessToken() throws IOException{
        Ticket ticket = ticketService.getTicket("access_token");
        long time = (System.currentTimeMillis()-ticket.getTime().getTime())/1000;
        String access_token = ticket.getValue();
        if(time>7000){
            String requestUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
                    + "&appid=" + APPID
                    + "&secret=" + SECRET;
            JSONObject json = readJsonFromUrl(requestUrl);
            //System.out.println(json);
            access_token = json.optString("access_token");
            if(access_token!=null){
                Ticket new_ticket = new Ticket();
                new_ticket.setName("access_token");
                new_ticket.setValue(access_token);
                ticketService.updateTicket(new_ticket);
            }
        }
        return access_token;
    }

    private String getJsApiTicket() throws IOException{
        Ticket ticket = ticketService.getTicket("jsapi_ticket");
        long time = (System.currentTimeMillis()-ticket.getTime().getTime())/1000;
        String jsapi_ticket = ticket.getValue();
        if(time>7000){
            String access_token = getAccessToken();
            String requestUrl = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token="+access_token;
            JSONObject json = readJsonFromUrl(requestUrl);
            jsapi_ticket = json.optString("ticket");
            if(jsapi_ticket!=null){
                Ticket new_ticket = new Ticket();
                new_ticket.setName("jsapi_ticket");
                new_ticket.setValue(jsapi_ticket);
                ticketService.updateTicket(new_ticket);
            }
        }
        return jsapi_ticket;
    }
}
