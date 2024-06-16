# flask-MxGPT

**注意，最外面的那个index.html是为了方便调试启动的，并不是真正会调用的html
真实的项目html在templates文件夹下**

### v1.1.0:
* 将URL封装到一个文件中进行统一的路由管理

* ***如果要启动项目，请在控制台输入***
```angular2html
flask --app loadURL.py --debug run
```

### v1.2.0:
* 发布数据库系统，重新优化产品结构。

* ***如果要启动项目，请在控制台输入***
```angular2html
flask --app app.py --debug run
```

### v1.3.0:
* 增加了主页导航分页的功能，实现跳转。
* 实现了服务器部署的部分
* 实现服务器部署和本地调试的参数化切换, **默认为local**

* ***如果要指定项目模式，请在控制台输入***
```angular2html
python3 app.py --mode=[local|server]
```

### v1.4.0:
* 成功在本地连接到服务器的MySQL数据库，实现本地和服务器的数据库的同步和远程管理。
* 修改了注册的逻辑，将**uuid**和**username**作为主键，实现用户唯一性。并且注册失败会显示信息。
* 修改了登录的逻辑，当登录失败的时候会显示信息。

* ***如果要在服务器持续运行，请在控制台输入***
```angular2html
nohup python3 app.py --mode=[local|server] &
```