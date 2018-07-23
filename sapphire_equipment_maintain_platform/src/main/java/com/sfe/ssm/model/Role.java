package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Role {
    private int id;
    private String roleName;
    private String roleSign;
    private String permissions;
}
