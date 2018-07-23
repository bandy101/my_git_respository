package com.sfe.ssm.dao;


import com.sfe.ssm.model.Repair;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RepairDao {

    Repair getRepairById(@Param("id") int id);

    Repair getRepairInfoById(@Param("id") int id);

    int createRepair(Repair dev);

    int updateRepair(Repair dev);

    int fillinRepair(Repair dev);

    int finishRepair(Repair dev);

    int deleteRepair(@Param("id") int id);

    List<Repair> selectByPageList(@Param("areaIds") String areaIds , @Param("workerId") String workerId , @Param("type") int type);

}
