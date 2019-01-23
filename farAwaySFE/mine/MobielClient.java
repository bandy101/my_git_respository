// package cn.itcast.mobile.client;


import cn.itcast.mobile.Webservice; // 端口
import cn.itcast.mobile.WebServiceImplService; // 服务
import cn.itcast.mobile.Ygjcsjxxb;

/**
 * 
* @ClassName: MobileClient 
* @Description: test
* @author michealzhuwb
* @date 2019年1月21日 16:35 
*
 */
public class MobileClient {
    public static void main(String[] args) {
        WebServiceImplService webs = new WebServiceImplService();

        Webservice Webservices = webs.getWebServiceImplPort();
        // boolean mobileCodeInfo = Webservice.addYgjcsjxxb(0.0,0.0,"1",0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"1","1",0.0,0.0,"1","1","1","1","1","1",0.0,0.0,0.0,"1",1,1,"1",0.0,"1",0.0,1,"1","1","1","1","1",0.0,0.0,0.0,0.0);
        Ygjcsjxxb T= new Ygjcsjxxb();
        boolean result = Webservices.addYgjcsjxxb(T);
        System.out.println(result);
    }
}