#coding=utf-8


import json
import re

__ALL__ = ["QueryItem" , "JPath"]

class QueryItem(object):

    def __init__(self , argv ,root_path = False):
        self.tag = argv[0]
        self.sub_tag = argv[2]
        self.operator = argv[3]
        self.value = argv[4]
        self.root_path = root_path 
    
    def __str__(self):
        return "root_path={root_path} tag={tag} sub_tag={sub_tag} operator={operator} value={value}".format(tag = self.tag , sub_tag=self.sub_tag , operator = self.operator , value = self.value , root_path = self.root_path )
class JPath(object):

    _parser_regx = re.compile(ur"""^(
            [\w\d\.\*\+_]+
            )(
                \[
                @([\w_\d]+)
                (=|>=|<=|>|<|~){1}
                ([\d\w]+)\]
            )?""" ,re.VERBOSE)


    def __init__(self ):
        self.split_char = "/"
    
    def _obj_2_json(self , obj):
        if obj is None:
            raise ValueError
        if isinstance(obj , basestring):
            return json.loads(obj )
        elif isinstance(obj , dict):
            return obj 
        else:
            raise TypeError

    def _extract_query_item(self , query):
        if query is None:
            raise ValueError("query must be not None !") 
        if isinstance(query , basestring):
            return self._parse_query(query)
        elif isinstance(query ,list):
            for _obj in query:
                if isinstance(_obj , QueryItem) is False:
                    raise TypeError("query is QueryItem list , but contain the item isn't QueryItem!")
            return query     
        else:
            raise TypeError("query type is error , query type in [basestring , QueryItem]!")

    def extract(self ,obj ,  query ):
        """根据
        """
        obj = self._obj_2_json(obj)
        querys = self._extract_query_item(query)
        objs = [obj]
        for query in querys:
            if query.root_path == True :
                objs = [self._find_name(query.tag , obj) for obj in objs]
            else:
                tmpobjs = [] 
                for obj in objs:
                    container = []
                    self._finds_name(query.tag , obj ,container)
                    tmpobjs.extend(container)
                objs = tmpobjs
            if len(objs) != 0 and query.operator and query.sub_tag and query.value:
                objs = [ obj  for obj in objs if self._has_attr(query.sub_tag , obj , query.value , query.operator) ]
            if len(objs) == 0:
                return []
        return objs 
                    
    def _parse_query(self , query):
        """将xpath解析成为程序所需要的query结构体
            params:
                query                   查询结构字符串
            return 
                query_list              [QueryItem]
            raise:
                None 
        """
        query_list = [] 
        query_paths = query.split(self.split_char)
        root_path = True 
        del query_paths[0]
        for qp in query_paths:
            if qp == "" :
                root_path = False
                continue
            query_list.append(QueryItem(self._parser_regx.match(qp).groups() , root_path = root_path))
            root_path = True
        return query_list

    def _finds_name(self , tag , obj , container ):
        """根据查询obj下所有节点的方法
            params
                tag                     需要查询的tag名称，字符串
                obj                     需要查询的json结构体，词典类型
                container               将查询到的json子结构体加在此处
            return 
                None 
            raise 
                None 
        """
        if isinstance(obj , list):
            for _obj in obj:
                self._finds_name(tag , _obj , container)
        elif isinstance(obj , dict):
            self._regx_find_dict(tag , obj , container)
            for key , _obj in obj.items():
                self._finds_name( tag , _obj  , container)
        return 

    def _regx_find_dict(self , tag , obj , container):
        """根据tag正则，当前obj所有key命中tagname
        """
        tag_pattern = re.compile(tag)
        for name , value in obj.items(): 
            match = tag_pattern.match(name)
            if match:
                container.append(value)
        return 
    
    def _has_attr(self , tag , obj , value , operator ):
        """主要是实现语法中对属性进行判断时候使用，实现[@name=="abc"] 等
            params:
                tag                     需要判断的属性value
                obj                     需要判断的结构体
                value                   tag作为key vlaue
                operator                逻辑判断的标识符o
            return 
                True                    有符合规则的属性
                False                   没有匹配上
            raise 
                Exception 
        """
        if obj and isinstance(obj , dict):
            if tag in obj:
                if operator == ">":
                    value = type(obj[tag])(value)
                    return obj[tag] > value 
                elif operator == "=":
                    _value = (type(obj[tag])(value))
                    return (obj[tag] == _value )
                elif operator == "<":
                    value = type(obj[tag])(value)
                    return obj[tag] < value 
                elif operator == ">=":
                    value = type(obj[tag])(value)
                    return obj[tag] >= value 
                elif operator == "<=":
                    value = type(obj[tag])(value)
                    return obj[tag] <= value 
                elif operator == "~":
                    match = re.compile(value).match(str(obj[tag]))
                    if match:
                        return True
        else:
            return False

    def _find_name(self , tag , obj ):
        if obj and isinstance(obj , dict):
            if tag in obj:
                return obj[tag]
        return None 

if __name__ == "__main__":

    obj = json.loads('{"a":{"b":1 , "c":1} , "d":[{"a":5}]}')
    container = []
    import sys
    x = JPath()
    print x.extract(obj , "/a[@c=1]/c")
