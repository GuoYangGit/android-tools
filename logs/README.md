# Xlog日志解析脚本

> 用于解析Xlog日志

## 使用方式

- 将需要解析的`xlog`日志放入`logs`目录下，替换`decode_log.py`中的`PRIV_KEY、PUB_KEY`
- 然后在`shell`中执行`py`命令行
```bash
python3 decode_log xxx.xlog
```