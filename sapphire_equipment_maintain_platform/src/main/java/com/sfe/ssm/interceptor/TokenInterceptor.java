package com.sfe.ssm.interceptor;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.common.oauth.Audience;
import com.sfe.ssm.common.oauth.JwtHelper;
import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  18 2017,16:34
 * 令牌验证过滤器 在配置文件中配置拦截的类
 */
public class TokenInterceptor implements HandlerInterceptor {

    @Autowired
    private Audience audienceEntity;

    @Override
    public void afterCompletion(HttpServletRequest arg0, HttpServletResponse arg1, Object arg2, Exception arg3)
            throws Exception {
        System.out.println("TokenInterceptor:afterCompletion");

    }

    private static final  int AL=7;
    @Override
    public void postHandle(HttpServletRequest arg0, HttpServletResponse arg1, Object arg2, ModelAndView arg3)
            throws Exception {
        System.out.println("TokenInterceptor:postHandle");


    }

    /**
     * 方法执行之前
     * @param request
     * @param response
     * @param handler
     * @return
     * @throws Exception
     */
    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response, Object handler) throws Exception {

        ResultMsg resultMsg;
        String auth = request.getHeader("Authorization");
        String bearer="bearer";
        if ((auth != null) && (auth.length() > AL)) {
            String headStr = auth.substring(0, 6).toLowerCase();
            if (headStr.compareTo(bearer) == 0) {
                auth = auth.substring(7, auth.length());
                Claims claims = JwtHelper.parseJWT(auth, audienceEntity.getBase64Secret());
                if (claims != null) {
                    return true;
                }
            }
        }

        response.setCharacterEncoding("UTF-8");
        response.setContentType("application/json; charset=utf-8");
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);

        ObjectMapper mapper = new ObjectMapper();

        resultMsg = new ResultMsg(ResultStatusCode.INVALID_TOKEN.getErrcode(), ResultStatusCode.INVALID_TOKEN.getErrmsg(), null);
        response.getWriter().write(mapper.writeValueAsString(resultMsg));
        return false;

    }

}
