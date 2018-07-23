package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.Date;

@Getter
@Setter
public class Equipment implements Serializable {

    private int id;

    private String name;

    private String code;

    private String airCode;

    private int areaId;

    private String location;

    private String address;

    private Date createtime;

    private String areaName;

    private String monthPassCount;

    private String monthNopassCount;

    private String passCount;

    private String nopassCount;

    private String insideTemperature;

    private String insideHumidity;

    private String withoutTemperature;

    private String withoutHumidity;

    private int[] timeLabel;

    private int[] uvIntenHr;

    private int[] irIntenHr;

}
