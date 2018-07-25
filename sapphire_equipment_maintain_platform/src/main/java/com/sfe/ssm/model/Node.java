package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
public class Node {

    private int id;

    private String parties;

    private String content;

    private Date nodetime;

    private String ordernum;

    private String imgurl;


}
