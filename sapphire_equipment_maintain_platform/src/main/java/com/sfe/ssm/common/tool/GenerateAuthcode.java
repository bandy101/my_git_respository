package com.sfe.ssm.common.tool;


/**
 * @Author： 谢粦耀
 * @Date： 2017/12/14 14:44
 * @Description： 随机生成6位随机字母数字的验证码/邀请码
 */
public class GenerateAuthcode {
    public static String randomAuthcode(){

        String model = "abcdefghijklmnopqrstuvwxyz0123456789";
        char[] m = model.toCharArray();     //拆成字符数组

        StringBuilder s = new StringBuilder();
        for (int i = 0; i < 6; ++i) {
            char c = m[(int) (Math.random() * model.length())];
            s.append(c);
        }
        //System.out.println(s);
        return s.toString();
    }
}
