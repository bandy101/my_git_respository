package com.sfe.ssm.dao;

import com.sfe.ssm.model.Task;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:07
 *
 */
@Repository
public interface TaskDao {

    /**
     *
     * @param taskId
     * @return
     */
    Task selectTaskById(@Param("taskId") Long taskId);

    /**
     *
     * @param jobName
     * @return
     */
    Task selectTaskByName(@Param("jobName") String jobName);

    /**
     *
     * @return
     */
    List<Task> selectAllTask();

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
    int update(Task task);

    /**
     *
     * @param id
     * @return
     */
    int delete(int id);
}