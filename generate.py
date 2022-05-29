
import yaml
from tools import md5, check
from static import actions, base, special, buff, job_filter_id


def get_path(job, combo, root='templates/'):
    if combo in base:
        path = root + base[combo]
    elif combo in special:
        path = root + special[combo]
    elif combo in buff:
        path = root + 'changewithbuff.xml'
    else:
        path = root + f'combo{len(actions[job][combo]["actions"]) - 1}stage.xml'
    
    return check(path)


class trigger():
    def __init__(self, job, combo, pos, is_cross=False) -> None:
        self.job = job
        self.combo = combo
        self.pos = pos
        self.is_cross = is_cross


    def parse(self, pipe):
        conf = actions[self.job][self.combo]
        path = get_path(self.job, self.combo)
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()[2:-1]
        
        tmp1 = lines[0].replace('ExportedFolder', 'Folder')
        tmp2 = lines[-1].replace('ExportedFolder', 'Folder')
        lines = [tmp1] + lines[1:-1] + [tmp2]

        text = ''.join(lines)

        settings = {}
        for k, v in conf['actions'].items():
            settings[k] = v
            settings[f'id_{k}'] = md5(self.combo+v)
        
        if 'key_levels' in conf:
            for i, v in enumerate(conf['key_levels']):
                settings[f'key_level_{i}'] = v
        
        if 'key_times' in conf:
            for i, v in enumerate(conf['key_times']):
                settings[f'key_time_{i}'] = v

        if 'variables' in conf:
            for i, v in enumerate(conf['variables']):
                settings[f'var_{i}'] = v
        
        settings['position'] = f'{self.pos[0]} {self.pos[1]}'

        if self.combo in base:
            settings['combo'] = self.combo
        else:
            settings['combo'] = f'{self.combo} {self.pos[0]} {self.pos[1]}'
        settings['id_combo'] = md5(self.combo + str(path))

        if self.is_cross:
            settings['is_cross'] = 'c'
        else:
            settings['is_cross'] = ''
        

        for k, v in settings.items():
            text = text.replace(f'%{k}%', str(v))
        
        pipe.write(text)



class folder():
    def __init__(self, name, ftype=None, specs=None) -> None:
        self.name = name
        self.ftype = ftype
        self.specs = specs
        self.subforders = []
        self.triggers = []


    def add(self, trigger):
        self.triggers.append(trigger)


    def append(self, subforder):
        self.subforders.append(subforder)


    def parse(self, pipe):
        if self.ftype == 'root':
            pipe.write('<?xml version="1.0"?>\n')
            pipe.write('<TriggernometryExport Version="1">\n')
            pipe.write(f'<ExportedFolder Id="{md5(self.name)}" Name="{self.name}" Enabled="true">\n')
        elif self.ftype == 'job':
            pipe.write(f'<Folder FFXIVJobFilterEnabled="True" FFXIVJobFilter="{self.specs}" ')
            pipe.write(f'Id="{md5(self.name)}" Name="{self.name}" Enabled="true">\n')
        else:
            pipe.write(f'<Folder Id="{md5(self.name)}" Name="{self.name}" Enabled="true">\n')
        pipe.write('<Folders>\n')

        if self.subforders != []:
            for subforder in self.subforders:
                subforder.parse(pipe)
        else:
            for trigger in self.triggers:
                trigger.parse(pipe)
        
        pipe.write('</Folders>\n')
        pipe.write('<Triggers />\n')
        if self.ftype == 'root':
            pipe.write('</ExportedFolder>\n')
            pipe.write('</TriggernometryExport>\n')
        else:
            pipe.write('</Folder>\n')



class generator:
    def __init__(self, path) -> None:
        with open(path, encoding='utf-8') as f:
            conf = yaml.safe_load(f)
        mode = conf['mode']
        tree = conf['config']
        if mode == 'Controller':
            is_cross = True
        else:
            is_cross = False
        self.root = folder(mode, ftype='root')
        for role, role_tree in tree.items():
            role_folder = folder(role)
            for job, job_tree in role_tree.items():
                job_folder = folder(job, ftype='job', specs=job_filter_id[job])
                for combo, pos in job_tree.items():
                    job_folder.add(trigger(job, combo, pos, is_cross))
                role_folder.append(job_folder)
            self.root.append(role_folder)
        
    def dump(self, path):
        with open(path, 'w', encoding='utf-8') as pipe:
            self.root.parse(pipe)
        print(f'\n触发器生成成功，存放在 {path}')




if __name__ == '__main__':
    g = generator('pos.yml')
    g.dump('output.xml')