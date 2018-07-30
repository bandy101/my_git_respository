package com.sfe.ssm.controller;

import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.model.Area;
import com.sfe.ssm.model.Equipment;
import com.sfe.ssm.model.Permission;
import com.sfe.ssm.model.User;
import com.sfe.ssm.service.AreaService;
import com.sfe.ssm.service.DetectionService;
import com.sfe.ssm.service.UserService;
import com.sfe.ssm.util.WxUtil;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.*;
import org.apache.shiro.authz.UnauthorizedException;
import org.apache.shiro.session.Session;
import org.apache.shiro.subject.Subject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.*;

/**
 * 2017-12-5  JoeLyZH
 * 授权管理 - 区域/角色控制
 * 绑定微信 - 自动登录/授权
 */
@RestController
@RequestMapping("/api/")
public class AuthenticateController {

    @Autowired
    private WxUtil wxUtil;
    @Autowired
    private UserService userService;
    //微信绑定授权开关
    private boolean CLOSE_WX = true;

    /**
     * 微信平台手机邀请码登入
     * @param user
     * @return
     */
    @RequestMapping(value = "login", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> login(@RequestBody User user){
        String info = loginUser(user);
        ResultMsg resultMsg;
        if (info.equals("SUCC")){
            info = SecurityUtils.getSubject().getSession().getAttribute("USERROLE").toString();
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), info);
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }else{
            resultMsg = new ResultMsg(ResultStatusCode.FALSE_LOGIN.getErrcode(),
                    ResultStatusCode.FALSE_LOGIN.getErrmsg(), info);
            return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
        }
    }

    /**
     * 系统登出
     * @return
     */
    @RequestMapping(value = "checkout")
    public ResponseEntity<ResultMsg> checkout() {
        ResultMsg resultMsg = new ResultMsg(ResultStatusCode.CHECK_OUT.getErrcode(),
                        ResultStatusCode.CHECK_OUT.getErrmsg(), "系统已登出");
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 判断登入 - 若绑定微信号自动登录
     * @param request
     * @param response
     * @throws IOException
     */
    @RequestMapping(value = "checkin")
    public void checkin(HttpServletRequest request,HttpServletResponse response) throws IOException {
        //微信授权跨域问题，不能使用异步跳转
        //ResultMsg resultMsg = null;
        if(CLOSE_WX) {
            response.sendRedirect(wxUtil.getDomain() + "/login.html?auto=invalid");
            //resultMsg = new ResultMsg(ResultStatusCode.INVALID_AUTO_LOGIN.getErrcode(),ResultStatusCode.INVALID_AUTO_LOGIN.getErrmsg(), "关闭授权登录");
        }else {
            String code = request.getParameter("code");
            if (code != null) {
                String authcode = wxUtil.getauth(code, 1);
                User user = userService.getUserByAuth(authcode);
                if (user == null) {
                    Session session = SecurityUtils.getSubject().getSession();
                    session.setAttribute("authcode", authcode);
                    response.sendRedirect(wxUtil.getDomain() + "/login.html?auto=invalid");
                    //resultMsg = new ResultMsg(ResultStatusCode.INVALID_AUTO_LOGIN.getErrcode(), ResultStatusCode.INVALID_AUTO_LOGIN.getErrmsg(), "关闭授权登录");
                } else {
                    UsernamePasswordToken token = new UsernamePasswordToken(user.getTelphone(), user.getAuthcode());
                    SecurityUtils.getSubject().login(token);
                    user.setLogintime(new Date());
                    userService.logintimeUser(user);
                    response.sendRedirect(wxUtil.getDomain() + "/welcome.html");
                    //resultMsg = new ResultMsg(ResultStatusCode.INVALID_AUTO_LOGIN.getErrcode(), ResultStatusCode.INVALID_AUTO_LOGIN.getErrmsg(), "关闭授权登录");
                }
            } else {
                wxUtil.getcode("/api/checkin", "snsapi_userinfo", response);
            }
        }
        //return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 越权处理
     * @return
     */
    @RequestMapping(value = "checkback")
    public ResponseEntity<ResultMsg> checkback() {
        ResultMsg resultMsg = new ResultMsg(ResultStatusCode.CHECK_BACK.getErrcode(),
                ResultStatusCode.CHECK_BACK.getErrmsg(), "权限不够");
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 检验是否已登录
     * @param user
     * @return
     */
    private String loginUser(User user) {
        if (isAuthenticated(user)) return "SUCC"; // 如果已经登陆，无需重新登录
        return userToken(user); // 调用shiro的登陆验证
    }

    /**
     * 注销登录
     * @return
     */
    @RequestMapping(value = "logout", method = RequestMethod.GET, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> logout(){
        ResultMsg resultMsg;
        Subject subject = SecurityUtils.getSubject();
        if (subject != null) {
            subject.logout();
        }
        resultMsg = new ResultMsg(ResultStatusCode.CHECK_OUT.getErrcode(),
                ResultStatusCode.CHECK_OUT.getErrmsg(), "系统已登出");
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 解绑微信号
     * @param user
     * @return
     */
    @RequestMapping(value = "unbind", method = RequestMethod.POST, consumes = "application/json",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResultMsg> unbind(@RequestBody User user){
        ResultMsg resultMsg;
        int result = userService.bindUser(user);
        if(result > 0) {
            Subject subject = SecurityUtils.getSubject();
            if (subject != null) {
                subject.logout();
            }
            resultMsg = new ResultMsg(ResultStatusCode.CHECK_OUT.getErrcode(),
                    ResultStatusCode.CHECK_OUT.getErrmsg(), "账号已解绑");
        }else{
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "操作失败");
        }
        return new ResponseEntity<ResultMsg>(resultMsg, HttpStatus.OK);
    }

    /**
     * 验证token
     */
    private String userToken(User user) {
        //组装token
        String msg = "SUCC";
        UsernamePasswordToken token = new UsernamePasswordToken(user.getTelphone(),user.getAuthcode());
        //token.setRememberMe(true);
        try {
            SecurityUtils.getSubject().login(token);
        } catch (IncorrectCredentialsException e) {
            msg = "邀请码错误或已失效";
        } catch (ExcessiveAttemptsException e) {
            msg = "登录失败次数过多";
        } catch (LockedAccountException e) {
            msg = "帐号已被锁定";
        } catch (DisabledAccountException e) {
            msg = "帐号已被禁用";
        } catch (ExpiredCredentialsException e) {
            msg = "会话已过期，请重新登录";
        } catch (UnknownAccountException e) {
            msg = "该手机号未录入本系统";
        } catch (UnauthorizedException e) {
            msg = "您没有得到相应的授权";
        }
        return msg;
    }

    /**
     * 判断是否已授权登录
     * @param user
     * @return
     */
    private boolean isAuthenticated(User user) {
        Subject subject = SecurityUtils.getSubject();
        if (subject.isAuthenticated()) {
            return true;
        }
        return false;
    }

}
