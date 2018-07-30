package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

import java.awt.*;
import java.sql.Blob;
import java.util.Date;
import java.util.List;
@Getter
@Setter
public class Node {

    private int id;

    private String parties;

    private String content;

    private Date nodetime;

    private String ordernum;

    /** 上传图片 **/
    private List<String> imgurl;

    private Detection child;

    private  int partiesid;

    private  int e_id;


    private String imgurls;


}
