package com.sfe.ssm.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.sfe.ssm.dao.DetectionDao;
import com.sfe.ssm.model.Detection;
import com.sfe.ssm.service.DetectionService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.Date;
import java.util.List;

@Service("detectionService")
public class DetectionServiceImpl implements DetectionService {

    @Resource
    DetectionDao detectionDao;

    @Override
    public int getCountForWorker(int wid) {
        return detectionDao.getCountForWorker(wid);
    }

    @Override
    public PageInfo getDetectionPageList(int wid, boolean already, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum,pageSize);
        List<Detection> listData = detectionDao.getDetectionPageList(wid , already);
        PageInfo page = new PageInfo(listData);
        return page;
    }

    @Override
    public PageInfo getAreaMonthDetectionList(int id, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum,pageSize);
        List<Detection> listData = detectionDao.getAreaMonthDetectionList(id);
        PageInfo page = new PageInfo(listData);
        return page;
    }

    @Override
    public PageInfo getAreaWeekDetectionList(int id, String date, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum,pageSize);
        List<Detection> listData = detectionDao.getAreaWeekDetectionList(id , date);
        PageInfo page = new PageInfo(listData);
        return page;
    }

    @Override
    public List<Integer> getMonthDetectionNums(String areaIds) {
        return detectionDao.getMonthDetectionNums(areaIds);
    }

    @Override
    public List<Integer> getWeekDetectionNums(String areaIds) {
        return detectionDao.getWeekDetectionNums(areaIds);
    }

    @Override
    public List<Integer> getWeekAssigneEqu(String areaIds) {
        return detectionDao.getWeekAssigneEqu(areaIds);
    }

    @Override
    public Detection getDetectionById(int id) {
        return detectionDao.getDetectionById(id);
    }

    @Override
    public Detection getWeekDetectionById(int eid) {
        return detectionDao.getWeekDetectionById(eid);
    }

    @Override
    public Detection getMonthDetectionById(int eid) {
        return detectionDao.getMonthDetectionById(eid);
    }

    @Override
    public int createDetection(Detection detection) {
        return detectionDao.createDetection(detection);
    }

    @Override
    public int fillinDetection(Detection detection) {
        return detectionDao.fillinDetection(detection);
    }

    @Override
    public int deleteDetection(int id) {
        return detectionDao.deleteDetection(id);
    }

    @Override
    public int finishDetection(Detection detection) {
        return detectionDao.finishDetection(detection);
    }
}
