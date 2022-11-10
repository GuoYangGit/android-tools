# UI自动化测试框架UIAutomator

> Readme文档 https://github.com/openatx/uiautomator2/blob/master/README.md

## 安装
- 安装`uiautomator2`
```bash
pip install --upgrade --pre uiautomator2
```
测试是否安装成功 `uiautomator2 --help`
- 安装UI查看器`weditor`
```bash
pip install -U weditor
```
安装好之后，就可以在命令行运行 `weditor --help` 确认是否安装成功了。
命令行直接输入 `weditor` 会自动打开浏览器，输入设备的`ip`或者序列号，点击`Connect`即可。
- 安装`uiautomator2`到手机
```bash
# init 所有的已经连接到电脑的设备
python -m uiautomator2 init
# 高阶用法
# init and set atx-agent listen in all address
python -m uiautomator2 init --addr :7912
```
安装提示`success`即可

## 操作指南
### 连接设备
```python
device = u2.connect()
```
### 启动/关闭App
```python
# 默认的这种方法是先通过atx-agent解析apk包的mainActivity，然后调用am start -n $package/$activity启动
d.app_start("com.example.hello_world")

# equivalent to `am force-stop`, thus you could lose data
d.app_stop("com.example.hello_world")
```
### 获取设备信息
```python
d.info
```
