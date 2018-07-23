package com.sfe.ssm.common.cache;

import org.apache.log4j.Logger;

import java.io.*;

/**
 * @author 廖志群
 * @version 1.00
 * @date 七月  11 2017,8:55
 *
 * 序列化和反序列化工具 redis操作服务专用
 */
public class SerializeUtil
{
    /**
     * 添加一个日志器
     */
    private static final Logger logger = Logger.getLogger(SerializeUtil.class);

    /**
     * 序列化
     *
     * @param object
     * @return
     */
    public static byte[] serialize(Object object)
    {
        byte[] bytes = null;
        if (object != null)
        {
            ObjectOutputStream oos = null;
            ByteArrayOutputStream baos = null;
            try
            {
                // 序列化
                baos = new ByteArrayOutputStream();
                oos = new ObjectOutputStream(baos);
                oos.writeObject(object);
                bytes = baos.toByteArray();
            }
            catch (Exception e)
            {
                e.printStackTrace();
                logger.error("序列化出现异常：", e);

            }
            finally
            {
                close(oos);
                close(baos);
            }
        }
        return bytes;
    }

    /**
     * 反序列化
     *
     * @param bytes
     * @return Object
     */
    public static Object unserialize(byte[] bytes)
    {
        Object returnObject = new Object();
        if (bytes != null)
        {
            ByteArrayInputStream bais = null;
            ObjectInputStream ois = null;
            try
            {
                // 反序列化
                bais = new ByteArrayInputStream(bytes);
                ois = new ObjectInputStream(bais);
                returnObject = ois.readObject();
            }
            catch (Exception e)
            {
                e.printStackTrace();
                logger.error("反序列化出现异常：", e);
            }
            finally
            {
                close(bais);
                close(ois);
            }
        }
        else
        {
            returnObject = null;
        }

        return returnObject;
    }

    /**
     * 关闭io流对象
     *
     * @param closeable
     */
    public static void close(Closeable closeable)
    {
        if (closeable != null)
        {
            try
            {
                closeable.close();
            }
            catch (Exception e)
            {
                e.printStackTrace();
                logger.error("关闭io流对象出现异常：", e);
            }
        }
    }

}
