import requests
import json
import base64
import hashlib

def robot(key, data):
    # 企业微信机器人的 webhook
    # 开发文档 https://work.weixin.qq.com/api/doc#90000/90136/91770
    webhook = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    headers = {'content-type': 'application/json'}  # 请求头
    r = requests.post(webhook, headers=headers, data=json.dumps(data))
    r.encoding = 'utf-8'
    # print(f'执行内容:{data}, 参数:{r.text}')
    # print(f'webhook 发送结果:{r.text}')
    return r.text


def bot_push(key, data):
    if type(key)!=str:
        print(f'webhook参数错误1:{key}_data')
        return
    if  len(key) == 0:
        print(f'webhook参数错误2:{key}_data')
        return

    try:
        res = robot(key, data)
        print(f'webhook 发出完毕: {res}')
        return res
    except Exception as e:
        print(e)


def bot_push_text(key, msg,user_list=[]):
    # 发送文本
    webhook_data = {
        "msgtype": "text",
        "text": {
            "content": msg ,
            "mentioned_list" : user_list
        }
    }

    # 企业微信机器人发送
    bot_push(key, webhook_data)
    return None

def bot_push_markdown(key, title , msg,user_list=[]):
    # 发送文本
	
	
    webhook_data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f'{title}\n<font color=\"comment\">{msg}</font>' ,
            "mentioned_list" : user_list
        }
    }

    # 企业微信机器人发送
    bot_push(key, webhook_data)
    return None

def bot_push_pic(key, pic_path):
    
    pic_obj =None
    with open(pic_path,'rb') as pic:
        pic_obj = pic.read()
    pic_64  =  base64.b64encode(pic_obj)
    pic_str = str(pic_64,'utf-8')
    pic_md5 = hashlib.md5(pic_obj).hexdigest()

    # 发送图片
    webhook_data = {
        "msgtype": "image",
        "image": {
            "base64": pic_str,
            "md5": pic_md5
        }
    }
    # 企业微信机器人发送
    bot_push(key, webhook_data)

    return None




def wx_robot(robot_list,msg,is_debug=False,user_list=[]):
    if is_debug:
        print(f'Debug robot:\n{robot_list}\n{msg},\n{user_list}')
        return
    # 虽然最大支持5120，但是太长了也没啥意义，就1024凑个整吧
    if len(msg)>1024:
        msg = msg[-1024:]
    for key in robot_list:
        bot_push_text(key,msg,user_list)
    
