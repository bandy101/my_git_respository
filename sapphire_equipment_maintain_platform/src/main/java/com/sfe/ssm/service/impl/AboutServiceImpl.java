package com.sfe.ssm.service.impl;


import com.sfe.ssm.dao.AboutDao;
import com.sfe.ssm.model.About;
import com.sfe.ssm.service.AboutService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import javax.annotation.Resource;


/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:14
 */
@Service
@Transactional(rollbackFor = Exception.class)
public class AboutServiceImpl implements AboutService {

    @Resource
    private AboutDao aboutDao;


    @Override
    public About getAboutById(Long id) {
        return aboutDao.selectById(id);
    }


}

