package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

@Getter
@Setter
public class User implements Serializable {

    private int id;

    private String name;

    private String telphone;

    private String authcode;

    private String address;

    private String touimg;

    private String area;

    private Date jointime;

    private Date logintime;

    private int role;

    private int unmark1;

    private int unmark2;

    private int unmark3;

    private Role roleModel;

    private List<Permission> permissionModel;

    private String areaname;

}
