"""
系统配置服务
本系统使用 json5 作为配置文件格式
(TOML不支持异质数组， 如 [1, '井眼井深', 0, 'm'])
"""
from __future__ import annotations
import os
import pyjson5 as qjson  # 非常奇怪，不知道怎么格式化输出
import json5 as json  # 要输出的时候改成这个，比较慢的

DEF_CFG_NAME = ''       # 主程序首次调用 Config() 时设置
LOCAL_CONF_DIR = ''     # 本地外部配置文件目录名
CONF_EXT = '.json5'


class ConfigError(Exception):
    def __init__(self, conf_name):
        filenames = [Config.conf_file_path(conf_name)]
        if conf_name != DEF_CFG_NAME:
            filenames.append(Config.conf_file_path(DEF_CFG_NAME))
        super().__init__('不存在任何配置文件', filenames)


class ConfigNode(dict):
    # done：增加parent属性，自动从parent.default获取参数
    __old_setattr__ = object.__setattr__

    # __old_getattr__ = object.__getattr__
    # __setattr__ = dict.__setitem__

    # __getattr__ = dict.__getitem__
    def __setattr__(self, key, value):
        # if key == '_parent' or key == '_default' or key == 'parent' or key == 'default':
        if key == '_parent' or key == 'parent':
            self.__old_setattr__(key, value)
        else:
            self.__setitem__(key, value)

    def __getattr__(self, key):
        # result = self.get(key) or self.parent and self.parent.default and self.parent.default.get(key)
        if key == '_parent':
            return self.__getattribute__(key)
        result = self.get(key)
        if result is None and self.parent is not None:
            default = self.parent.default
            if default is not None and default != self:
                result = default.get(key)
        return result

    def __init__(self, dict_=None, parent: ConfigNode = None):
        super().__init__()
        self._parent = parent
        # self._default = None
        if dict_ is not None:
            for k, v in dict_.items():
                self[k] = self.from_value(v, self)

    def assign_default(self, default):
        for key in default:
            l = self.get(key)
            if l is None:
                self[key] = default[key]
            elif isinstance(l, ConfigNode):
                l.assign_default(default[key])

    def assign_local(self, local):
        for key in local:
            # 'net_gate.tt_addr.host': 'localhost'
            if key == 'cfgVersion':
                continue
            default_value = self.value_of(key)
            local_value = local.get(key)
            if default_value is not None and local_value is not None and local_value != default_value:
                self.set_value(key, local_value)

    def take_local_settings(self, values: dict = None):
        local = ConfigNode({'cfg_version': self.cfg_version})
        for key in self.envSettingNotes:
            default_value = self.value_of(key)
            value = default_value
            if values is not None:
                value = values.get(key)
                if value is None:
                    value = default_value
                if isinstance(value, str) and isinstance(default_value, int):
                    try:
                        value = int(value)
                    except:
                        value = default_value
            if value != default_value:
                Config.root.set_value(key, value)
                setattr(local, key, value)
        return local

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @classmethod
    def from_value(cls, value, node=None):
        if isinstance(value, ConfigNode):
            value.parent = node
            return value
        if isinstance(value, dict):
            return cls(value, node)
        if isinstance(value, list):
            for i in range(0, len(value)):
                value[i] = cls.from_value(value[i])
        return value

    def value_of(self, path):
        result = self
        names = path.split('.')
        for name in names:
            # result = result.get(name)
            result = getattr(result, name)
            if result is None:
                break
        return result

    def set_value(self, path, value):
        _parent = self
        names = path.split('.')
        for i in range(0, len(names) - 1):
            _parent = getattr(_parent, names[i])
            if _parent is None:
                break
        if _parent is not None:
            setattr(_parent, names[i + 1], value)


