package com.sfe.ssm.dao;

import com.sfe.ssm.model.Detection;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.Date;
import java.util.List;

@Repository
public interface DetectionDao {

    int getCountForWorker(@Param("wid") int id);

    List<Detection> getDetectionPageList(@Param("wid") int id,@Param("already") boolean already);

    List<Detection> getAreaMonthDetectionList(@Param("aid") int id);

    List<Detection> getAreaWeekDetectionList(@Param("aid") int id , @Param("date") String date);

    List<Integer> getMonthDetectionNums(@Param("areaIds") String areaIds);

    List<Integer> getWeekDetectionNums(@Param("areaIds") String areaIds);

    List<Integer> getWeekAssigneEqu(@Param("areaIds") String areaIds);

    Detection getDetectionById(@Param("id") int id);

    Detection getWeekDetectionById(@Param("eid") int eid);

    Detection getMonthDetectionById(@Param("eid") int eid);

    int createDetection(Detection detection);

    int fillinDetection(Detection detection);

    int deleteDetection(@Param("id") int id);

    int finishDetection(Detection detection);

}
