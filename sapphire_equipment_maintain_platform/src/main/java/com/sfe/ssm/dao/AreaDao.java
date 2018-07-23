package com.sfe.ssm.dao;


import com.sfe.ssm.model.Area;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AreaDao {

    Area getAreaById(@Param("id") int id);

    int createArea(Area area);

    int updateArea(Area area);

    int deleteArea(@Param("id") int id);

    List<Area> selectByPageList(@Param("areaIds") String areaIds);

    List<Area> getAreaList(@Param("areaIds") String areaIds);

    List<Area> getAreaEquipmentList(@Param("areaIds") String areaIds);

    List<Area> getAreaAirEquipmentList(@Param("areaIds") String areaIds);

}
