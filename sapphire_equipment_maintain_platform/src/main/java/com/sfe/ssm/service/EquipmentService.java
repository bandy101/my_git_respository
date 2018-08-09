package com.sfe.ssm.service;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.model.Equipment;

import java.util.List;
import java.util.Map;


public interface EquipmentService {

    Equipment getEquipmentById(int id);

    Equipment getEquipmentByCode(String code);

    Equipment getEquipmentAssign(int id);

    int createEquipment(Equipment equipment);

    int updateEquipment(Equipment equipment);

    int deleteEquipment(int id);

    boolean isExistEquipment(Equipment equipment);

    List<String> selectNameList(String eids);

    PageInfo selectByPageList(String areaIds, Integer pageNum, Integer pageSize);

    List<Equipment> selectByAreaid(int aid);

    List<Equipment> selectAreaEquipmentLocation(String areaIds);

    List<Equipment> selectAirEquipmentLocation(String areaIds);

    List<Equipment> selectEquipmentLocation();

    int getCountInArea(String areaIds);

    Map getAirInArea(String areaIds);
}
