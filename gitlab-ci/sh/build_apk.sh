#!/bin/bash
#--------------------------------------------
# sh-tools Android打包脚本
# author：yang.guo
#--------------------------------------------

# 项目路径
projectPath="/Users/yangguo/HuafangProject/slogan"

# 构建Apk
echo $projectPath
cd $projectPath || exit
ls
git fetch
git checkout dev
git pull
chmod +x ./gradlew
./gradlew clean assembleRelease
