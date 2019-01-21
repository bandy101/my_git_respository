// package cn.itcast.mobile.client;

import cn.itcast.mobile.Webservice; //porttype
import cn.itcast.mobile.WebServiceImplService;
// import cn.itcast.mobile.WebServiceImplServiceSoapBinding;
import cn.itcast.mobile.Ygjcsjxxb;
/**
 * 
* @ClassName: MobileClient 
* @Description: TODO(公网手机号查询客户端) 
* @author 
* @date 20.017年11月8日 上午8:35:0.02 
*
 */
public class MobielClient {
    public static void main(String[] args) {
        //创建服务访问点集合的对象，例如：<wsdl:service name="MobileCodeWS">
        WebServiceImplService webs = new WebServiceImplService();
        //获取服务实现类，例如：<wsdl:portType name="MobileCodeWSSoap">，port--binding--portType
        //MobileCodeWSSoap mobileCodeWSSoap = mobileCodeWS.getPort(MobileCodeWSSoap.class);
        //根据服务访问点的集合中的服务访问点的绑定对象来获得绑定的服务类
        //获得服务类的方式是get+服务访问点的name：getWSServerPort
        Webservice s = webs.getWebServiceImplPort();
        // String mobileCodeInfo = mobileCodeWSSoap.getMobileCodeInfo("18518114962", "");
        // System.out.println(mobileCodeInfo);
        // WebServiceImplServiceSoapBinding x = new WebServiceImplServiceSoapBinding();
        //a =0.0,0.0,"1",0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"1","1",0.0,0.0,,"1","1","1","1","1","1",0.0,0.0,0.0,"1",1,1,"1",0.0,"1",0.0,1,"1","1","1","1","1",0.0,0.0,0.0,0.0 
        boolean X = false;
        // boolean r = s.addYgjcsjxxb(0.0,0.0,"1",0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"1","1",0.0,0.0,"1","1","1","1","1","1",0.0,0.0,0.0,"1",1,1,"1",0.0,"1",0.0,1,"1","1","1","1","1",0.0,0.0,0.0,0.0);
        Ygjcsjxxb x = new Ygjcsjxxb();
        boolean r =s.addYgjcsjxxb(x);
        System.out.println(r);

    }
}