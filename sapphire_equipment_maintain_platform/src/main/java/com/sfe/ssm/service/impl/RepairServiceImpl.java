package com.sfe.ssm.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;

import com.sfe.ssm.dao.RepairDao;
import com.sfe.ssm.model.Repair;
import com.sfe.ssm.service.RepairService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service("repairService")
public class RepairServiceImpl implements RepairService {
    @Resource
    private RepairDao repairDao;

    @Override
    public Repair getRepairById(int id) {
        return repairDao.getRepairById(id);
    }

    @Override
    public Repair getRepairInfoById(int id) {
        return repairDao.getRepairInfoById(id);
    }

    @Override
    public int createRepair(Repair dev){
        return repairDao.createRepair(dev);
    }

    @Override
    public int updateRepair(Repair dev){
        return repairDao.updateRepair(dev);
    }

    @Override
    public int fillinRepair(Repair dev) {
        return repairDao.fillinRepair(dev);
    }

    @Override
    public int finishRepair(Repair dev) {
        return repairDao.finishRepair(dev);
    }

    @Override
    public int deleteRepair(int id){
        return repairDao.deleteRepair(id);
    }

    @Override
    public PageInfo selectByPageList(String areaIds, String workerId, Integer type, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Repair> listData = repairDao.selectByPageList(areaIds,workerId,type);
        PageInfo page = new PageInfo(listData);
        return page;
    }
}
