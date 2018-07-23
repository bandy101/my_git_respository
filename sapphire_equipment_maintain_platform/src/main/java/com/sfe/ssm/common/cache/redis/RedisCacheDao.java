package com.sfe.ssm.common.cache.redis;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  11 2017,8:52
 * redis的dao层接口
 */
public interface RedisCacheDao
{
    /**
     * 根据key存储object
     *
     * @param key 键
     * @param value 要存储的对象Object
     * @return boolean 存储成功或失败的标志
     * ***/
      boolean saveObject(String key, Object value);

    /**
     * 根据key获取object
     *
     * @param key 键
     * @return Object 与key对应的object
     * ***/
      Object getObject(String key);


    /**
     * 根据key删除数据
     *
     * @param key 键
     * @return boolean 删除成功或失败的标志
     * ***/
      boolean deleteKey(String key);
}
