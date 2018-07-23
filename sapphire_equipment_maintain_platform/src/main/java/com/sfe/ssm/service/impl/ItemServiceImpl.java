package com.sfe.ssm.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;

import com.sfe.ssm.dao.ItemDao;
import com.sfe.ssm.model.Item;
import com.sfe.ssm.service.ItemService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class ItemServiceImpl implements ItemService {

    @Resource
    ItemDao itemDao;


    @Override
    public int createItem(Item item) {
        return itemDao.createItem(item);
    }

    @Override
    public int updateItem(Item item) {
        return itemDao.updateItem(item);
    }

    @Override
    public int deleteItem(int id) {
        return itemDao.deleteItem(id);
    }

    @Override
    public PageInfo selectByPageList(Integer pageNum, Integer pageSize) {

        PageHelper.startPage(pageNum,pageSize);
        List<Item> listData = itemDao.selectByPageList();
        PageInfo page = new PageInfo(listData);
        return page;
    }

    @Override
    public List<Item> getAllItem() {
        return itemDao.getAllItem();
    }

    @Override
    public List<String> getExceptionItem(String exceptions) {
        return itemDao.getExceptionItem(exceptions);
    }
}
