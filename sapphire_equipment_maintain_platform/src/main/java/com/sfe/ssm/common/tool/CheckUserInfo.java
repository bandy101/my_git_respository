//package com.sfe.ssm.common.tool;
//
//import com.sfe.ssm.model.User;
//import com.sfe.ssm.service.UserService;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.stereotype.Component;
//
//import java.util.List;
//
///**
// * @Author： 谢粦耀
// * @Date： 2017/12/13 11:24
// * @Description： 用户信息检查
// */
//@Component
//public class CheckUserInfo {
//    @Autowired
//    private UserService userService ;
//
//    /**
//     * 判断用户的telphone是否与数据库中其它用户重复
//     * @param userUUT
//     * @return boolean 重复则返回true
//     */
//    public boolean isDuplicateMobileNumber(User userUUT) {
//        List<User> allUser = userService.getAllUser();
//        for (User anAllUser : allUser) {
//            if (anAllUser.getTelphone().equals(userUUT.getTelphone())) { //若号码相同
//                return true;
//            }
//        }
//        return false;
//    }
//
//}
