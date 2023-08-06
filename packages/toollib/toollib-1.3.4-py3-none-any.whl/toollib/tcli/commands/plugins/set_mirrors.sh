#!/bin/bash
set -e
:<<EOF
@author axiner
@version v1.0.0
@created 2023/4/19 11:52
@abstract 设置镜像源
@description
@history
EOF

# 判断系统是否为Ubuntu
release_info=$(cat /etc/*-release)
if [[ "$release_info" =~ Ubuntu ]]; then
  echo "Current system: Ubuntu"
  #备份原有的镜像源文件
  cp /etc/apt/sources.list /etc/apt/sources.list.bak.$(date +%Y%m%d)
  # 阿里云源
  echo "# 阿里镜像源" > /etc/apt/sources.list
  echo "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse" >> /etc/apt/sources.list
  # 清华源
  echo "" >> /etc/apt/sources.list
  echo "# 清华镜像源" >> /etc/apt/sources.list
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse" >> /etc/apt/sources.list
  echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse" >> /etc/apt/sources.list
  # 更新apt源
  apt-get update
  echo "Apt sources have been configured finished（若更新失败请检查网络是否畅通）"
# 判断系统是否为CentOS或RedHat或Rocky
elif [[ "$release_info" =~ "CentOS" ]]; then
  echo "Current system: CentOS"
  # 备份原有的yum源配置文件
  cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak.$(date +%Y%m%d)
  # 下载CentOS-Base.repo yum源配置文件
  curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
  # 更新yum源
  yum makecache
  echo "Yum sources have been configured finished（若更新失败请检查网络是否畅通）"
elif [[ "$release_info" =~ "Red Hat" ]]; then
  echo "Current system: RedHat"
  # 备份原有的yum源配置文件
  cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak.$(date +%Y%m%d)
  # 下载CentOS-Base.repo yum源配置文件
  curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
  # 更新yum源
  yum makecache
  echo "Yum sources have been configured finished（若更新失败请检查网络是否畅通）"
elif [[ "$release_info" =~ "Rocky" ]]; then
  echo "Current system: Rocky"
  # 备份原有的yum源配置文件
  cp /etc/yum.repos.d/Rocky-Base.repo /etc/yum.repos.d/Rocky-Base.repo.bak.$(date +%Y%m%d)
  # 下载CentOS-Base.repo yum源配置文件
  curl -o /etc/yum.repos.d/Rocky-Base.repo http://mirrors.aliyun.com/repo/rocky-8-x86_64.repo
  # 更新yum源
  yum makecache
  echo "Yum sources have been configured finished（若更新失败请检查网络是否畅通）"
else
  echo "System only supported: Ubuntu|CentOS|RedHat|Rocky"
  exit 1
fi
