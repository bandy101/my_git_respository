package com.sfe.ssm.common.cache.redis;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  11 2017,8:50
 * redis 缓存服务接口
 */
public interface RedisCacheService {

    /**
     * 根据id缓存数据。 参数说明：id和sessionObject不允许为null或空值。 数据库若已存在同名键，则会覆盖掉
     * @param id
     * @param sessionObject
     * @return
     */
     boolean putSessionObject(String id, Object sessionObject);


    /**
     * 根据id删除已缓存的数据。 参数说明：id不允许为null和空值
     * @param id
     * @return
     */
     boolean clearSessionObject(String id);


    /**
     * 根据id获取已缓存的缓存数据。 参数说明：id不允许为null和空值
     * @param id
     * @return
     */
     Object getsessionObject(String id);
}
