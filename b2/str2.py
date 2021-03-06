# coding=utf-8


from exceptions2 import *

__ALL__ = ["replace_all"]

def dict_to_string(data):
    if data and len(data) > 0 and isinstance(data, dict):
        return ' '.join(["%s:%s" % (__key, __val) for __key, __val in data.items()])
    return ''

def is_empty(words):
    if words is None or ( hasattr(words , '__len__') and len(words) ==0):
        return True
    return False

def get_sign_repeat(sign, n):
    judge_str(sign)
    judge_num(n)
    return sign * n


def join_str_list(buf, join_str):
    judge_list(buf)
    judge_str(join_str)
    return join_str.join(buf)


def reverse(words):
    judge_str(words)
    return words[::-1]

def replace_all( word , patterns):
    if isinstance(patterns , basestring):
        return word.replace(patterns)
    if isinstance(patterns , (dict)):
        for pattern in patterns.items():
            word = word.replace(pattern[0],pattern[1])
        return word
    raise TypeError

def get_same_starts(word1, word2):
    '''
    功能:获得字符串相同的开头
    返回： 如果不相同 返回 '' 否则返回 相同部分
    exceptions:
        如果 word1 / word2 不是字符串或者为空 ， 抛出异常
    '''
    judge_str(word1)
    judge_str(word2)
    l = min(len(word1), len(word2))
    for i in range(l):
        if word1[i] != word2[i]:
            return word[: i]
    return word[:l]


def get_same_ends(word1, word2):
    judge_str(word1)
    judge_str(word2)
    l = min(len(word1), len(word2))
    for i in range(l, 0, -1):
        pass


class Buffer2(object):

    '''
    编写类似java stringbuilder 工具类 ，
    将字符串扩展变的容易简单
    '''

    def __init__(self, content=None):
        self.__buf = []
        if content:
            judge_str(content)

    def append(self, line):
        '''
        字符串追加
        '''
        if line == None:
            raise ValueError, 'append value is None !'
        if isinstance(line, (str, unicode, list, tuple)):
            self.__buf.extend(line)
            return
        raise TypeError, 'append function can accept value\'s is list str unicode tuple '

    def __add__(self, line):
        self.append(line)
        return self

    def find_first(self, value):
        judge_str(value)
        if len(value) > len(self.__buf):
            return -1
        return self.__buf.index(value)

    def __len__(self):
        return len(self.__buf)

    def sort(self):
        self.__buf.sort()

    def reverse(self):
        return str(''.join(self.__buf))[::-1]

    def char_at(self, index):
        judge_null(index)
        judge_type(index, (int))
        judge_ge_value(index, 0)
        judge_le_value(index, len(self.__buf))
        return self.__buf(index)

    def __getitem__(self, key):
        return self.charat(index)

    def __setitem__(self, index, value):
        judge_null(index)
        judge_type(index, (int))

    def __str__(self):
        return self.to_str('')

    def to_str(self, join_str=''):
        judge_str(join_str)
        return join_str.join(self.__buf)

    def __eq__(self, val):
        if val == None:
            return False
        if isinstance(val, list):
            return self.__buf == val
        elif isinstance(val, Buffer2):
            return self.__buf == val.__buf
        elif isinstance(val, str):
            return self.to_str() == val
        return False



def upper_char(words, upper_len):
    if len(words) < upper_len:
        upper_len = len(words)
    return ''.join([chr(ord(words[i]) - 32) if i < upper_len and ord(words[i]) <= 122 and ord(words[i]) >= 97 else words[i] for i in range(len(words))])

def iconvft(content , code1 = "gbk",code2 = "utf-8",ignore = False):
    if content is None:
        return content
    return content.decode(code1).encode(code2) if ignore is False else content.decode(code1,"ignore").encode(code2)
