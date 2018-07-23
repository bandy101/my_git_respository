//package com.sfe.ssm.controller;
//
//
//import com.sfe.ssm.common.*;
//import com.sfe.ssm.common.EncryptionHelper;
//
//import com.sfe.ssm.common.log.SystemLog;
//import com.sfe.ssm.common.oauth.Audience;
//import com.sfe.ssm.common.oauth.JwtHelper;
//import com.sfe.ssm.common.version.ApiVersion;
//import com.sfe.ssm.model.*;
//
//import com.sfe.ssm.common.oauth.AccessToken;
//import com.sfe.ssm.service.UserService;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.http.MediaType;
//import org.springframework.web.bind.annotation.*;
//
//import javax.annotation.Resource;
//
//
///**
// * @author 廖志群
// * @version 1.00
// * @date 五月  17 2017,14:14
// * 令牌认证控制器
// */
//@RestController
//@RequestMapping(value = "/api/{version}/")
//public class AuthenticationController {
//
//
//    @Autowired
//    private Audience audienceEntity;
//
//    @Resource
//    private UserService userService;
//
//
//    /**
//     * 获取访问令牌
//     * @param loginPara
//     * @return
//     */
//    @RequestMapping(value = "/oauth/token",method = RequestMethod.POST,consumes = "application/json",
//            produces = MediaType.APPLICATION_JSON_VALUE)
//    @ApiVersion(1)
//    @SystemLog(module = "认证控制",methods = "获取访问令牌")
//    public Object getAccessToken(@RequestBody LoginPara loginPara)
//    {
//        ResultMsg resultMsg;
//        try
//        {
//            if(loginPara.getClientId() == null
//                    || (loginPara.getClientId().compareTo(audienceEntity.getClientId()) != 0))
//            {
//                resultMsg = new ResultMsg(ResultStatusCode.INVALID_CLIENTID.getErrcode(),
//                        ResultStatusCode.INVALID_CLIENTID.getErrmsg(), null);
//                return resultMsg;
//            }
//
//            //验证用户名密码
//            User user = userService.getUserByName(loginPara.getUserName());
//            if (user == null)
//            {
//                resultMsg = new ResultMsg(ResultStatusCode.INVALID_PASSWORD.getErrcode(),
//                        ResultStatusCode.INVALID_PASSWORD.getErrmsg(), null);
//                return resultMsg;
//            }
//            else
//            {
//                String md5Password = EncryptionHelper.getMD5(loginPara.getPassword()+user.getId());//.getSalt()
//
//                if (md5Password.compareTo(user.getUserPwd()) != 0)
//                {
//                    resultMsg = new ResultMsg(ResultStatusCode.INVALID_PASSWORD.getErrcode(),
//                            ResultStatusCode.INVALID_PASSWORD.getErrmsg(), null);
//                    return resultMsg;
//                }
//            }
//
//            //拼装accessToken
//            String accessToken = JwtHelper.createJWT(loginPara.getUserName(), String.valueOf(user.getId()),
//                    user.getUserPhone(), audienceEntity.getClientId(), audienceEntity.getName(),//user.getRole(), audienceEntity.ClientId, audienceEntity.Name,
//                    audienceEntity.getExpiresSecond() * 1000, audienceEntity.getBase64Secret());
//
//            //返回accessToken
//            AccessToken accessTokenEntity = new AccessToken();
//            accessTokenEntity.setAccessToken(accessToken);
//            accessTokenEntity.setExpiresIn(audienceEntity.getExpiresSecond());
//            accessTokenEntity.setTokenType("bearer");
//            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
//                    ResultStatusCode.OK.getErrmsg(), accessTokenEntity);
//            return resultMsg;
//
//        }
//        catch(Exception ex)
//        {
//            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
//                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), null);
//            return resultMsg;
//        }
//    }
//
//
//
//
//
//
//
//
//
//
//}
