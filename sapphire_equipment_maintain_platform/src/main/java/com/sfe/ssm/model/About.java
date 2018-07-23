package com.sfe.ssm.model;

import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * @author 廖志群
 * @version 1.00
 * @date 五月  15 2017,17:06
 */
@Data
public class About implements Serializable {

    private String id;
    private String projectName;
    private String versions;
    private String remark;
    private String technicalSupport;
    private String link;
    private String email;
    private Date creationTime;

}

