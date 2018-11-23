# coding: utf-8

'''
上传模块编写格式


- 每个上传模块独立文件
- 模块中至少包含两个方法, 名称、参数、返回值如下

```
# 黑烟记录上传函数
def upload(record: RecordData) -> bool
```
- param record: 需要上传的黑烟记录
- return: 返回上传是否成功

```
# 车流量统计上传函数
def statistics(st_id, time: datetime, interval: int) -> bool
```
- param st_id: 站点编号
- param time: 统计时间
- param interval: 统计间隔 单位为分钟
- return: 返回上传是否成功
'''
