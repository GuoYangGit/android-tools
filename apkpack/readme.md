## Android自动化打包并且上传fir

---
### 使用说明

> 主要用于android项目的自动化打包,并且打包完成自动化上传fir的功能(就一句命令python fir.py),简化我们去手动打包apk,然后手动去fir上传应用的过程.

1. **config.py(配置文件)**进行项目配置

```python
# 这里输入你的项目名称
apkName = "富勤金融"
# android的项目地址
projectPath = "/Users/guoyang/FuQinHengYe/FortunesFinance"
# 构建命令(比如我们项目进行了productFlavors配置,这里就输入我们productFlavors配置的tag,如果项目没有进行productFlavors配置,那这里可以什么都不填写)
buildTool = "releseApi"
# Android SDK buidtools路径
sdkBuildToolPath = "/Users/guoyang/Library/Android/sdk/build-tools/26.0.2"

# fir的配置
# fir的BundleId
firBundleId = '******'
# fir的apiToken
firApiToken = '************'
```

2. 然后我们就可以运行命令了,``python fir.py``,接下来我们就可以一边休息一边看着``cmd``的输出命令,等着自动化打包的结束了.
 
