package com.sfe.ssm.model.view;

import lombok.Data;

import java.util.Date;

/**
 * @author 廖志群
 * @version 1.00
 * @date 九月  20 2017,14:41
 */
@Data
public class VUserList {

    private String id;
    private String userName;
    private String userPhone;
    private String userEmail;
    private String userPwd;
    private String remarks;
    private int status;
    private int authorId;
    private Date creationTime;
    private int modifierId;
    private Date modificationTime;
    private boolean isAdministrator;
    private int depId;
    private String depName;
    private int postId;
    private String postName;



}
