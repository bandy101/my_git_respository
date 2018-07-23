package com.sfe.ssm.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;

import com.sfe.ssm.dao.AreaDao;
import com.sfe.ssm.model.Area;
import com.sfe.ssm.service.AreaService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service("areaService")
public class AreaServiceImpl implements AreaService {

    @Resource
    AreaDao areaDao;

    @Override
    public Area getAreaById(int id) {

        return areaDao.getAreaById(id);
    }

    @Override
    public int createArea(Area area) {

        return areaDao.createArea(area);
    }

    @Override
    public int updateArea(Area area) {

        return areaDao.updateArea(area);
    }

    @Override
    public int deleteArea(int id) {

        return areaDao.deleteArea(id);
    }

    @Override
    public PageInfo selectByPageList(String areaIds, Integer pageNum, Integer pageSize) {

        PageHelper.startPage(pageNum,pageSize);
        List<Area> listData = areaDao.selectByPageList(areaIds);
        PageInfo page = new PageInfo(listData);
        return page;
    }

    @Override
    public List<Area> getAreaList(String areaIds) {
        return areaDao.getAreaList(areaIds);
    }

    @Override
    public List<Area> getAreaEquipmentList(String areaIds) {
        return areaDao.getAreaEquipmentList(areaIds);
    }

    @Override
    public List<Area> getAreaAirEquipmentList(String areaIds) {
        return areaDao.getAreaAirEquipmentList(areaIds);
    }
}
