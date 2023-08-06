'''
Copyright [2023] [许灿标]
license: Apache License, Version 2.0
email: lcctoor@outlook.com
'''

import re
from decimal import Decimal
from math import ceil
from collections import deque
import hashlib
from hashlib import shake_256
from fractions import Fraction
from typing import Union


########################################## vbool ##########################################

class vbool():
    '''
        解决 1 == True 的历史遗留问题
    '''
    name: str
    _hash_value: int
    _bool_vlaue: bool
    def __new__(cls, value, name='', _sysValue=False):
        if _sysValue:
            self = object.__new__(cls)
            self.name = name
            self._bool_vlaue = bool(value)
            return self
        else:
            return vtrue if value else vfalse

    def __bool__(self): return self._bool_vlaue
    def __eq__(self, o): return self is o
    def __str__(self): return self.name

vtrue = vbool(True, 'vtrue', _sysValue=True)
vfalse = vbool(False, 'vfalse', _sysValue=True)

uniset = vbool(True, 'uniset', _sysValue=True)  # 全集
empset = vbool(False, 'empset', _sysValue=True)  # 空集

SysEmpty = vbool(False, 'SysEmpty', _sysValue=True)
    # 供开发者调用的表示空的标识, 如:
        # 作为默认参数以识别调用者是否传参
        # 在函数内部作为某种状态标识
    # 此参数只允许函数开发者引用, 禁止函数调用者引用.

########################################## bidict ##########################################

class bidict:
    ''' 双向字典 '''
    def __init__(self):
        self.core = {}
    
    def __setitem__(self, key, value):
        self.pop(key, None)
        self.pop(value, None)
        self.core[key] = value
        self.core[value] = key
    
    def __getitem__(self, key):
        return self.core[key]

    def get(self, key, default=SysEmpty):
        value = self.core.get(key, default)
        if value is SysEmpty:
            {}.get(key)
        return value
    
    def pop(self, key, default=SysEmpty):
        if key in self.core:
            value = self.core.pop(key)
            self.core.pop(value)
            return value
        elif default is SysEmpty:
            {}.pop(key)
        else:
            return default

########################################## ztype ##########################################

class WillCover:
    '''
    如果父类中的某个变量等于此类, 则表示该变量必须在子类中被覆盖.
    '''
    def __init__(self, *vs, **kvs):
        raise Exception('WillCover')


class ztype():
    core: Union[int, float, str, tuple, list, set, dict, Fraction]
    selfType = WillCover

    def __getattr__(self, name):
        return self.core.__getattr__(name)
    
    @classmethod
    def _ztypeCore(cls, obj):
        if isinstance(obj, ztype):
            return obj.core
        return obj
    
    @classmethod
    def _sonTypeCore(cls, obj):
        if isinstance(obj, cls):  # cls的值会随着子类而变化
            return obj.core
        return obj
    
    def __str__(self): return str(self.core)
    def __int__(self): return int(self.core)
    def __float__(self): return float(self.core)
    def __bool__(self): return bool(self.core)
    def str(self): return str(self)
    def int(self): return int(self)
    def float(self): return float(self)
    def bool(self): return bool(self)
    def vbool(self): return vbool(self)

    def __iter__(self): yield from self.core
    def __len__(self): return len(self.core)

    # 默认用内核比较大小
    def __eq__(self, obj): return self.core == self._ztypeCore(obj)
    def __ne__(self, obj): return self.core != self._ztypeCore(obj)
    def __lt__(self, obj): return self.core < self._ztypeCore(obj)
    def __le__(self, obj): return self.core <= self._ztypeCore(obj)
    def __gt__(self, obj): return self.core > self._ztypeCore(obj)
    def __ge__(self, obj): return self.core >= self._ztypeCore(obj)

    # 加减乘除默认用内核操作
    def __mul__(self, n): return self.selfType(self.core * self._ztypeCore(n), SysEmpty)
    def __rmul__(self, n): return self.selfType(self.core * self._ztypeCore(n), SysEmpty)
    def __add__(self, n): return self.selfType(self.core + self._ztypeCore(n), SysEmpty)
    def __radd__(self, n): return self.selfType(self.core + self._ztypeCore(n), SysEmpty)
    def __sub__(self, n): return self.selfType(self.core - self._ztypeCore(n), SysEmpty)
    def __rsub__(self, n): return self.selfType(self._ztypeCore(n) - self.core, SysEmpty)
    def __truediv__(self, n): return self.selfType(self.core / self._ztypeCore(n), SysEmpty)
    def __rtruediv__(self, n): return self.selfType(self._ztypeCore(n) / self.core, SysEmpty)
    def __iadd__(self, n):
        self.core += self._ztypeCore(n)
        return self
    def __isub__(self, n):
        self.core -= self._ztypeCore(n)
        return self.core
    def __imul__(self, n):
        self.core *= self._ztypeCore(n)
        return self
    def __itruediv__(self, n):
        self.core /= self._ztypeCore(n)
        return self


########################################## vnum ##########################################

