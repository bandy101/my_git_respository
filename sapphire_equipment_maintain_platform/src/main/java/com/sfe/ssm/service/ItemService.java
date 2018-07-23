package com.sfe.ssm.service;

import com.github.pagehelper.PageInfo;
import com.sfe.ssm.model.Item;

import java.util.List;


public interface ItemService {

    int createItem(Item item);

    int updateItem(Item item);

    int deleteItem(int id);

    PageInfo selectByPageList(Integer pageNum, Integer pageSize);

    List<Item> getAllItem();

    List<String> getExceptionItem(String exceptions);
}
