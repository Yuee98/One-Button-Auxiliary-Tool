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


class js:
    def __init__(self, path) -> None:
        self.f = open(path, 'r', encoding='utf-8')
        self.vars = {}

    def keys(self):
        return self.vars.keys()

    def __getattr__(self, key):
        if key in self.vars:
            return self.vars[key]
        else:
            return None

    def eval(self):
        var_list = ['actions', 'key_levels', 'key_times', 'variables']
        for var in var_list:
            locals()[var] = var
        for i in range(1, 16):
            locals()[f'action_{i}'] = f'action_{i}'
        
        line = self.f.readline()
        while line:
            if line.startswith('const'):
                name = line.split('=')[0][5:].strip()
                context = line.split('=')[-1].replace('//', '#')
                if '[' in context:
                    end = ']'
                elif '{' in context:
                    end = '}'
                else:
                    raise ValueError
                
                line = self.f.readline().replace('//', '#')
                while not line.startswith(end):
                    context += line
                    line = self.f.readline().replace('//', '#')
                context += line

                self.vars[name] = eval(context)
            line = self.f.readline()
        self.f.close()
        
        return self

