package com.sfe.ssm.common.tool;

import java.util.Random;

/**
 * @author 廖志群
 * @version 1.00
 * @date 八月  22 2017,9:35
 * 数学功能函数
 */
public class MathHelper {

    /**
     * 随机数生成
     * @return
     */
    public static int numRandom(){
        int max=2000;
        int min=10;
        Random random = new Random();

        int s = random.nextInt(max)%(max-min+1) + min;
        return s;
    }

    /**
     * 随机数生成
     * @return
     */
    public static int numRandom(int min,int max){
        Random random = new Random();

        int s = random.nextInt(max)%(max-min+1) + min;
        return s;
    }

}
