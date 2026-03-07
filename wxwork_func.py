import os,requests
from requests_toolbelt import MultipartEncoder
from urllib import parse
current_dir  = os.path.dirname(__file__) #当前文件夹
def QYWXSendGroupFile(filepath, url):
    """
    发送微信群组机器人文件
    :param filepath: 文件路径
    :param url: 群组机器人WebHook
    :return:
    """
    # url为群组机器人WebHook，配置项
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="+url
    headers = {
        "content-type": "application/json"
    }
    # 发送文件需要先上传文件获取media_id
    media_id = UploadFile(filepath, url)
    msg={"msgtype":"file","file":{"media_id":media_id}}
    # 发送请求
    try:
        result = requests.post(url, headers=headers, json=msg)
        return True
    except Exception as e:
        print("企业微信机器人发送文件失败,详细信息:" + str(e))
        return False
def UploadFile(filepath, webHookUrl):
    """
    企业微信机器人上传文件，发送文件前需要先上传--要求文件大小在5B~20M之间
    :param filepath: 文件路径
    :param webHookUrl: 群组机器人WebHook
    :return: media_id
    """
    # url为群组机器人WebHook，配置项
    url = webHookUrl
    params = parse.parse_qs(parse.urlparse( webHookUrl ).query)
    print(params)
    webHookKey=params['key'][0]
    upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webHookKey}&type=file'
    headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"}
    filename = os.path.basename(filepath)
    try:
        multipart = MultipartEncoder(
            fields={'filename': filename, 'filelength': '', 'name': 'media', 'media': (filename, open(filepath, 'rb'), 'application/octet-stream')},
            boundary='-------------------------acebdf13572468')
        headers['Content-Type'] = multipart.content_type
        resp = requests.post(upload_url, headers=headers, data=multipart)
        json_res = resp.json()
        if json_res.get('media_id'):
            # print(f"企业微信机器人上传文件成功，file:{filepath}")
            return json_res.get('media_id')
    except Exception as e:
        # print(f"企业微信机器人上传文件失败，file: {filepath}, 详情：{e}")
        print("企业微信机器人上传文件失败,详细信息:" + str(e))
        return ""

#msg_poster("test",driverManage_token)
def msg_poster(w, t):
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "content": t
            }
        }
        requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="+w, json=msg, headers={"Content-Type":"application/json"})