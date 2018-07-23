package com.sfe.ssm.service.impl;

import com.sfe.ssm.dao.LogDao;
import com.sfe.ssm.model.Log;
import com.sfe.ssm.service.LogService;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.List;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:14
 */
@Service
@Transactional(rollbackFor = Exception.class)
public class LogServiceImpl implements LogService {

    @Resource
    private LogDao logDao;

    @Override
    public Log selectLogById(@Param("logId") Long logId){
        return logDao.selectLogById(logId);
    }

    @Override
    public List<Log> selectAllLog(){
        return logDao.selectAllLog();
    }

    @Override
    public int insert(Log log){
        return logDao.insert(log);
    }

    @Override
    public int update(Log log){
        return logDao.update(log);
    }

    @Override
    public int delete(int logId){
        return logDao.delete(logId);
    }


}

