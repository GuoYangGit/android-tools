# Xlog日志解析
## 使用方式
- 将需要解析的`xlog`日志放入`logs`目录下，替换`decode_log.py`中的`PRIV_KEY、PUB_KEY`
- 然后在`shell`中执行`py`命令行
```shell
python3 decode_log xxx.xlog
```

## 生成私钥和公钥
- 生成私钥
```shell
python3 gen_key.py
```