## 黄油绘本论坛 
#### 在线访问地址：www.zhangyongyu.com
![](/static/img/butter.gif)

#### 基本功能
- 注册、登录、权限管理、发帖、评论、私信、修改密码和更换头像等
- 使用 MongoDB 存储数据，并实现相应的 ORM 
- 使用 Redis 存储 token 数据
- 使用 Jinja2 解耦业务逻辑与表现逻辑
- 利用插入随机数防御 CSRF 攻击，利用 Jinja2 转义防御 XSS 攻击
- 使用 Nginx, Gunicorn 和Supervisor 进行部署，实现静态文件缓存、均衡负载、多进程管理等功能，提高访问性能
- 利用 Vagrant 实现开发与部署的一致环境，并使用 Bash 脚本一键部署
