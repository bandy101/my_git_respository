package com.sfe.ssm.dao;


import com.sfe.ssm.model.Permission;
import com.sfe.ssm.model.User;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserDao {

    List<User> getAreaWorker(@Param("areaid") int areaid);

    User getUserById(@Param("id") int id);

    User selectUserByName(@Param("name") String name);

    User getUserByTel(@Param("telphone") String telphone);

    User getUserByAuth(@Param("auth") String auth);

    String getAuthcode(@Param("telphone") String telphone);

    int createUser(User user);

    int updateUser(User user);

    int bindUser(User user);

    int logintimeUser(User user);

    int addArea(@Param("aid") int aid, @Param("id") int id);

    int addUnmark1(@Param("id") int id, @Param("count") int count);

    int updateUnmark1(@Param("id") int id, @Param("count") int count);

    int addUnmark2(@Param("id") int id);

    int addUnmark3(@Param("id") int id);

    int deleteUser(@Param("id") int id);

    int isExistPhoneNumber(User user);

    List<User> selectByPageList(@Param("areaIds") String areaIds);

    List<User> getUsersByIntersectionArea(@Param("areaIds")String areaIds, @Param("pickRoles")String pickRoles);

    List<Permission> getPermissions(@Param("permissions") String permissions);
}
