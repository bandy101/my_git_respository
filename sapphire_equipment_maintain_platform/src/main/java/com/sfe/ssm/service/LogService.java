package com.sfe.ssm.service;

import com.sfe.ssm.model.Log;


import java.util.List;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  24 2017,16:29
 */
public interface LogService {

    /**
     * ssss
     * @param logId
     * @return
     */
    Log selectLogById(Long logId);

    /**
     * ssss
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
