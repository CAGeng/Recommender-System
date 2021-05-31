# 代码说明

* 根目录 : movie_rec_sys

  * appfront:前端文件夹
    * <目前仅供测试，之后将真正的前端文件夹接入>
  
* movie_rec_sys:后端文件夹
    * settings.py:全局参数
    * urls.py:通过路径'/api'将后端接口转移到app目录——recommend
  * recommend:app文件夹
    * <该目录处理并响应前端请求>
    * recommend.py和database.py是之前的算法模块和数据模块
    * urls.py定义api的网络接口，将其连接到views.py中的函数接口
    * views.py实现了接收请求，发送响应的函数接口
  * movies:电影图片文件夹，是图片url的基地址



## 使用方法

## 准备

和之前一样，如果没有构建数据库，还是要先运行**根目录/recommend/database.py**构建数据库，他需要在同级目录中添加input文件夹并将原始数据放进去。

### 后端测试

进入根目录，运行

```
python .\manage.py runserver
```

在   **http://127.0.0.1:8000/+$api名称**    的地址可以访问到后端返回的数据。

![image-20210324232946340](C:\Users\sft\Desktop\se\django\movie_rec_sys\readme.assets\image-20210324232946340.png)

![image-20210324233210034](C:\Users\sft\Desktop\se\django\movie_rec_sys\readme.assets\image-20210324233210034.png)

![image-20210324233236466](C:\Users\sft\Desktop\se\django\movie_rec_sys\readme.assets\image-20210324233236466.png)



### 前端测试

进入/appfront 文件夹，运行

```
npm run dev
```

（可能需要npm install一些东西）



在http://localhost:8080可以访问到测试页面

![image-20210324233551107](C:\Users\sft\Desktop\se\django\movie_rec_sys\readme.assets\image-20210324233551107.png)