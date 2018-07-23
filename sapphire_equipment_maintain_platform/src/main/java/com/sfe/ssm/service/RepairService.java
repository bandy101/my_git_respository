package com.sfe.ssm.service;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.model.Repair;

public interface RepairService {

    Repair getRepairById(int id);

    Repair getRepairInfoById(int id);

    int createRepair(Repair dev);

    int updateRepair(Repair dev);

    int fillinRepair(Repair dev);

    int finishRepair(Repair dev);

    int deleteRepair(int id);

    PageInfo selectByPageList(String areaIds, String workerId, Integer type, Integer pageNum, Integer pageSize);
}
