import yaml
import re
import traceback
from rogue_tools import path_tool

'''
    配合proto_tool使用，通过这个来获得【extension_name和io接口名称】
    通过这两个参数，就可以引入proto导出的xxxxx_pb2.py。
'''
class YamlGrop():
    '''
    所有yaml的聚合类\n
    '''
    def __init__(self,folder) -> None:
        self.yaml_dic = {}
        self.yaml_name_list=[]
        sub_list = path_tool.get_sub_files(folder,full_path=True,include='.yaml',exclude='EnumDef.yaml')
        for sub_file in sub_list:
            yaml = YamlObj(sub_file)
            self.yaml_dic[yaml.ext_id]=yaml
            self.yaml_dic[yaml.name]=yaml
            self.yaml_name_list.append(yaml.name)

    def get_all_yaml_name_list(self):
        return self.yaml_name_list

    def get_yaml(self,ext_id_or_name):
        return self.yaml_dic.get(ext_id_or_name,None)

    def get_yaml_name(self,ext_id_or_name):
        '''
        尽量不要使用，使用get_yaml_info替代
        '''
        yaml = self.get_yaml(ext_id_or_name)
        return yaml.name if yaml else None


    def get_yaml_request_name(self,ext_id_or_name,cmd_id):
        '''
        尽量不要使用，使用get_yaml_info替代
        '''
        return self.yaml_dic[ext_id_or_name].get_request_name(cmd_id)

    def get_yaml_reply_name(self,ext_id_or_name,cmd_id):
        '''
        尽量不要使用，使用get_yaml_info替代
        '''
        return self.yaml_dic[ext_id_or_name].get_reply_name(cmd_id)

    def get_yaml_info(self,ext_id_or_name,cmd_id):
        '''
        获得一个接口的信息
        '''
        yaml = self.get_yaml(ext_id_or_name)
        if not yaml:
            return None,None,None
        yaml_name = yaml.name
        if not yaml_name:
            return None,None,None
        request_name = self.get_yaml_request_name(ext_id_or_name,cmd_id)
        reply_name = self.get_yaml_reply_name(ext_id_or_name,cmd_id)
        return yaml_name,request_name,reply_name
class YamlObj():
    '''
    #####################################################################
    #                         一个自定义yaml对象                         #    
    #####################################################################  
    '''
    def __init__(self,file_path):
        self.file_path=file_path
        self.cmd_dic={}
        
        try:
            dic:dict            = yaml.safe_load(open(self.file_path, encoding='utf-8'))
            self.name           = dic.get('name',None)
            self.ext_id         = dic.get('extensionId',None)
            yaml_cmd_list       = dic.get('cmdList',[])

            for cmd in yaml_cmd_list:
                yaml_cmd = YamlCmd(cmd)
                self.cmd_dic[yaml_cmd.index]=yaml_cmd

            
        except Exception as err:
            traceback.print_exc()
    def get_all_cmd(self):
        return self.cmd_dic
        
    def get_extension_name(self):
        return self.name
        
    def get_request_name(self,index:int):
        return self.cmd_dic[index].request

    def get_reply_name(self,index:int):
        return self.cmd_dic[index].reply

class YamlCmd():
    def __init__(self,cmd_line) -> None:

        self.rs_dic={}
        pattern = re.compile(r'[(]([0-9]+)[)]', re.I)   # re.I 表示忽略大小写
        m = pattern.search(cmd_line)
        self.index     = int(m.group()[1:-1])
        self.name      = yaml_cmd_handle(cmd_line,'void')
        self.request   = yaml_cmd_handle(cmd_line,'@in')
        self.reply     = yaml_cmd_handle(cmd_line,'@out')


def yaml_cmd_handle(src_str,start_str):
    pattern = re.compile(r'('+start_str+')([ ]+)([a-z]+)', re.I)   # re.I 表示忽略大小写
    m = pattern.search(src_str)
    if m:
        pattern2 = re.compile(r'([a-z]+)', re.I)
        s=pattern2.search(m.group()[len(start_str):])
        return s.group()
    return None




