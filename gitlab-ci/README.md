# GitLab自动构建框架

## yaml目录

- 合并分支触发自动构建[merge_request_pipelines](./yml/merge_request_pipelines.yml)
- push分支触发自动构建[push_pipelines](./yml/push_pipelines.yml)

## py目录

- 一键打包流程类[build_notify_apk](./py/build_notify_apk.py)
- apk构建工具类[apk_utils](./py/apk_utils.py)
- 飞书通知类[feishu](./py/feishu.py)
- fir上传Apk工具类[fir](./py/fir.py)

## sh目录

- 打包Apk脚本[build_apk](./sh/build_apk.sh)
- 查看git提交记录[git_change](./sh/git_change.sh)