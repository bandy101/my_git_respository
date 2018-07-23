package com.sfe.ssm.controller;

import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.common.version.ApiVersion;
import com.sfe.ssm.model.Task;
import com.sfe.ssm.quartz.QuartzManager;
import com.sfe.ssm.quartz.achieve.MyJob;
import com.sfe.ssm.service.TaskService;

import org.quartz.Job;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;


/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  17 2017,15:54
 * 定时任务控制器
 */
@RestController
@RequestMapping(value = "/api/{version}/quartz/")
public class QuartzApiController {

    // 定时器
    /**
     * 任务名
     */
    public static String JOB_NAME = "动态任务调度";
    /**
     * 任务组名
     */
    public static String JOB_GROUP_NAME = "XLXXCC_JOB_GROUP";
    /**
     * 触发器名
     */
    public static String TRIGGER_NAME = "动态任务触发器";
    /**
     * 触发器组名
     */
    public static String TRIGGER_GROUP_NAME = "XLXXCC_JOB_GROUP";

    @Autowired TaskService taskService;
    @Resource
    private QuartzManager quartzManager;

    @RequestMapping(value = "integrated/", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg addQuartz() {

        try {
            System.out.println("【系统启动】开始(每1秒输出一次)...");
            quartzManager.addJob(MyJob.class, JOB_NAME, JOB_GROUP_NAME, TRIGGER_NAME, TRIGGER_GROUP_NAME, "0/1 * * * * ?");

            Thread.sleep(5000);
            System.out.println("【修改时间】开始(每5秒输出一次)...");
            quartzManager.modifyJobTime(JOB_NAME, JOB_GROUP_NAME, TRIGGER_NAME, TRIGGER_GROUP_NAME, "0/5 * * * * ?");

            Thread.sleep(6000);
            System.out.println("【移除定时】开始...");
            quartzManager.removeJob(JOB_NAME, JOB_GROUP_NAME, TRIGGER_NAME, TRIGGER_GROUP_NAME);
            System.out.println("【移除定时】成功");
        } catch (Exception e) {
            e.printStackTrace();
        }

        ResultMsg resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }


    /**
     * 动态添加定时任务类
     *
     * @param task
     * @return
     */
    @RequestMapping(value = "task/", method = RequestMethod.POST, consumes = "application/json", produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg addTask(@RequestBody Task task) {
        ResultMsg resultMsg;
        try {
            quartzManager.addJob((Class<? extends Job>) (Class.forName(task.getJobClass()).newInstance().getClass()),
                    task.getJobName(), task.getJobGroupName(), task.getTriggerName(), task.getTriggerGroupName(), task.getCron());
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }

    /**
     * 修改动态定时任务类
     *
     * @param id
     * @param
     * @return
     */
    @RequestMapping(value = "task/{id}", method = RequestMethod.PUT, consumes = "application/json", produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg updateTask(@PathVariable("id") long id) {
        ResultMsg resultMsg;
        try {
            Task task = taskService.getTaskById(id);
            quartzManager.modifyJobTime(task.getJobName(), task.getJobGroupName(), task.getTriggerName(),
                    task.getTriggerGroupName(), task.getCron());
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }

    /**
     * 删除动态定时任务类
     *
     * @param id
     * @return
     */
    @RequestMapping(value = "Task/{id}", method = RequestMethod.DELETE, consumes = "application/json")
    @ApiVersion(1)
    public ResultMsg deleteTask(@PathVariable("id") long id) {
        ResultMsg resultMsg;
        try {
            Task task = taskService.getTaskById(id);
            quartzManager.removeJob(task.getJobName(), task.getJobGroupName(), task.getTriggerName(), task.getTriggerGroupName());
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }


    /**
     * 动态添加定时任务类-毫秒
     *
     * @param task
     * @return
     */
    @RequestMapping(value = "task/simple/", method = RequestMethod.POST, consumes = "application/json", produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg addSimpleTask(@RequestBody Task task) {
        ResultMsg resultMsg;
        try {
            quartzManager.addJob((Class<? extends Job>) (Class.forName(task.getJobClass()).newInstance().getClass()),
                    task.getJobName(), task.getJobGroupName(), task.getTriggerName(), task.getTriggerGroupName(), Integer.parseInt(task.getCron()));

        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }

    /**
     * 修改动态定时任务类-毫秒
     *
     * @param id
     * @return
     */
    @RequestMapping(value = "task/simple/{id}", method = RequestMethod.PUT, consumes = "application/json", produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg updateSimpleTask(@PathVariable("id") long id) {
        ResultMsg resultMsg;
        try {
            Task task = taskService.getTaskById(id);
            quartzManager.modifyJobTime(task.getJobName(), task.getJobGroupName(), task.getTriggerName(),
                    task.getTriggerGroupName(), Integer.parseInt(task.getCron()));
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }

    /**
     * 暂停一个定时器
     *
     * @return
     */
    @RequestMapping(value = "task/pause/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg pauseJob(@PathVariable("id") long id) {
        ResultMsg resultMsg;
        try {
            Task task = taskService.getTaskById(id);
            quartzManager.pauseJob(task.getJobName(), task.getJobGroupName());
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }

    /**
     * 恢复一个定时器
     *
     * @return
     */
    @RequestMapping(value = "task/resume/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg resumeJob(@PathVariable("id") long id) {
        ResultMsg resultMsg;
        try {
            Task task = taskService.getTaskById(id);
            quartzManager.resumeJob(task.getJobName(), task.getJobGroupName());
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }

    /**
     * 立即执行一个定时器 只运行一次
     *
     * @return
     */
    @RequestMapping(value = "task/runnow/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg runAJobNow(@PathVariable("id") long id) {
        ResultMsg resultMsg;
        try {
            Task task = taskService.getTaskById(id);
            quartzManager.runAJobNow(task.getJobName(), task.getJobGroupName());
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), "ok");

        return resultMsg;
    }

    /**
     * 获取所有计划中的任务列表
     *
     * @return
     */
    @RequestMapping(value = "task/all", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg queryAllJob() {
        ResultMsg resultMsg;
        List<Map<String, Object>> lstMap;
        try {
            lstMap = quartzManager.queryAllJob();
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstMap);

        return resultMsg;
    }

    /**
     * 获取所有正在运行的job
     *
     * @return
     */
    @RequestMapping(value = "task/run", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    @ApiVersion(1)
    public ResultMsg queryRunJon() {
        ResultMsg resultMsg;
        List<Map<String, Object>> lstMap;
        try {
            lstMap = quartzManager.queryRunJon();
        } catch (Exception e) {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), e.getMessage());
            return resultMsg;
        }

        resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                ResultStatusCode.OK.getErrmsg(), lstMap);

        return resultMsg;
    }

}
