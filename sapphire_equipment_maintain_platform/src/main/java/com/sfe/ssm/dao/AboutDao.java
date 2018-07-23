package com.sfe.ssm.dao;

import com.sfe.ssm.model.About;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;


/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:07
 */
@Repository
public interface AboutDao {

    /**
     * 获取关于信息
     * @param id
     * @return
     */
    About selectById(@Param("id") Long id);


}