import hashlib
from pathlib import Path
import urllib.request
from urllib.error import HTTPError, URLError
flag = 0

def get_remote_sha1(url):
    try:
        tmp = urllib.request.urlopen(url)
        params = tmp.read().decode()
        return eval(params)['sha']
    except HTTPError or URLError:
        global flag
        if flag == 0:
            print('无法检查模板更新，使用当前保存版本生成触发器')
            print('通常是因为GitHub API访问达上限，删除src文件夹可强制进行更新')
            print('如下载成功可忽略此信息')
            flag = 1
        return None


def get_local_sha1(path):
    with open(path, 'rb') as f:
        content = f.read()
    content = b'blob %d\0' % len(content) + content
    return hashlib.sha1(content).hexdigest()


def check(path, src = Path('src/'),
          api = 'https://api.github.com/repos/Yuee98/FFXIVOneButtonCombo/contents/',
          remote = 'https://raw.githubusercontent.com/Yuee98/FFXIVOneButtonCombo/main/'):
    
    api = api + path
    url = remote + path 
    path = src/path

    if not path.parent.is_dir():
        path.parent.mkdir(parents=True)

    if path.exists():
        remote_sha1 = get_remote_sha1(api)
        if remote_sha1 is None or remote_sha1 == get_local_sha1(path):
            return path
        else:
            path.unlink()

    try:
        urllib.request.urlretrieve(url, str(path))
    except HTTPError:
        print(f'下载 {path} 失败，请检查网络连接或架梯子尝试')
        exit()
    else:
        print(f'下载 {path} 成功')

    return path


def md5(text:str):
    return hashlib.md5(text.encode()).hexdigest()


def job_filter_id(job):
    d = {
        '骑士': 262144,
        '战士': 1048576,
        '暗黑骑士': 2147483648,
        '绝枪战士': 68719476736,

        '白魔法师': 8388608,
        '学者': 134217728,
        '占星师': 4294967296,
        '贤者': 549755813888,

        '忍者': 536870912,
        '武僧': 524288,
        '武士': 8589934592,
        '龙骑士': 2097152,
        '钐镰客': 274877906944,

        '诗人': 4194304,
        '机工士': 1073741824,
        '舞者': 137438953472,

        '黑魔法师': 16777216,
        '召唤师': 67108864,
        '赤魔法师': 17179869184,
    }
    return d[job]