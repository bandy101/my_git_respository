# Web服务API说明

字符编码均使用`UTF-8`

- ## /
    静态文件根目录

- ## /api
    数据传输除二进制数据外均使用json格式

    返回数据格式如下
    ```
    {
        "success": true|false,  # 此次操作是否成功
        "content": object       # 返回结果 此次操作返回的数据 当操作失败时为错误原因
    }
    ```

    - 普通用户: user, 密码: sfe-123456
    - 审核用户: auditor, 密码: sfe@123456
    - 管理员: admin, 密码: admin@sfe
    
    URL|请求方法|data|说明|返回结果
    :----:|:---:|:---:|:---:|:---:
    /api/server_name|GET|-|获取该服务站点的名称|站点名称
    -|-|-|-|-
    /api/login|POST|`{"user":"用户名", "password":"密码(需要做一次MD5)"}`|登录|返回用户权限, int
    /api/permission|GET|-|获取当前登录用户的权限|int
    -|-|-|-|-
    /api/config|GET|-|获取当前服务的所有配置|返回一个数组 数组中的每个成员都是一个配置
    /api/config?action=startAll|GET|-|启动所有配置的黑烟检测|无
    /api/config?action=stopAll|GET|-|停止所有配置的黑烟检测|无
    /api/config?action=shutdownAll|GET|-|关闭所有黑烟检测进程|无
    -|-|-|-|-
    /api/config/id|GET|-|获取指定ID的配置|返回一个对象 该对象为指定ID的配置
    /api/config/id?action=start|GET|-|启动指定ID的黑烟检测|无
    /api/config/id?action=stop|GET|-|停止指定ID的黑烟检测|无
    /api/config/id?action=restart|GET|-|重启指定ID的黑烟检测|无
    /api/config/id?action=reload|GET|-|重新加载指定ID的配置文件|无
    /api/config/id?action=shutdown|GET|-|关闭指定ID的黑烟检测进程|无
    /api/config/id|POST|一个配置对象 详见[配置](config_help.md)|添加一个配置, 路径ID与数据ID需要一致|无
    /api/config/id|PUT|同POST|修改指定ID的配置, 路径ID与数据ID需要一致|无
    /api/config/id|DELETE|-|删除一个配置|无
    -|-|-|-|-
    /api/status/id|GET|-|获取指定ID的当前状态|`{"status": 运行状态, "rtmp": RTMP推送状态(bool)}`
    /api/status|GET|-|获取所有配置当前的状态|`{"id": {"status": 运行状态, "rtmp": RTMP推送状态(bool)}`
    -|-|-|-|-
    /api/frame/id|GET|-|生成一张指定ID配置视频源的视频帧, 图片会在生成30秒后自动删除|成功返回图片路径
    -|-|-|-|-
    /api/rtmp_host|GET|-|获取RTMP流的外部访问地址|返回形如`127.0.0.1:1935`的文本
    /api/rtmp|GET|-|获取所有配置的RTMP推送状态(是否在推送)|`{id:true|false, ...}`
    /api/rtmp/id|GET|-|获取指定ID的RTMP推送状态|`true|false`
    /api/rtmp/id?action=start|GET|-|启动指定ID的RTMP推送|无
    /api/rtmp/id?action=stop|GET|-|停止指定ID的RTMP推送|无
    -|-|-|-|-
    /api/autostart|GET|-|获取当前的进程自动启动的值|`true|false`
    /api/autostart?action=start|GET|-|启动进程自动停止|无
    /api/autostart?action=stop|GET|-|启动进程自动停止|无
    -|-|-|-|-
    /api/log|GET|-|获得主程序日志|返回一个数组, 每个成员是一行日志
    /api/log/id|GET|-|获取指定站点日志|同`/api/log`
    -|-|-|-|-
    /api/list/plate_color|GET|-|获取车牌颜色列表| 文本数组
    /api/list/plate_type|GET|-|获取车牌类型列表| 文本数组
    /api/list/vehicle_color|GET|-|获取车辆颜色列表| 文本数组
    /api/list/vehicle_type|GET|-|获取车辆类型列表| 文本数组
    -|-|-|-|-
    /api/record|GET|-|获取站点列表|返回站点列表
    /api/record/id|GET|-|获取记录列表|返回记录状态列表, 列表信息为`{"id": 记录id, "name": 显示名称, "status": 确认状态(bool), "upload": 上传状态(string)}`
    /api/record/id/record_id|GET|-|获取记录文本信息|` {"st_id": 站点ID, "st_name": 站点名称, "Ringelmann": 林格曼黑度, "plate": 车牌, "plate_color": 车牌颜色, "plate_type": 车牌类型, "vehicle_type": 车辆类型, "vehicle_color": 车辆颜色, "lane": 车道号, "timestamp": 记录抓取时间(13位时间戳)}`
    /api/record/id/record_id/image1|GET|-|获取记录图片1|jpeg格式图片
    /api/record/id/record_id/image2|GET|-|获取记录图片2|jpeg格式图片
    /api/record/id/record_id/video|GET|-|获取记录视频|mp4格式视频
    /api/record/id/record_id/status|GET|-|修改记录状态为`true`|无
    /api/record/id/record_id/upload|POST|`{"Ringelmann": 林格曼黑度, "plate": 车牌号码, "plate_color": 车牌颜色, "plate_type": 车牌类型, "vehicle_color": 车辆颜色, "vehicle_type": 车辆类型, "lane": 车道号}`|修改记录上传状态为`等待上传`|无

    ### 记录上传时, 各字段的有效取值如下
    | 字段名称 | 说明 | 类型 | 有效取值 |
    | ------- | ---- | ---- | ------- |
    | Ringelmann | 林格曼黑度 | int | 0 <= Ringelmann <= 5 |
    | plate | 车牌号 | str | 任意文本值
    | plate_color | 车牌颜色 | str | ["蓝", "黄", "白", "黑", "绿", "黄绿", "其他"] |
    | Plate_type | 车牌类型 | str | ["大型汽车", "小型汽车", "使馆汽车", "领馆汽车", "境外汽车", "外籍汽车", "农用运输车", "拖拉机", "挂车", "教练汽车", "警用汽车", "大型新能源汽车", "小型新能源汽车", "其他] |
    | vheicle_color | 车辆颜色 | str | ["白", "银", "灰", "黑", "红", "深蓝", "蓝", "黄", "绿", "棕", "粉", "紫", "深灰", "青", "其他"] |
    | vehicle_type | 车辆类型 | str | ["客车", "货车", "轿车", "面包车", "小货车", "行人", "二轮车", "三轮车", "SUV/MPV", "中型客车", "机动车", "非机动车", "小型轿车", "微型轿车", "皮卡车", "其他"] |
    | lane | 车道号 | int | 大于0的整数
