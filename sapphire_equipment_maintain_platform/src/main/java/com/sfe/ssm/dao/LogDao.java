package com.sfe.ssm.dao;

import com.sfe.ssm.model.Log;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;


/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  24 2017,16:26
 */
@Repository
public interface LogDao {

    /**
     *
     * @param logId
     * @return
     */
    Log selectLogById(@Param("logId") Long logId);

    /**
     *
     * @return
     */
    List<Log> selectAllLog();

    /**
     *
     * @param log
     * @return
     */
    int insert(Log log);

    /**
     *
     * @param log
     * @return
     */
    int update(Log log);

    /**
     *
     * @param id
     * @return
     */
    int delete(int id);

}
