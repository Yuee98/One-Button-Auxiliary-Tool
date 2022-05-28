import js2py
import hashlib
from pathlib import Path
import urllib.request
import time

def get_remote_sha1(content):
    content = b'blob %d\0' % len(content) + content
    return hashlib.sha1(content).hexdigest()


def get_local_sha1(path):
    with open(path, 'rb') as f:
        content = f.read()
    content = b'blob %d\0' % len(content) + content
    return hashlib.sha1(content).hexdigest()


def check(path, src = Path('src/'),
          remote = 'https://ffxiv-one-button-combo.vercel.app/'):
    
    url = remote + path 
    path = src/path
    print(f'检查 {path} 更新'.ljust(50, '.'), end=' ')

    if not path.parent.is_dir():
        path.parent.mkdir(parents=True)

    response = urllib.request.urlopen(url)
    content = response.read()
    if path.exists():
        if response.code == 200:
            if get_remote_sha1(content) == get_local_sha1(path):
                print('当前已是最新版本')
                return path
            else:
                path.unlink()
                print('更新成功')
        else:
            print('无法检查更新，使用当前版本触发器')
            return path

    else:
        if response.code == 200:
            print('下载成功')
        else:
            print('下载失败，请检查网络连接或架梯子尝试')
            exit()

    with open(path, 'wb') as f:
        f.write(content)

    response.close()
    time.sleep(0.5)
    return path


def md5(text:str):
    return hashlib.md5(text.encode()).hexdigest()


action_path = check('js/actions.js')
with open(action_path, encoding='utf-8') as f:
    context = js2py.EvalJs()
    context.execute(f.read())
actions = context.actions.to_dict()
base = context.base.to_dict()
special = context.special.to_dict()
buff = context.changeWithBuff.to_list()


job_filter_id = {
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