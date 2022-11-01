#!/bin/bash
#--------------------------------------------
# sh-tools Git获取提交记录
# author：yang.guo
#--------------------------------------------

# 项目路径
projectPath="/Users/yangguo/HuafangProject/slogan"

getGitChange() {
  # 获取上次打印过的commitID
  lastCommitId=$(cat "$projectPath/gitCommitHistory")
  # 获取当前的commitID
  currentCommitId=$(git rev-parse HEAD)
  echo 当前commitId:"$currentCommitId"
  echo 上次记录的commitId:"$lastCommitId"
  # 获取这两次提交之间的变更说明
  gitLog=$(git log "$lastCommitId".."$currentCommitId" --pretty=format:"%s\t%cn#")
  echo 变更说明"$gitLog"
  # 把中文冒号换成英文的
  gitLog=${gitLog//：/:}
  # 按#进行了分割
  array=(${gitLog//#/ })
  changeResult=""
  #开始遍历
  for var in "${array[@]}"; do
    if [[ $var =~ ]: ]]; then
      #按#进行了分割
      tempArray=(${var//"]:"/ })
      if [ ${#tempArray[@]} == 2 ]; then
        nextChange="${tempArray[1]}\n"
        echo "$nextChange"
        changeResult=$changeResult$nextChange
      fi
    fi
  done
  echo "$changeResult"
}

# ---------------- 准备gitLog变更日志----------------
# 先调到项目目录下
cd $projectPath || exit
# 获取当前git提交记录
changeResult=$(getGitChange)
echo "$changeResult"
