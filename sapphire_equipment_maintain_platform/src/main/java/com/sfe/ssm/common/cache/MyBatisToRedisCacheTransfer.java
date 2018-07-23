package com.sfe.ssm.common.cache;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;

/**
 * @author 廖志群
 * @version 1.00
 * @date 六月  29 2017,17:18
 *  静态注入中间类
 */
public class MyBatisToRedisCacheTransfer
{
    @Autowired
    public void setJedisConnectionFactory(JedisConnectionFactory jedisConnectionFactory) {
        MyBatisToRedisCache.setJedisConnectionFactory(jedisConnectionFactory);
    }

}
