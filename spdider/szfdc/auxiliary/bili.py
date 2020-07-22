import yaml, re,urllib.request
# import gzip
# rand_ua_ip的下面两种导入方式，前者从包外导入时可以，后运行该文件时可以，原因不明。
from auxiliary import rand_ua_ip # 从包外导入时使用
# import rand_ua_ip # 运行该文件时使用

def urlbuilder(yaml_path):
    """
    yaml_path是输入的yaml文件地址
    根据输入的YAML文件构造网页链接，返回保存有链接的列表
    """
    try:
        # 读取yaml文件
        with open(yaml_path,'r') as f:
            dat = yaml.loader.BaseLoader(f)
            dat = dat.get_data()
    except Exception as e:
        raise Exception(e)
    # "https://www.bilibili.com/ranking/榜单类型/分区/投稿时间/统计周期"
    base_url = "https://www.bilibili.com/ranking/"
    url_list = [[],[]]
    key_lists = list(dat.keys())
    for key, value in dat[key_lists[0]].items():
        # 榜单类型 
        rankMenu = value
        for key1, value1 in dat[key_lists[1]].items():
            # 分区
            if key == "新人榜" and key1 == "国创相关":
                # 新人榜里没有“国创相关”
                continue
            rankTab = str(value1)
            for key2, value2 in dat[key_lists[2]].items():
                # 投稿时间：1-近期投稿、0-全部投稿
                if key == "新人榜":
                    rankType = '0'
                else:
                    rankType = str(value2)
                for key3, value3 in dat[key_lists[3]].items():
                    period = str(value3)
                    url_list[0].append(".".join([key,key1,key2,key3])) # 名字
                    url_list[1].append(base_url+"/".join([rankMenu,rankTab,rankType,period])) # 地址
    return url_list

def get_rawdata(url,ua=None):
    """
    打开网页并返回解码后的数据,出现异常时返回None
    默认随机UA，
    当ua为字符串时或仅有一个值的列表时使用固定UA，为列表时从其中随机选择使用。
    """
    if ua is None:
        ua = rand_ua_ip.random_ua()
    elif type(ua) == list and len(ua) > 1:
        ua = rand_ua_ip.random_ua(ua)
    # 构造请求头
    headers = {
        # "Host":"api.bilibili.com",
        "Referer": url,
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
        "User-Agent":ua
    }
    req = urllib.request.Request(url=url,headers=headers)
    try:
        res = urllib.request.urlopen(req)
        # dat = gzip.decompress(res.read()).decode('utf-8','ignore') #gzip.decompress解压数据之后在解码
        raw_data = res.read().decode('utf-8','ignore')
        return raw_data
    except Exception as e:
        print("{},该页面可能不存在!".format(e))
        return None

if __name__ == "__main__":
    # import rand_ua_ip
    # 测试 urlbuilder()
    yaml_path = "./biliInUrllib/items.yaml"
    url_list = urlbuilder(yaml_path)
    [print(i) for i in url_list]
    print(len(url_list))

    # 测试 get_rawdata()
    url = "https://api.bilibili.com/x/web-interface/archive/stat?aid=92954385"
    data = get_rawdata(url)
    if re.findall(r'"code":(.*?),',data) == ["0"]:
        sta_dat = {
            "view" : re.findall(r'"view":(\d+?),',data)[0], # 播放量
            "danmaku" : re.findall(r'"danmaku":(\d+?),',data)[0], # 弹幕
            "reply" : re.findall(r'"reply":(\d+?),',data)[0], # 评论
            "favorite" : re.findall(r'"favorite":(\d+?),',data)[0], # 收藏
            "coin" : re.findall(r'"coin":(\d+?),',data)[0], # 投币
            "share" : re.findall(r'"share":(\d+?),',data)[0], # 分享
            "like" : re.findall(r'"like":(\d+?),',data)[0], # 点赞
        }
        print(sta_dat)
    else:
        mes = re.findall(r'"message":(.*?),',data)
        print("{}:[ av{} ]不存在!".format(mes[0],aid))