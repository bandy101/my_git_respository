package com.sfe.ssm.dao;


import com.sfe.ssm.model.Equipment;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public interface EquipmentDao {

    Equipment getEquipmentById(@Param("id") int id);

    Equipment getEquipmentByCode(@Param("code") String code);

    Equipment getEquipmentAssign(@Param("id") int id);

    int createEquipment(Equipment equipment);

    int updateEquipment(Equipment equipment);

    int deleteEquipment(@Param("id") int id);

    int isExistEquipment(Equipment equipment);

    List<String> selectNameList(@Param("eids") String eids);

    List<Equipment> selectByPageList(@Param("areaIds") String areaIds);

    List<Equipment> selectByAreaid(@Param("aid") int aid);

    List<Equipment> selectAreaEquipmentLocation(@Param("areaIds") String areaIds);

    List<Equipment> selectAirEquipmentLocation(@Param("areaIds") String areaIds);

    List<Equipment> selectEquipmentLocation();

    int getCountInArea(@Param("areaIds") String areaIds);

    Map getAirInArea(@Param("areaIds") String areaIds);

}
