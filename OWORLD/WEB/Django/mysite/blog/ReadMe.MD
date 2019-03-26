# explain
    admin.py：用于将模型注册到管理后台，以便在Django的管理后台（Django administration site）查看。管理后台也是一个可选的应用。
    apps.py：当前应用的主要配置文件
    migrations这个目录包含应用的数据迁移记录，用来追踪数据模型的变化然后和数据库同步。
    models.py：当前应用的数据模型，所有的应用必须包含一个models.py文件，但其中内容可以是空白。
    test.py：为应用增加测试代码的文件
    views.py：应用的业务逻辑部分，每一个视图接受一个HTTP请求，处理这个请求然后返回一个HTTP响应。