class Config:
    main: Config = None
    root: ConfigNode = None
    """
    第一个创建的实例将作为系统的主配置对象
    """

    def __init__(self, conf_name=None, default='', local_dir='', show_message=print):
        if Config.main is None:
            Config.main = self
        self.root: ConfigNode = None
        global DEF_CFG_NAME, LOCAL_CONF_DIR
        self.conf_name = conf_name or default or DEF_CFG_NAME
        if default != '' and DEF_CFG_NAME == '':
            DEF_CFG_NAME = default
        if DEF_CFG_NAME == '':
            raise Exception('编码错误：首次调用Config()必须指定default=?')
        if local_dir != '' and LOCAL_CONF_DIR == '':
            LOCAL_CONF_DIR = local_dir
        if LOCAL_CONF_DIR == '':
            raise Exception('编码错误：首次调用Config()必须指定local_dir=?')

        # self.default = self.open_conf_file(default, local=False)
        # self.root = self.open_conf_file(self.conf_name, local=True)
        # self._root = ConfigNode({'local': self.root, 'default': self.default})
        # self.root = self._root.local
        # self.default = self._root.default

        inner = self.open_conf_file(default, local=False)
        if self.conf_name == DEF_CFG_NAME:
            self.root = inner
            if Config.root is None:
                Config.root = self.root
        local = self.open_conf_file(self.conf_name, local=True, show_message=show_message)
        if self.conf_name != DEF_CFG_NAME:
            self.default = inner
            self.root = local
            self.root.assign_default(self.default)

    def get_value(self, path):
        result = None
        if self.root is not None:
            result = self._value_of(self.root, path)
        if result is None and self.default is not None:
            result = self._value_of(self.default, path)
        return result

    @classmethod
    def _value_of(cls, root: ConfigNode, path):
        return root.value_of(path)

    @classmethod
    def _set_value(cls, root, path, value):
        parent = root
        names = path.split('.')
        for i in range(0, len(names) - 1):
            parent = getattr(parent, names[i])
            if parent is None:
                break
        if parent is not None:
            setattr(parent, names[i + 1], value)

    def get_object(self, path):
        result = self.get_value(path)
        # return ConfigNode(result)
        return result

    @staticmethod
    def conf_path(sub_name=None, local=False):
        if local:
            path = os.path.abspath(os.path.join(os.getcwd(), '..', LOCAL_CONF_DIR))
        else:
            path = os.path.join(os.getcwd(), 'config')
        if sub_name is not None:
            path = os.path.join(path, sub_name)
        return path

    @staticmethod
    def conf_file_path(conf_name, local=False):
        return Config.conf_path(sub_name=f"{conf_name}{CONF_EXT}", local=local)

    @classmethod
    def open_conf_file(cls, conf_name, local=False, show_message=print):
        conf_file = cls.conf_file_path(conf_name, local)
        if local and (conf_name == DEF_CFG_NAME):
            # 检查本地配置文件
            return cls.check_local_config(cls.root, show_message=show_message)
        return cls.load_from(conf_file)

    @classmethod
    def check_local_config(cls, root: ConfigNode, show_message=print):
        # default = cls.main.default
        # default_ver = default.get('cfg_version')
        # default_file = cls.conf_file_path(DEF_CFG_NAME, local=False)
        local_file = cls.conf_file_path(DEF_CFG_NAME, local=True)
        _dir = os.path.dirname(local_file)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        # if not os.path.exists(local_file):
        #     _dir = os.path.dirname(local_file)
        #     if not os.path.exists(_dir):
        #         os.makedirs(_dir)
        #     # 第一次，不改版本号，以便能够直接运行，增强用户信心
        #     copyfile(default_file, local_file)
        local = None
        if os.path.exists(local_file):
            local = cls.load_from(local_file)
            local_ver = local.cfg_version
            if local_ver == root.cfg_version:
                if local_ver >= '1.4':
                    root.assign_local(local)
                return local
            # 若本地文件版本不匹配，则重命名以作备份
            if local_ver != '0.0':
                n, e = os.path.splitext(local_file)
                new_file = f'{n}-{local_ver}{e}'
                if os.path.exists(new_file):
                    os.remove(local_file)
                else:
                    os.rename(local_file, new_file)

        # with open(default_file, mode='r', encoding='utf-8') as f:
        #     cfgstr = f.read()
        # cfgstr = cfgstr.replace(f"cfg_version: '{default_ver}',", "cfg_version: '0.0',")
        # # todo: 应该注释掉除版本号以外的内容
        # with open(local_file, mode='w', encoding='utf-8') as f:
        #     f.write(cfgstr)
        # raise Exception(f'系统为你创建了新的本机配置文件，请重新编辑配置文件，正确设置各项内容后，将版本号设置为{default_ver}\r\n'
        #                 f'文件：《{local_file}》')

        # local = root.take_local_sample()
        # cfgstr = json.dumps(local, indent=4, sort_keys=False, ensure_ascii=False)
        # with open(local_file, mode='w', encoding='utf-8') as f:
        #     f.write(cfgstr)
        local = cls.create_local_config(root, local)
        local_ver = local.cfg_version
        if local_ver >= '1.4':
            root.assign_local(local)
        show_message('系统配置已更新，请进入系统后，尽快打开配置界面，检查各项设置')

    @classmethod
    def create_local_config(cls, root: ConfigNode, values: dict = None):
        local = root.take_local_settings(values)
        cls.save_to_file(local, DEF_CFG_NAME, local=True)
        return local

    @classmethod
    def object_of(cls, path):
        return cls.main.get_object(path)

    @classmethod
    def value_of(cls, path):
        return cls.main.get_value(path)

    @classmethod
    def load_from(cls, conf_file, no_err=False):
        result = None
        if os.path.exists(conf_file):
            with open(conf_file, mode='r', encoding='utf-8') as f:
                # ext = os.path.splitext(conf_file)[1].lower()
                # if ext == '.json' or ext == '.json5':
                #     result = json.load(f)
                # elif ext == '.toml':
                #     result = toml.load(f)
                result = qjson.load(f)
        else:
            if no_err:
                return None
            raise FileNotFoundError(conf_file)
            # raise Exception(f'文件不存在<<{conf_file}>>')
        return ConfigNode.from_value(result)

    @classmethod
    def save_to_file(cls, conf: ConfigNode, conf_name, local=False):
        conf_file = cls.conf_file_path(conf_name, local)
        cfgstr = json.dumps(conf, indent=4, sort_keys=False, ensure_ascii=False)
        with open(conf_file, mode='w', encoding='utf-8') as f:
            f.write(cfgstr)
        return conf_file

    @classmethod
    def del_conf_file(cls, conf_name, local=False):
        conf_file = cls.conf_file_path(conf_name, local)
        if os.path.exists(conf_file):
            os.unlink(conf_file)
            return conf_file
        return None

    @classmethod
    def assign_local(cls, root, local):
        for key in local:
            # 'net_gate.tt_addr.host': 'localhost'
            if key == 'cfgVersion':
                continue
            default_value = cls._value_of(root, key)
            local_value = local.get(key)
            if default_value is not None and local_value is not None and local_value != default_value:
                cls._set_value(root, key, local_value)
