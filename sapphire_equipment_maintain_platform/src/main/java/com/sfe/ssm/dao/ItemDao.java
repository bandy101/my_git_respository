package com.sfe.ssm.dao;


import com.sfe.ssm.model.Item;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ItemDao {

    List<Item> getAllItem();

    int createItem(Item item);

    int updateItem(Item item);

    int deleteItem(@Param("id") int id);

    List<Item> selectByPageList();

    List<String> getExceptionItem(@Param("exceptions") String exceptions);
}
