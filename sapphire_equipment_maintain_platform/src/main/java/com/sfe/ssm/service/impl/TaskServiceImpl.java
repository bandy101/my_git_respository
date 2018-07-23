package com.sfe.ssm.service.impl;

import com.sfe.ssm.dao.TaskDao;
import com.sfe.ssm.model.Task;
import com.sfe.ssm.service.TaskService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.List;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:14
 */
@Service
@Transactional(rollbackFor = Exception.class)//配置事务 发生Exception异常了，就进行回滚
//@Transactional(readOnly = true)
public class TaskServiceImpl implements TaskService {

    @Resource
    private TaskDao taskDao;

    @Override
    public Task getTaskById(Long taskId) {
        return taskDao.selectTaskById(taskId);
    }

    @Override
    public Task getTaskByName(String jobName) {
        return taskDao.selectTaskByName(jobName);
    }

    @Override
    public List<Task> getAllTask() {
        return taskDao.selectAllTask();
    }

    @Override
    public int insert(Task task){
        return taskDao.insert(task);
    }

    @Override
    public int updateTask(Task task){
        return taskDao.update(task);
    }

    @Override
    public int deleteTaskById(int taskId){
        return taskDao.delete(taskId);
    }

}