class vnum(ztype):
    '''
        1. float和int没必要拆成两种, 太麻烦了
        2. 解决浮点数精度问题
    '''
    def __new__(cls, numerator, denominator=SysEmpty):
        self = object.__new__(cls)
        self.selfType = cls
        # 创建core
        numerator = self._intoFraction(numerator)
        if denominator is SysEmpty:
            self.core = numerator
        else:
            self.core = Fraction(numerator, self._intoFraction(denominator))
        return self

    @classmethod
    def _intoFraction(cls, v):
        try:
            v = v._vnum_()  # _vnum_为预处理方法, 它将v处理成本方法能够处理的数据.
        except:
            pass
        if isinstance(v, (int, float)): return Fraction(v)
        if isinstance(v, Fraction): return v
        if isinstance(v, cls): return v.core
        if isinstance(v, str): return Fraction(Decimal(v))
        if v in (None,): return Fraction(0)
        raise TypeError(type(v))

    def __hash__(self): return hash(self.core)  # 使用内核的哈希值作为字典的键


########################################## vdict ##########################################

def _XpathGet(dic, i, keySize, keys):
    if i < keySize and type(dic) is dict:
        ikey = keys[i]
        for k, v in dic.items():
            if k == ikey:
                if i == keySize - 1:
                    return v
                value = _XpathGet(v, i + 1, keySize, keys)
                if value is not SysEmpty:
                    return value
            else:
                value = _XpathGet(v, i, keySize, keys)
                if value is not SysEmpty:
                    return value
    return SysEmpty


class vdict(ztype):
    def __new__(cls, obj=SysEmpty, **kvs):
        self = object.__new__(cls)
        self.selfType = cls
        # 创建core
        if obj is SysEmpty:
            self.core = kvs
        else:
            try:
                self.core = dict(obj)
            except:
                try:
                    self.core = dict(obj._dict_())
                except:
                    if obj in (None,):
                        self.core = {}
                    else:
                        raise ValueError(obj)
        return self

    def xpath(self, *keys):
        '''
            一个查找字典的子孙键的工具.
            使用场景: 当字典的结构具有不确定性, 或者要获取的键位于较深层的子孙层时, 可使用该函数进行取值.
        '''
        if not isinstance(keys, tuple):
            keys = (keys, )
        value = _XpathGet(self.core, 0, len(keys), keys)
        if value is SysEmpty:
            raise KeyError(keys)
        return value
    
    def deepGet(self, *keys, default=None):
        res = self.core
        try:
            for k in keys:
                res = res[k]
            return res
        except:
            return default

########################################## vstr ##########################################

class vstr(ztype):

    s_a = 'abcdefghijklmnopqrstuvwxyz'
    s_A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s_0 = '0123456789'
    s_0a = '0123456789abcdefghijklmnopqrstuvwxyz'
    s_0A = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s_aA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s_0aA = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __new__(cls, obj=SysEmpty, **kvs):
        self = object.__new__(cls)
        self.selfType = cls
        self.core = str(obj)
        return self

    def wash_paragraph(self):  # 单段清洗
        text = re.sub('\s+', ' ', self.core)
        text = re.sub('^ +', '', text)
        text = re.sub(' +$', '', text)
        return vstr(text)

    def sub(self, pattern, repl, count=0, flags=0):
        return vstr(re.sub(pattern, repl, self.core, count, flags))

    def visible(self):  # 是否含可视字符
        return vbool(re.search('[^\s]', self.core))

    def has_sound(self):   # 是否含有有声字符(支持中文和英文)
        return vbool(re.search('[\u4e00-\u9fa5\da-zA-Z]', self.core))

    def has_chinese(self):
        return vbool(re.search('[\u4e00-\u9fa5]', self.core))

    def __bytes__(self): return self.core.encode('utf8')

    def md5(self, rtype=str):
        value = hashlib.md5(bytes(self))
        if rtype in (str, 'str'): return value.hexdigest()
        if rtype in (bytes, 'bytes'): return value.digest()
        if rtype in (vstr, 'vstr'): return vstr(value.hexdigest())
        raise TypeError(rtype)

    def shake256(self, rtype='vstr', rsize=32):
        value = shake_256(bytes(self))
        if rtype is str: return value.hexdigest(ceil(rsize/2))[:rsize]
        if rtype in ('vstr', vstr): return vstr(value.hexdigest(ceil(rsize/2))[:rsize])
        if rtype is bytes: return value.digest(rsize)
        raise TypeError(rtype)

    def __hash__(self): return hash(self.core)  # 使用内核的哈希值作为字典的键
    def __contains__(self, obj): return self._sonTypeCore(obj) in self.core


########################################## vbytes ##########################################

class vbytes(ztype):

    def __new__(cls, obj=b''):
        self = object.__new__(cls)
        self.selfType = cls
        try:
            self.core = bytes(obj)
        except:
            if isinstance(obj, str):
                self.core = obj.encode('utf8')
            elif isinstance(obj, (int, float)):
                self.core = bytes([int(obj)])
            elif obj in (None,):
                self.core = b''
            else:
                raise
        return self


########################################## ToolPool ##########################################

class ToolPool():
    def __init__(self, mktool, minlen:int=0, maxlen=None):
        self.mktool = mktool
        self.pool = deque([mktool() for i in range(minlen or 0)], maxlen=maxlen)
    
    def put(self, obj):  # 右进
        self.pool.append(self.beforePut(obj))
    
    def get(self):  # 左出
        try:
            return self.beforeGet(self.pool.popleft())
        except:
            return self.mktool()
    
    def beforeGet(self, obj): return obj
    def beforePut(self, obj): return obj