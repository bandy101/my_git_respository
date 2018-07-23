package com.sfe.ssm.service;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.model.Area;

import java.util.List;

public interface AreaService {

    Area getAreaById(int id);

    int createArea(Area area);

    int updateArea(Area area);

    int deleteArea(int id);

    PageInfo selectByPageList(String areaIds, Integer pageNum, Integer pageSize);

    List<Area> getAreaList(String areaIds);

    List<Area> getAreaEquipmentList(String areaIds);

    List<Area> getAreaAirEquipmentList(String areaIds);

}
