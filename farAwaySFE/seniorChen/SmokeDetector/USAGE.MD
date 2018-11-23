# 使用说明

默认Python版本为`3.6` 

程序需要管理员权限

参数说明格式为 `参数名称 参数类型[默认值]: 参数说明`

## 主运行程序

- ### run_main
    黑烟检测主控制程序

    - 使用
        
        `run_main.pyc` **需要GUI界面支持**

- ### run_process
    黑烟检测主运行程序

    - 参数
    
        *config_path* **str**: [配置文件](config_help.MD)路径 
    
        *is_subprocess* **bool[False]**: 是否为子进程
    
    - 使用
    
        ```
        run_process.pyc CONFIG_PATH [IS_SUBPROCESS]

        run_process.pyc --config-path CONFIG_PATH [--is-subprocess IS_SUBPROCESS]
        ```

- ### smoke
    黑烟演示程序

    - 使用

        `smoke.pyc` **需要GUI界面支持**


## 辅助程序

- ### DL
    训练、测试 `SFE.DL.Net` 模型

    #### 子命令

    1. train

        训练模型

        - 参数

            *model_path* **str**: 模型保存路径

            *image_path* **str**: 数据集路径

            *time* **int**: 训练轮数

            *load_model* **bool[False]**: 是否加载模型权重

        - 使用

            ```
            DL.pyc train MODEL_PATH IMAGE_PATH TIME [LOAD_MODEL]

            DL.pyc train --model-path MODEL_PATH --image-path IMAGE_PATH --time TIME [--load-model LOAD_MODEL]
            ```

    2. test

        测试模型

        - 参数

            *model_path* **str**: 模型所在路径
    
            *image_path* **str**: 测试图片所在路径

        - 使用

            ```
            DL.pyc test MODEL_PATH IMAGE_PATH
            
            DL.pyc test --model-path MODEL_PATH --image-path IMAGE_PATH
            ```

- ### train
    训练`SFE.DL`中指定的模型

    - 参数

        *model_name* **str**: 要训练的模型名称(SFE.DL中的模块名称)

        *data_dir* **str**: 训练数据所在路径

        *save_path* **str**: 模型保存路径

        *epoch* **int**: 训练轮数

    - 使用

        ```
        train.pyc MODEL_NAME DATA_DIR SAVE_PATH EPOCH
        
        train.pyc --model-name MODEL_NAME --data-dir DATA_DIR --save-path SAVE_PATH --epoch EPOCH
        ```

## 测试程序

- ### test_video
    测试指定视频并将测试结果保存到指定目录

    - 参数

        *test_src* **str/tuple**: 视频源

        *save_dir* **str[./result]**: 检测结果保存目录

        *clean* **bool[True]**: 是否先清空保存目录

        *save_car* **bool[True]**: 保存车辆图片

        *save_smoke* **bool[True]**: 保存黑烟图片

        *pack* **bool[False]**: 是否打包检测结果

        *pack_dir* **str[/FTP/result]**: 打包文件保存路径

    - 使用

        ```
        test_video.pyc TEST_SRC [SAVE_DIR] [CLEAN] [SAVE_CAR] [SAVE_SMOKE] [PACK] [PACK_DIR]
        
        test_video.pyc --test-src TEST_SRC [--save-dir SAVE_DIR] [--clean CLEAN] [--save-car SAVE_CAR] [--save-smoke SAVE_SMOKE] [--pack PACK] [--pack-dir PACK_DIR]
        ```
