package com.sfe.ssm.util;

import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 2017-12-20 JoeLyZH
 * 基础工具类
 */
@Service("BaseToolUtil")
public class BaseToolUtil {

    /**
     * 字符串数组拼接分隔符
     * @param join
     * @param list
     * @return
     */
    public String joinByList(String join , List<String> list){
        String joinstr = "";
        for (String str:list) {
            joinstr += str+join;
        }
        if (joinstr!=""){
            joinstr = joinstr.substring(0,joinstr.length()-1);
        }
        return joinstr;
    }

    /**
     * 整型数组拼接分隔符
     * @param join
     * @param list
     * @return
     */
    public String joinByIntList(String join , List<Integer> list){
        String joinstr = "";
        for (int str:list) {
            joinstr += str+join;
        }
        if (joinstr!=""){
            joinstr = joinstr.substring(0,joinstr.length()-1);
        }
        return joinstr;
    }

    /**
     * 数组中查询该值是否存在
     * @param id
     * @param strs
     * @return
     */
    public boolean findByList(int id , String[] strs){

        for (String areaid:strs) {
            if (Integer.parseInt(areaid) == id){
                return true;
            }
        }
        return false;
    }

}
