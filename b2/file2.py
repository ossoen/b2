#coding=utf-8

import os
from exceptions2 import judge_str, judge_null, judge_type
from system2 import reload_utf8
import os
import time

__ALL__ = ["get_caller_dir", "get_caller_file", "read_config_json", "read_dict_format_line", "isdir", "wait_running_flag", "touch", "mkdir_m", "mkdir_p", "mkdir_p_child", "write", "FilesRead", "FilesWrite"]

def isdir(path):
    judge_str(path, 0, (str))
    return os.path.isdir(path)

def rm(file_path , exception = False):
    if file_path is None or os.path.exists(file_path) is False:
        if exception is True:
            raise TypeError
        else:
            return False
    if os.path.isfile(file_path):
        return os.remove(file_path)
    elif os.path.isdir(file_path) and not os.listdir(file_path):
        return os.rmdir(file_path)
    if exception is True:
        raise TypeError("%s is not empty dir" % file_path)
    else:
        return False
def get_caller_file():
    """获得调用者文件绝对路径
        param:
        return:调用者文件绝对路径
        raise None
        test:
            >>> get_caller_file() == os.path.abspath(__file__)
    """
    import inspect
    caller_file = inspect.stack()[1][1]
    return os.path.abspath(caller_file)

def get_caller_dir():
    """获得调用者文件绝对目录路径
        param:
        return:调用者文件绝对目录路径
        raise None
        test:
            >>> get_caller_dir() == os.path.abspath(os.path.dirname(__file__))
    """
    import inspect
    caller_file = inspect.stack()[1][1]
    return os.path.abspath(os.path.dirname(caller_file))

def wait_running_flag(running_flag , wait_time = 0.1 , call_back = None ):
    """等待一个文件删除功能
        params:
            running_flag                    需要等待运行的文件
            wait_time                       为了防止死循环，设置一个循环值
        return:
            True                            函数成功运行
            False                           参数有错误
        raise
            None
        test:
            >>> wait_running_flag("")
    """
    if running_flag is None \
            or isinstance(running_flag ,basestring) is False \
            or os.path.exists(running_flag) \
            or isinstance(wait_time , (float  , int, long)) is False \
            or wait_time <= 0 or (call_back is not None and callable(call_back) is False):
               raise TypeError
    while os.path.exists(running_flag) is False:
        time.sleep(wait_time)
    if call_back is not None:
        call_back(running_flag)
    return True



def touch(path):
    """根据path创建文件
        params:
            path                    需要创建文件类型
        return
            True
            False
        raise
            None
    """
    if path and isinstance(path , basestring):
        with open(path , "a") as f:
            os.utime(path , None)
        return True
    return False

def mkdir_m(path):
    if path:
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
            else:
                raise ValueError, "path [%s] has been create , but isn't dir !" % path
        else:
            return os.mkdir(path)
    raise ValueError, "path is empty , please check !"


def mkdir_p(path):
    if path:
        _paths = os.path.split(path)
        if len(_paths) == 0:
            return True
        mkdir_path = _paths[0]
        for _path in _paths[1:]:
            mkdir_m(mkdir_path)
            mkdir_path = os.path.join(mkdir_path, _path)
        mkdir_m(mkdir_path)
        return True
    else:
        raise ValueError, "path is none or empty , please check !"

def split_path(p):
    if p and len(p) > 0 and isinstance(p,  str):
        return os.path.split(p)



def mkdir_p_child(path, child_path):
    return mkdir_p(os.path.join(path, child_path))


def write(lines,  path, overwrite=True, join_str='\n'):
    judge_str(line, 1, (str))
    judge_str(path, 1, (str))
    judge_null(lines)
    judge_type(
        lines, 'lines type [list , tuple , str , unicode]', (list, tuple, str, unicode))
    if os.path.exists(path) and overwrite == False:
        raise ValueError, 'path is exists! %s' % path
    with open(path, 'w') as f:
        if isinstance(lines, (str, unicode)):
            f.write(lines)
        else:
            f.write(join_str.join([line for line in lines]))

def read_config_json(file_path):
    """从文件内部读取json转换成词典
    """
    content = None
    import json
    with open(file_path) as f:
        contents = "".join(f.readlines())
        return json.loads(contents)


def read_dict_format_line(file_path  , *argv , **kw ):
    """从那件读入
    """
    split_fun = kw.get("split_fun" , lambda x : x.split())
    for attr in argv:
        if isinstance(attr , basestring) is False:
            raise TypeError

    from collections import namedtuple
    from collections import OrderedDict
    _Line = namedtuple("_Line" , " ".join(argv))
    d = OrderedDict()
    with open(file_path) as f:
        for line in f:
            values = split_fun(line.rstrip())
            d[values[0]] = _Line._make(values[1:])
    return d

def walk_folder(root_path, file_filter=lambda x: true, current_level=0):
    '''
    遍历文件夹文件：
    root_path 遍历文件夹
    file_filter 判断文件是否要收录函数 ， 返回 boolean
    '''
    judge_str(root_path, 1, (str))
    files = []
    if os.path.isfile(root_path):
        if file_filter and callable(file_filter):
            if file_filter(root_path):
                files.append(root_path)
        return files
    for f in os.listdir(root_path):
        cur_path = os.path.join(root_path, f)
        if os.path.isfile(cur_path):
            if file_filter and callable(file_filter):
                if file_filter(cur_path):
                    files.append(cur_path)
            else:
                files.append(cur_path)
        elif os.path.isdir(cur_path):
            current_level += 1
            files.extend(walk_folder(cur_path, file_filter, current_level))
    return files


