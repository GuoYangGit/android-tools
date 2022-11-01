#!/bin/bash
#--------------------------------------------
# sh-tools 点9转png命令
# author：yang.guo
#--------------------------------------------

#---------------通用配置信息----------------
# 项目路径
# projectPath='/Users/yz/DHNProjects/LamourApp/fancyme_live/live'
projectPath='/Users/948589294qq.com/Desktop/Demo/app'
# 图片输出路径
srcPath='/src/main/res/mipmap-xxhdpi'
# 图片后缀
pngSuffix='.png'
# 点9图后缀
png9Suffix='.9.png'
#-----------------------------------------

# 打开对应.9图片的文件夹
cd $projectPath$srcPath
# 输出当前目录下的文件名
ls
# 用户输入图片名称
echo "请输入需要转换的图片名称："
read pngName

# 进行.9转.png
aapt s -i $pngName$png9Suffix -o $pngName$pngSuffix
