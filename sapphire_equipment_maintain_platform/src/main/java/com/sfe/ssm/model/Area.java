package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

@Getter
@Setter
public class Area implements Serializable {

    private int id;

    private String name;

    private Date createtime;

    private boolean auth;

    private List<Equipment> equipmentList;

}
