package com.sfe.ssm.model;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class Item {

    private int id;

    private String name;

    private int sort;

    private int pid;

    private List<Item> child;

}
