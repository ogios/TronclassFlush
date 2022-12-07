# TronclassFlush
刷欧亚畅课课程访问量的小程序

## 食用指北

> conf.ini自行创建

使用flush.py文件：
```shell
python .\flush.py -session "<session>" -url "<course_url>" -count <count>
```
使用flush.exe文件:
```shell
flush.exe -session "<session>" -url "<course_url>" -count <count>
```

### session与课程获取

> 暂时还没有方法通过账号密码获取session，学的还差很多😭只能手动登录之后在开发者工具中获取  

登入后在页面里打开开发者工具，在控制台中输入:
```javascript
$.cookie("session")
```

手动复制，在命令行中加入 `-session ` 并粘贴在它后面，记得用双引号括起来，运行后session会被保存，下次再刷可以不输入session，除非session更新或失效

![Snipaste_2022-12-03_21-12-44](https://user-images.githubusercontent.com/96933655/206089872-be2446d1-f1c5-419b-9491-1afca5f626de.png)


课程就是直接进入需要刷的课程的页面，复制网页链接传入 `-url ` 后面即可

## 测试页面
本人用flask暂时做了一个测试交互页面，并非永久开启，随时可能关闭：
[test](http://47.94.146.109:5570/)  
可能存在无效的刷新，不稳定  

![htmlexample](https://user-images.githubusercontent.com/96933655/206091858-b966993d-e24a-4279-9d7b-1d76b894f000.png)

