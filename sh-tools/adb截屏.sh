#!/bin/bash
#--------------------------------------------
# sh-tools adb截屏保存电脑命令
# author：yang.guo
#--------------------------------------------
echo "开始截图"
DATE=$(date "+%Y%m%d-%H-%M-%S") 
echo $DATE
adb shell screencap /sdcard/screen_${DATE}.png
adb pull /sdcard/screen_${DATE}.png /Users/guoyang/Desktop/截屏.png
osascript -e 'tell application "Terminal" to quit' & exit