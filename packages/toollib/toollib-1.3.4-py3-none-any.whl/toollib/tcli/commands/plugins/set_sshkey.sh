#!/bin/bash
:<<EOF
@author axiner
@version v1.0.0
@created 2023/4/19 11:52
@abstract 设置免密
@description
@history
EOF

function install_sshpass() {
  release_info=$(cat /etc/*-release)
  if [[ "$release_info" =~ "Ubuntu" ]]; then
    apt-get update && apt-get install -y sshpass
  elif [[ "$release_info" =~ (CentOS|Red Hat|Rocky) ]]; then
    yum install -y sshpass
  else
    echo "System only supported: Ubuntu|CentOS|RedHat|Rocky"
    exit 1
  fi
}

function gen_key() {
  if ! [ -f "$HOME/.ssh/id_rsa.pub" ]; then
    ssh-keygen -t rsa -P '' -f $HOME/.ssh/id_rsa <<< y
  fi
}

function distribute_key {
  IFS=',' read -ra INFO <<< "$1"
  if [ "${#INFO[@]}" -ne 4 ]; then
    echo -e "\033[31m"$1"：Set failed（请检查配置是否正确）\033[0m"
  else
    IP=${INFO[0]}
    USER=${INFO[1]}
    PASS=${INFO[2]}
    PORT=${INFO[3]}
    # set key
    ping -c 1 -w 1 $IP &>/dev/null
    if [ $? -eq 0 ]; then
      sshpass -p $PASS ssh-copy-id -o StrictHostKeyChecking=no -p $PORT $USER@$IP &>/dev/null
      if [ $? -eq 0 ]; then
        echo -e "\033[32m$IP@$USER：Set succeeded\033[0m"
      else
        echo -e "\033[31m$IP@$USER：Set failed（请检查配置是否正确）\033[0m"
      fi
    else
      echo -e "\033[31m$IP@$USER：Set failed（请检查是否能ping通）\033[0m"
    fi
  fi
}


if ! command -v sshpass &> /dev/null; then
  install_sshpass
fi
gen_key
# Check is a file or a string
if [[ -f $1 ]]; then
  # file
  while read line; do
    distribute_key "$line"
  done < "$1"
else
  # string
  for line in $1; do
    distribute_key "$line"
  done
fi