def _create_folder_map(root_path, file_filter=lambda x: True, cur_level=0, limit_level=None):
    '''
    遍历文件夹文件：
    root_path 遍历文件夹
    file_filter 判断文件是否要收录函数 ， 返回 boolean
    '''
    if limit_level != None:
        if cur_level >= limit_level:
            return
    judge_str(root_path, 1, (str))
    file_map = {}
    for f in os.listdir(root_path):
        cur_path = os.path.join(root_path, f)
        if os.path.isfile(cur_path):
            if file_filter and callable(file_filter):
                if file_filter(cur_path):
                    file_map[f] = 'f'
            else:
                file_map[f] = 'f'
        elif os.path.isdir(cur_path):
            cur_level = cur_level + 1
            file_map[cur_path] = _create_folder_map(
                cur_path, file_filter, cur_level=cur_level)
    return file_map


def create_folder_map(root_path, file_filter=lambda x: True, limit_level=None):
    return {root_path: _create_folder_map(root_path, file_filter, limit_level=limit_level)}


class FilesRead(object):
    """多文件读取文件 ， 生成迭代器  ， 只需要next就可以读入文件夹下的所有文件
    """

    def __init__(self,files,**kw):
        if files is None:
            raise ValueError("files is string array!contain file|folder path")
        self.file_filter = kw.get("file_filter" , lambda root , dir , f:  True )
        if self.file_filter is None or callable(self.file_filter) is False:
            raise ValueError("filter is callable!")
        self.files = []
        files_set = set()
        for file_path in files:
            if os.path.isdir(file_path):
                for root,dirs,file_list in os.walk(file_path):
                    for f in file_list:
                        if self.file_filter(root , dirs , f):
                            path = os.path.join(root,f)
                            if path in files_set:
                                continue
                            self.files.append(path)
                            files_set.add(path)
            elif os.path.isfile(file_path) and self.file_filter(None , None , file_path):
                self.files.append(file_path)
                files_set.add(file_path)
        self.__filehandle = None
        self.__file_index = -1
        self.__line_cache = []
        self.__cur_file_path = None

    def __iter__(self):
        return FilesRead(files=self.files)

    def next(self):
        line = self.get_line()
        if not line:
            raise StopIteration, 'files has no content to read!'
        return line.strip('\n')

    def __get_cur_line(self):
        if self.__filehandle:
            return self.__filehandle.readline()
        return None

    def get_line(self):
        """从输入文件夹或者文件中读入一行数据
            params:
                None
            return
                None 如果没有文件可以读取时候
            raise
                None
        """
        line = self.__get_cur_line()
        while not line and self.__file_index < (len(self.files) - 1):
            self.__file_index += 1
            if self.__filehandle:
                self.__filehandle.close()
            self.__cur_file_path = self.files[self.__file_index]
            if not os.path.isfile(self.__cur_file_path):
                continue
            self.change_file(self.__cur_file_path)
            self.__filehandle = open(self.__cur_file_path)
            line = self.__filehandle.readline()
        return line

    def change_file(self, file_path):
        pass

    def is_readall(self, files):
        """判读files参数 ， 是否都可读状态
        """
        if not files:
            return False
        for f in files:
            if f and isinstance(f, str) and (not os.path.isfile(f)):
                return False
        return True

    def get_current_file(self):
        return self.__cur_file_path


class FilesWrite(object):
    """多文件写操作 ，因为很多时候 ，需要拼接多个临时文件，根据一定key的方式
        使用方式：
            fileswirte = FilesWrite("./data" , file_prefix = "tmp_" , file_count = 1000)
            fileswrite.write(key , line )
    """

    def __init__(self , save_path ,file_prefix = "tmp_", file_count = 5000 , write_mode = "w"):
        self.file_count = file_count
        self.file_handles = {}
        mkdir_p(save_path)
        self.save_path = save_path
        self.file_prefix = file_prefix
        self.write_mode = write_mode


    def get_file_id(self , key ):
        if key is None:
            raise Exception , "key error is must be not None"
        return hash(key) % self.file_count

    def get_file_handle(self , part_id ):
        if part_id in self.file_handles:
            return self.file_handles[part_id]
        else:
            if part_id > self.file_count:
                part_id = part_id % self.file_count
            self.file_handles[part_id] = open(os.path.join(self.save_path ,"%s%s"% ( self.file_prefix , str(part_id))) , self.write_mode)
            return self.file_handles[part_id]

    def write(self , key , line):
        """写方法
            params:
                key 写文件的key
                line 文件内容 ， 现在为string ， 没有进行判断
            return:
                None
            raise
                None
        """
        part_id = self.get_file_id(key)
        self.get_file_handle(part_id).write(line)


    def close(self):
        """关闭文件写方法;这个方法不安全，但是现在work
        """
        for part_id in self.file_handles.keys():
            self.file_handles[part_id].close()

    def __len__(self):
        return len(self.file_handles)

    def flush(self):
        for file_handler in  self.file_handles.values():
            file_handler.flush()
