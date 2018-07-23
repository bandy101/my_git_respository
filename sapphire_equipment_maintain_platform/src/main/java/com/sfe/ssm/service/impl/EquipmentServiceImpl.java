package com.sfe.ssm.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;

import com.sfe.ssm.dao.EquipmentDao;
import com.sfe.ssm.model.Equipment;
import com.sfe.ssm.service.EquipmentService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service("equipmentService")
public class EquipmentServiceImpl implements EquipmentService {

    @Resource
    EquipmentDao equipmentDao;

    @Override
    public Equipment getEquipmentById(int id) {
        return equipmentDao.getEquipmentById(id);
    }

    @Override
    public Equipment getEquipmentByCode(String code) {
        return equipmentDao.getEquipmentByCode(code);
    }

    @Override
    public Equipment getEquipmentAssign(int id) {
        return equipmentDao.getEquipmentAssign(id);
    }

    @Override
    public int createEquipment(Equipment equipment) {
        return equipmentDao.createEquipment(equipment);
    }

    @Override
    public int updateEquipment(Equipment equipment) {
        return equipmentDao.updateEquipment(equipment);
    }

    @Override
    public int deleteEquipment(int id) {
        return equipmentDao.deleteEquipment(id);
    }

    /**
     * 判断传入参数描述的设备是否在数据库中已重复
     * @param equipment
     * @return boolean 重复则返回true
     */
    @Override
    public boolean isExistEquipment(Equipment equipment){
        int ret = equipmentDao.isExistEquipment(equipment);
        return ret != 0;
    }

    @Override
    public List<String> selectNameList(String eids) {
        return equipmentDao.selectNameList(eids);
    }

    @Override
    public PageInfo selectByPageList(String areaIds, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum,pageSize);
        List<Equipment> listData = equipmentDao.selectByPageList(areaIds);
        PageInfo page = new PageInfo(listData);
        return page;
    }

    @Override
    public List<Equipment> selectByAreaid(int aid) {

        return equipmentDao.selectByAreaid(aid);
    }

    @Override
    public List<Equipment> selectAreaEquipmentLocation(String areaIds) {
        return equipmentDao.selectAreaEquipmentLocation(areaIds);
    }

    @Override
    public List<Equipment> selectAirEquipmentLocation(String areaIds) {
        return equipmentDao.selectAirEquipmentLocation(areaIds);
    }

    @Override
    public List<Equipment> selectEquipmentLocation() {
        return equipmentDao.selectEquipmentLocation();
    }

    @Override
    public int getCountInArea(String areaIds) {
        return equipmentDao.getCountInArea(areaIds);
    }

}
