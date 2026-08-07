---
title: Git 使用指南
date: 2026-08-07
tags: Git, 工具, 教程

---

Git 是目前最流行的分布式版本控制系统，广泛用于软件开发和项目管理。本文将介绍 Git 的基本使用方法。

## 安装 Git

**Windows**: 下载 [Git for Windows](https://git-scm.com/download/win) 并安装，如果下载太慢可以使用[镜像](https://registry.npmmirror.com/binary.html?path=git-for-windows/)下载

**Mac**: `brew install git`

**Linux**: `sudo apt install git` (Ubuntu/Debian)

## 基本配置

安装后先配置用户信息：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

名字可以随便填，但如果你要推到`github`上需要写GitHub 绑定的邮箱。

#### 如何查看`github`上的邮箱？

- 登录 GitHub，点右上角头像 → **Settings**（设置）
- 左侧找到 **Emails**，就能看到绑定的邮箱和隐私邮箱
- 打勾勾选 "Keep my email address private" 后，页面会显示你的隐私邮箱 `用户名@users.noreply.github.com`

## 常用命令

### 初始化与克隆

```bash
git init              # 初始化新仓库
git clone <url>       # 克隆远程仓库
```

### 日常工作流

```bash
git add .             # 添加所有修改到暂存区
git commit -m "说明"  # 提交更改
git push              # 推送到远程
git pull              # 拉取远程更新
```

### 查看状态

```bash
git status            # 查看当前状态
git log --oneline     # 查看提交历史
git diff              # 查看未暂存的修改
```

## 分支管理

```bash
git branch feature    # 创建分支
git checkout feature  # 切换分支
git checkout -b dev   # 创建并切换分支
git merge feature     # 合并分支
git branch -d feature # 删除分支
```

## 撤销操作

```bash
git checkout -- file  # 撤销工作区修改
git reset HEAD file   # 取消暂存
git reset --soft HEAD~1  # 撤销上次提交，保留修改
```

## 实用技巧

| 命令              | 作用           |
| ----------------- | -------------- |
| `git stash`       | 临时保存修改   |
| `git stash pop`   | 恢复保存的修改 |
| `git log --graph` | 图形化显示分支 |
| `git remote -v`   | 查看远程仓库   |

## 总结

掌握这些基础命令后，你就可以开始使用 Git 管理代码了。建议多实践，熟练后可以学习更高级的用法如 rebase、cherry-pick 等。