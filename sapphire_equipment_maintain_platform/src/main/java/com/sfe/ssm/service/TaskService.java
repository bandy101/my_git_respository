package com.sfe.ssm.service;

import com.sfe.ssm.model.Task;

import java.util.List;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:15
 */
public interface TaskService {

    /**
     *
     * @return
     */
    List<Task> getAllTask();

    /**
     *
     * @param jobName
     * @return
     */
    Task getTaskByName(String jobName);

    /**
     *
     * @param taskId
     * @return
     */
    Task getTaskById(Long taskId);

    /**
     *
     * @param task
     * @return
     */
    int insert(Task task);

    /**
     *
     * @param task
     * @return
     */
    int updateTask(Task task);

    /**
     *
     * @param taskId
     * @return
     */
    int deleteTaskById(int taskId);
}

