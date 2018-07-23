package com.sfe.ssm.service;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.model.Detection;

import java.util.Date;
import java.util.List;

public interface DetectionService {

    int getCountForWorker(int wid);

    PageInfo getDetectionPageList(int wid, boolean already, Integer pageNum, Integer pageSize);

    PageInfo getAreaMonthDetectionList(int id, Integer pageNum, Integer pageSize);

    PageInfo getAreaWeekDetectionList(int id, String date, Integer pageNum, Integer pageSize);

    List<Integer> getMonthDetectionNums(String areaIds);

    List<Integer> getWeekDetectionNums(String areaIds);

    List<Integer> getWeekAssigneEqu(String areaIds);

    Detection getDetectionById(int id);

    Detection getWeekDetectionById(int eid);

    Detection getMonthDetectionById(int eid);

    int createDetection(Detection detection);

    int fillinDetection(Detection detection);

    int deleteDetection(int id);

    int finishDetection(Detection detection);

}
