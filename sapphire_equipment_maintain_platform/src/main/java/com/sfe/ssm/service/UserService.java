package com.sfe.ssm.service;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.model.Permission;
import com.sfe.ssm.model.User;

import java.util.List;

public interface UserService {

    List<User> getAreaWorker(int areaid);

    User getUserById(int id);

    User selectUserByName(String name);

    User getUserByTel(String telphone);

    User getUserByAuth(String auth);

    String getAuthcode(String telphone);

    int createUser(User user);

    int updateUser(User user);

    int bindUser(User user);

    int logintimeUser(User user);

    int addArea(int aid, int id);

    int addUnmark1(int id, int count);

    int updateUnmark1(int id, int count);

    int addUnmark2(int id);

    int addUnmark3(int id);

    int deleteUser(int id);

    boolean isExistPhoneNumber(User user);

    PageInfo selectByPageList(String areaIds, Integer pageNum, Integer pageSize);

    PageInfo getPageInfoByINTArea(String areaIds, String pickRoles, Integer pageNum, Integer pageSize);

    List<Permission> getPermissions(String permissions);
}
