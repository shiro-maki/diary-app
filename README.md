# 日记打卡

本地单人的日记打卡小工具。每天写一篇日记即自动打卡，记录连续天数。

## 功能

- 写日记：每天一篇，自动打卡，统计当前连续 / 历史最长连续天数
- 补卡：可以补写昨天，衔接连续天数
- 历史回看：左侧日期列表随时翻阅、修改旧日记

## 技术

- Python 3.13 + customtkinter（现代桌面 GUI）
- 数据本地存储：`data/YYYY/YYYY-MM-DD.json`，一天一个文件，**不进 Git**

## 安装与运行

1. 安装官方 CPython（需包含 tcl/tk），本项目开发环境为 `D:\Python`
2. 安装依赖：
   ```bash
   D:\Python\python.exe -m pip install -r requirements.txt
   ```
3. 双击 `start.bat` 启动（bat 内硬编码了 `D:\Python\python.exe`，路径不同请自行改）

## 数据说明

- 日记保存在本地 `data/` 目录，已加入 `.gitignore`，不会上传到仓库
- 备份：直接拷贝 `data/` 文件夹即可

## 目录结构

```
main.py          入口
ui.py            界面（customtkinter）
storage.py       存储（一天一个 JSON）
streak.py        连续天数计算
requirements.txt 依赖
start.bat        双击启动
data/            日记数据（本地，不进 Git）
```
