**字符编码: UTF-8**

**内容格式: json**

**文件命名: 站点编号.json**

例子

    {
        "id": "0",
        "name": "测试点",
        "upload_func": "test",
        "video_source": "test_video/0.mp4",
        "Ringelmann": 1,
        "save_path": "t/0",
        "border": [
            [[0, 0], [100, 0]],     // 上边界
            [[0, 100], [100, 100]]  // 下边界
        ],
        "start_time": null,
        "stop_time": null,
        "statistics": null,
        "statis_interval": null
    }

**参数说明**

参数            |参数类型|允许null|说明
:--------------:|:-----:|:-----:|:-----------------------------
name            |str    |True   |站点名称
id              |int/str|False  |站点编号
video_source    |str    |False  |视频源 可以为视频文件路径 也可以为海康视频流 为视频流时格式为 `IP地址||端口号||用户名||密码||视频通道号`
save_path       |str    |False  |本地文件保存目录
border          |array  |True   |车道边界 包含为上、下边界两个数组, 每个数组成员数**必须相同** 成员也为数组 数据为 `[x, y] x, y ∈ [0, 100]`, 为`null`时为全屏 
Ringelmann      |int    |True   |林格曼黑度阈值 *取值区间为 [0, 5]*
upload_func     |str    |True   |使用的黑烟记录上传模块, 多个上模块之间用`|`分割, 在模块名称之后添加`[属性名=属性值][属性名2=属性值2]`可以设置指定的模块属性
statistics      |str    |True   |使用的车流量统计上传模块, 使用方法同`upload_func`
statis_interval |int/str|True   |车辆统计间隔 单位为*分钟* `statistical`为`null`时该选项无效, **每个车流量上传模块对应一个间隔, 一一对应, 多个间隔之间用`|`分割**
start_time      |str    |True   |自动开始时间 为`null`时不自动开始 时间格式为`小时:分钟` 如`0:0` 表示零点零分自动开始
stop_time       |str    |True   |自动停止时间 其他同`start_time`
