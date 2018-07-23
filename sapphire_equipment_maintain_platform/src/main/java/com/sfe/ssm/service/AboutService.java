package com.sfe.ssm.service;


import com.sfe.ssm.model.About;


/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:15
 */
public interface AboutService {

    /**
     *获取关于信息
     * @param id
     * @return
     */
    About getAboutById(Long id);


}

