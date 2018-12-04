# 实时黑烟检测系统

## [使用说明](USAGE.md)


## 目录结构

```
/
├─doc           # 说明文档
├─demo          # demo目录
│  └─ui             # GUI模版目录
├─server        # 所有主运行程序极其附属模块都在该目录中
│  ├─common         # 公共类目录
│  ├─config         # 默认站点配置目录
│  ├─DBModel        # 数据库模型
│  ├─ProcessManager # 黑烟检测进程管理服务
│  ├─upload_func    # 存放各个上传模块
│  └─web_static     # web服务的静态文件目录
├─SFE           # 核心模块
│  ├─DL             # 深度学习模块
│  ├─resource       # 模块使用的资源文件目录
│  └─thirdparty     # 第三方模块存放目录
└─tools         # 工具程序所在目录
```