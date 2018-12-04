# 使用说明

默认Python版本为`3.6`

**程序运行需要管理员权限**

**所有执行程序都依赖于核心模块, 请确保运行之前核心模块已安装**

源代码无法直接运行 请运行`compile.py`生成`release`目录 然后目录中选择相同的运行环境运行

参数说明格式为 `参数名称 参数类型[默认值]: 参数说明`

## 核心模块安装
- 安装
    1. 进入`SFE`模块所在目录
    2. 执行`python SFE install` 核心模块将自动安装到运行版本的目录中
- 卸载
    - 执行`python -m SFE uninstall` 核心模块将自动删除

## 服务程序
服务程序在`server`目录中

- ### run_process
    黑烟检测主运行程序

    配置文件编写格式[点击查看](config_help.md)

    
    - 使用
        ```
        run_process.pyc --config-path CONFIG_PATH --auth-code AUTH_CODE [--rtmp-host RTMP_HOST] - start [--rtmp RTMP] [--thread THREAD]
        
        run_process.pyc --config-path CONFIG_PATH --auth-code AUTH_CODE [--rtmp-host RTMP_HOST] - connect --address ADDRESS [--start START] [--rtmp RTMP]
        ```
    - 参数
        - config_path *str*: 配置文件路径
        - auth_code *str*: 授权码
        - rtmp_host *str[None]*: RTMP流推送地址 默认为`127.0.0.1` 流将推送到`rtmp://rtmp_host/live/id`
        - start: 直接启动黑烟检测
            - rtmp *bool[False]*: 是否在开始后启动推流
            - thread *bool[False]*: 是否以线程模式启动
        - connect: 连接到指定socket服务并等待指令
            socket连接成功后支持以下指令(所有指令以"\n"结尾):
            ```
            "shutdown": 停止并关闭程序
            "start": 启动检测
            "stop": 停止检测
            "restart": 重启检测
            "reload": 重新加载配置, 若正在进行检测, 将重启检测
            "status": 获取当前黑烟检测运行状态 返回"0"或"1"
            "rtmp start": 开始推送rtmp流指令
            "rtmp stop": 停止推送rtmp流指令
            "rtmp status": 获取rtmp推送状态 返回"0"或"1"
            ```
            - address *str*: socket服务地址 形式为"ip:port" 如 "127.0.0.1:8888"
            - start *bool[False]*: 是否在连接成功后立即启动检测
            - rtmp *bool[False]*: 是否在启动检测的同时开始推送rtmp

- ### run_server
    黑烟检测管理Web服务

    [WEB服务接口](web_help.MD)

    - 使用
        ```
        run_server.pyc [--port PORT] [--host HOST] [--daemon DAEMON]
        ```

    - 参数
        - port *int[80]*: 端口号
        - host *str["0.0.0.0"]*: 绑定地址
        - daemon *bool[True]*: 在非Windows系统下是否已守护进程模式启动



## demo
黑烟演示程序
    
- 使用 **需要GUI界面支持**
    ```
    smoke.pyc
    ```


## 辅助工具程序
所有辅助工具程序都在`tools`目录中

- ### auth
    获取设备机器码和计算授权码
    - 使用
        ```
        auth.pyc getAuthID

        auth.pyc getAuthCode [--auth-id AUTH_ID]
        ```

    - 参数
        - getAuthID: 获取机器码
        - getAuthCode: 获取授权码
            - auth_id *str[None]*: 授权ID, 为`None`时会获取当前机器的ID

- ### convert
    遍历指定目录, 将其中的所有图片转化为指定大小和格式并按原目录结构保存到指定目录

    - 使用
        ```
        convert.pyc
        ```


- ### grab_vehicle
    自动检测和保存视频中的车辆

    - 使用
    ```
    grab_vehicle.pyc grab --video-path VIDEO_PATH

    grab_vehicle.pyc grabAll --video-path VIDEO_PATH
    ```

    - 参数
        - grab: 检测指定视频
            - video_path *str*: 视频路径
        - grabAll: 检测目录中的所有视频
            - video_path *str*: 视频目录路径

