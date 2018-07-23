package com.sfe.ssm.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;

import com.sfe.ssm.dao.UserDao;
import com.sfe.ssm.model.Permission;
import com.sfe.ssm.model.User;
import com.sfe.ssm.service.UserService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service("userService")
public class UserServiceImpl implements UserService {
    @Resource
    private UserDao userDao;

    @Override
    public List<User> getAreaWorker(int areaid) {
        return userDao.getAreaWorker(areaid);
    }

    @Override
    public User getUserById(int id) {

        return userDao.getUserById(id);
    }

    @Override
    public User selectUserByName(String name) {
        return userDao.selectUserByName(name);
    }

    @Override
    public User getUserByTel(String telphone) {
        return userDao.getUserByTel(telphone);
    }

    @Override
    public User getUserByAuth(String auth) {
        return userDao.getUserByAuth(auth);
    }

    @Override
    public String getAuthcode(String telphone) {

        return userDao.getAuthcode(telphone);
    }

    @Override
    public int createUser(User user) {

        return userDao.createUser(user);
    }

    @Override
    public int updateUser(User user) {
        return userDao.updateUser(user);
    }

    @Override
    public int bindUser(User user) {
        return userDao.bindUser(user);
    }

    @Override
    public int logintimeUser(User user) {
        return userDao.logintimeUser(user);
    }

    @Override
    public int addArea(int aid, int id) {
        return userDao.addArea(aid, id);
    }

    @Override
    public int addUnmark1(int id, int count) {
        return userDao.addUnmark1(id, count);
    }

    @Override
    public int updateUnmark1(int id, int count) {
        return userDao.updateUnmark1(id, count);
    }

    @Override
    public int addUnmark2(int id) {
        return userDao.addUnmark2(id);
    }

    @Override
    public int addUnmark3(int id) {
        return userDao.addUnmark3(id);
    }

    @Override
    public int deleteUser(int id) {

        return userDao.deleteUser(id);
    }

    /**
     * 判断传入用户联系电话是否在数据库中已重复
     * @param user ----UUT
     * @return boolean 重复则返回true
     */
    @Override
    public boolean isExistPhoneNumber(User user){
        int ret = userDao.isExistPhoneNumber(user);
        return ret != 0;
    }

    @Override
    public PageInfo selectByPageList(String areaIds, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum,pageSize);
        List<User> listData = userDao.selectByPageList(areaIds);
        return new PageInfo(listData);
    }

    @Override
    public PageInfo getPageInfoByINTArea(String areaIds, String pickRoles, Integer pageNum, Integer pageSize){
        PageHelper.startPage(pageNum, pageSize);
        List<User> listData = userDao.getUsersByIntersectionArea(areaIds, pickRoles);
        return new PageInfo(listData);
    }

    @Override
    public List<Permission> getPermissions(String permissions) {
        return userDao.getPermissions(permissions);
    }
}
