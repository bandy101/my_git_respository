package com.sfe.ssm.realm;

import com.sfe.ssm.model.Permission;
import com.sfe.ssm.model.User;
import com.sfe.ssm.service.UserService;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.*;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.authz.SimpleAuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.session.Session;
import org.apache.shiro.subject.PrincipalCollection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * 2017-12-08 JoeLyZH
 * 授权管理-[作用域]
 */
@Component(value = "userAuthorizingRealm")
public class UserAuthorizingRealm extends AuthorizingRealm {

    @Autowired
    private UserService userService;

    /**
     * 权限控制
     * @param principalCollection
     * @return
     */
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principalCollection) {
        Set<String> roleNames = new HashSet<String>();
        Set<String> permissions = new HashSet<String>();
        roleNames.add(SecurityUtils.getSubject().getSession().getAttribute("USERROLE").toString());
        permissions.add("area:read");
        SimpleAuthorizationInfo info = new SimpleAuthorizationInfo(roleNames);
        info.setStringPermissions(permissions);
        return info;
    }

    /**
     * 身份验证
     * @param authenticationToken
     * @return
     * @throws AuthenticationException
     */
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken authenticationToken) throws AuthenticationException {
        UsernamePasswordToken token = (UsernamePasswordToken) authenticationToken;
        String telphone = token.getUsername();
        User user = userService.getUserByTel(telphone);
        if (user == null) {
            throw new UnknownAccountException();
        } else {
            String permissions = user.getRoleModel().getPermissions();
            List<Permission> permissionList = userService.getPermissions(permissions);
            String authcode = user.getAuthcode();
            String joincode = String.valueOf(token.getPassword());
            if (joincode == authcode || joincode.equals(authcode)) {
                Session session = SecurityUtils.getSubject().getSession();
                if(authcode.length() == 6) {
                    String auth = (String) session.getAttribute("authcode");
                    if (auth != null) {
                        user.setAuthcode(auth);
                        userService.bindUser(user);
                        token.setPassword(auth.toCharArray());
                        authcode = auth;
                        session.setAttribute("authcode",null);
                    }
                }
                session.setAttribute("USERID",user.getId());
                session.setAttribute("AREAIDS",user.getArea());
                session.setAttribute("USERROLE",user.getRoleModel().getRoleSign());
                session.setAttribute("USERPERMISSION",permissionList);
                return new SimpleAuthenticationInfo(telphone, authcode, getName());
            } else {
                throw new IncorrectCredentialsException();
            }
        }
    }
}