- ### toolbox
    测试黑烟模型、采集黑烟数据

    - 使用
    ```
    toolbox.pyc [--model-path MODEL_PATH] - grabImages --dir-path DIR_PATH --save-dir SAVE_DIR --name NAME --msg MSG --category CATEGORY [--scale SCALE] [--start-idx START_IDX]

    toolbox.pyc [--model-path MODEL_PATH] - grabVideo --video-path VIDEO_PATH --save-dir SAVE_DIR --name NAME --msg MSG --category CATEGORY [--scale SCALE] [--start-idx START_IDX] [--cycle CYCLE]

    toolbox.pyc [--model-path MODEL_PATH] - predictHKImage --img-path IMG_PATH [--scale SCALE]

    toolbox.pyc [--model-path MODEL_PATH] - predictHKImages --img-dir IMG_DIR [--scale SCALE]

    toolbox.pyc [--model-path MODEL_PATH] - predictImage --img-path IMG_PATH [--box BOX] [--roi ROI] [--scale SCALE] [--show SHOW]
    
    toolbox.pyc [--model-path MODEL_PATH] - predictImages --dir-path DIR_PATH [--box BOX] [--roi ROI] [--scale SCALE] [--show SHOW]

    toolbox.pyc [--model-path MODEL_PATH] - predictVideo  --video-path VIDEO_PATH [--scale SCALE]
    ```

    - 参数
        - model_path *str["./smoke.h5"]*: 模型路径
        - grabImages: 采集指定目录中图片素材, 最终文件保存结构为:
            ```
            save_dir/src/name/category/name_msg_idx.jpg
            save_dir/dst/name/category/name_msg_idx.jpg
            ```
            - dir_path *str*: 图片目录路径
            - save_dir *str*: 保存目录
            - name *str*: 名称（推荐格式为：日期_地点）
            - msg *str*: 文件名附加信息
            - category *str*: 保存图片的类别
            - scale *float[None]*: 图片缩放比例
            - start_idx *int[0]*: 起始编号
        - grabVideo: 采集视频画面中黑烟素材, 最终文件保存结构为:
            ```
            save_dir/src/name/category/name_msg_idx.jpg
            save_dir/dst/name/category/name_msg_idx.jpg
            ```
            - video_path *str*: 视频路径
            - save_dir *tr*: 保存目录
            - name *str*: 名称（推荐格式为：日期_地点）
            - msg *str*: 文件名附加信息
            - category *str*: 保存图片的类别
            - scale *float[None]*: 图片缩放比例
            - start_idx *int[0]*: 起始编号
            - cycle *int[5]*: 周期, 如：`5`表示每5帧显示1次图片
        - predictHKImage: 识别海康图片, 图片命名格式为`x-y-w-h.jpg`
            - img_path *str*: 图片路径
            - scale *float[None]*: 显示图片的缩放比例
        - predictHKImages: 批量识别海康图片, 图片命名格式为`x-y-w-h.jpg`
            - img_dir *str*: 图片目录路径
            - scale *float[None]*: 显示图片的缩放比例
        - predictImage: 识别指定图片
            - img_path *str*: 图片路径
            - box *tuple[None]*: 车辆位置, 如果为None则原图识别
            - roi *bool[False]*: 是否手动选择车辆位置
            - scale *float[None]*: 图片缩放比例
            - show *bool[False]*: 是否显示用于识别的图像
        - predictImages: 识别指定图片目录中的图片
            - dir_path *str*: 图片目录
            - box *tuple[None]*: 车辆位置, 如果为None则原图识别
            - roi *bool[False]*: 是否手动选择车辆位置
            - scale *float[None]*: 图片缩放比例
            - show *bool[False]*: 是否显示用于识别的图像
        - predictVideo: 识别视频
            - video_path *str*: 视频路径
            - scale *float[None]*: 图片缩放比例

- ### test
    测试测试集的识别率、正检、误检、漏检数量

    - 使用
    ```
    test.pyc --model-name MODEL_NAME --model-path MODEL_PATH --test-dir TEST_DIR
    ```

    - 参数
        - model_name *str*: 要训练的模型名称(SFE.DL中的模块名称)
        - model_path *str*: 模型文件路径
        - test_dir *str*: 测试集路径


- ### train
    训练`SFE.DL`中指定的模型

    - 使用
        ```
        train.pyc --model-name MODEL_NAME --data-dir DATA_DIR --save-path SAVE_PATH --epoch EPOCH [--load-path LOAD_PATH]
        ```

    - 参数
        - model_name *str*: 要训练的模型名称(SFE.DL中的模块名称)
        - data_dir *str*: 训练数据所在路径
        - save_path *str*: 模型保存路径
        - epoch *int*: 训练轮数
        - load_path *str[None]*: 是否从指定模型中加载权重, 当路径有效加载


- ### test_video
    测试指定视频并将测试结果保存到指定目录

    - 参数
        - test_src *str/tuple*: 视频源
        - save_dir *str[./result]*: 检测结果保存目录
        - clean *bool[True]*: 是否先清空保存目录
        - save_car *bool[True]*: 保存车辆图片
        - save_smoke *bool[True]*: 保存黑烟图片
        - pack *bool[False]*: 是否打包检测结果
        - pack_dir *str[/FTP/result]*: 打包文件保存路径

    - 使用
        ```
        test_video.pyc --test-src TEST_SRC [--save-dir SAVE_DIR] [--clean CLEAN] [--save-car SAVE_CAR] [--save-smoke SAVE_SMOKE] [--pack PACK] [--pack-dir PACK_DIR]
        ```
