# 生产环境启动
```bash
docker compose up -d
```

# 开发
```bash
cd backend
```
## 更新数据库迁移文件
```bash
python3 manager.py makemigrations
```
## 更新数据库表结构
```bash
python3 manager.py migrate
```
## 启动单测
```bash
python3 manager.py test
```
## 开发环境启动
```bash
python3 manager.py runserver
```