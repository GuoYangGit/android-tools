# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/11/1-10:50
@Desc: 构建Apk相关工具类
"""
import json
import os
import re
import subprocess
import fir

# TODO 这里需要根据自己项目进行改写
# 项目路径
project_path = "/Users/yangguo/HuafangProject/slogan"
# apk路径
apk_path = "/app/build/outputs/apk/release"
# buildTool路径
build_tool_path = "/Users/yangguo/Library/Android/sdk/build-tools/30.0.3"
# AppName
apk_name = 'slogan'


# 获取Apk路径
def get_apk_file(path=project_path):
    path = f'{path}{apk_path}'
    for file in os.listdir(path):
        if '.apk' in file:
            return f'{path}/{file}'
    return ''


# 获取apk信息
def get_apk_info(build_apk_path):
    apk_info = run_cmd(f'{build_tool_path}/aapt d badging {build_apk_path}')
    print(f'获取apk信息为:{apk_info}')
    data = {}
    match = re.compile(r"package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(apk_info)
    data['version_code'] = match.group(2)
    data['version_name'] = match.group(3)
    data['apk_name'] = apk_name
    return data


# 运行CMD命令并返回运行结果
def run_cmd(command):
    print(f'当前执行的cmd:{command}')
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
    return str(ret.stdout, "utf-8")


# 构建APK
def build_apk(build_apk_path=project_path):
    os.chdir(build_apk_path)
    os.system("ls")
    os.system('git fetch')
    os.system('git checkout dev')
    os.system('git pull')
    build_apk_shell = './gradlew clean assembleRelease'
    os.system(build_apk_shell)


# 获取git提交变更记录
def git_change(git_apk_path=project_path):
    os.chdir(git_apk_path)
    # 获取上次打印过的commitID
    last_commit_id = open('gitCommitHistory', 'r').read()
    print(f'上次提交:{last_commit_id}')
    # 获取当前的commitID
    current_commit_id = run_cmd('git rev-parse HEAD').strip()
    print(f'本次提交:{current_commit_id}')
    # git获取提交记录,以json形式进行返回
    log_shell = f'git log {last_commit_id}..{current_commit_id} --date=iso ' \
                r'--pretty=format:"{\"author\": \"%cn\",\"message\": \"%s\"}," ' \
                r'$@ | perl -pe "BEGIN{print \"[\"}; END{print \"]\n\"}" | perl -pe "s/},]/}]/"'
    git_log = run_cmd(log_shell).replace('：', ':')
    json_log = json.loads(git_log)
    change_result = ''
    for log in json_log:
        log_arr = re.split(r'\[\w+?\]:', log['message'])
        author = log['author']
        if len(log_arr) >= 2:
            for content in log_arr:
                if content == '':
                    continue
                change_result = f'{change_result}{content} {author}\n'
    return change_result


if __name__ == '__main__':
    res = fir.fir_apk_url()
    print(res)
# build_apk(projectPath)
