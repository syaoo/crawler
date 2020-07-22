# 该url可得到含有相应排行信息的js文件（综合评分前100每位up1个视频）
# rid=分区，day=统计周期，type=榜单类型，arc_type=近期投稿1、全部投稿0
# url = "https://api.bilibili.com/x/web-interface/ranking?rid=0&day=3&type=1&arc_type=1&jsonp=jsonp&callback=__jp12" 
#

# 获取相应的排行网页，参数：榜单类型，分区，投稿类型（近期、全部），统计周期
# url = "https://www.bilibili.com/ranking/all/0/1/3"
#

# 项目中将使用后一个URL获取所需数据
import lxml.etree
import re,os,numpy,time
from auxiliary import bili



def ext_list(url,ua=None):
    """
    提取排行数据，返回av号及评分列表。
    """
    ##转为etree通过xpath提取
    data = bili.get_rawdata(url)
    if data:
        etdat = lxml.etree.HTML(data)
        tip_txt = etdat.xpath('//span[@class="tip-txt"]/text()')
        print(tip_txt)  #评分统计说明
        avlist = etdat.xpath('//div[@class="info"]/a/@href')  #评分前100视频的URL
        ptslist = etdat.xpath('//div[@class="info"]//div[@class="pts"]/div/text()')  #评分前100视频的综合评分
        tltlist = etdat.xpath('//div[@class="info"]/a/text()') #评分前100视频的标题
        avlist.extend(etdat.xpath('//a[@class="other-link"]/@href'))  #进入前100的up其视频URL
        ptslist.extend(etdat.xpath('//a[@class="other-link"]/strong/text()'))  #进入前100的up其视频综合评分
        tltlist.extend(etdat.xpath('//a[@class="other-link"]/span[@class="title"]/text()'))
        # avlist = [re.search(r"av\d+",i).group() for i  in avlist]
        avlist = [re.findall(r"av\d+",i)[0] for i  in avlist]
        return [tip_txt,tltlist,avlist,ptslist]
    else:
        return [[],[],[]]

def ext_stats(aid,ua=None):
    """
    aid = 视频av号,'av92531906' or '92531906'都可以
    提取指定视频的统计数据：播放、弹幕、评论、收藏、投币、分享、点赞数量
    """
    aid = aid.lower().replace('av','')
    url = "https://api.bilibili.com/x/web-interface/archive/stat?aid="+aid
    data = bili.get_rawdata(url)
    if data:
        # 视频存在时返回数据中code字段为0；
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
            return sta_dat
        else:
            mes = re.findall(r'"message":(.*?),',data)
            print("{}:[ av{} ]不存在!".format(mes[0],aid))
            return None
    else:
        return None

class Writer:
    """
    数据写入类
    后面可把字段改为参数使用，提高类的通用性。
    keys = ['aid','coin', 'danmaku', 'favorite', 'like', 'reply', 'share', 'view', 'score']
    """
    __counter = 0 # 计数器(全局变量)
    def __init__(self,fullpath,tip_txt=None):
        self.fullpath = fullpath
        self.tip_txt = tip_txt
        self.time = time.strftime("%Y-%m-%d,%H:%M:%S",time.localtime())
        self.write_head()
    def write_head(self):
        """
        写入文件头
        """
        if self.tip_txt:
            # 如果tip_txt~=None，写入提示信息,文件写入时间和标题
            with open(self.fullpath,'w') as f: # 打开一个文件只用于写入
                f.write("Tip: {} Write @ {}\n".format(self.tip_txt,self.time))
                # f.write("av号, 投币, 弹幕, 收藏, 点赞, 评论, 分享, 播放, 评分, 标题\n")
                # f.write("aid, coin, danmaku, favorite, like, reply, share, view, score, title\n") 
                # # 逗号分割, 标题中的,/，可能会引起pandas读取错误
                f.write("aid\tcoin\tdanmaku\tfavorite\tlike\treply\tshare\tview\tscore\ttitle\n") # \t分割
                self.__counter += 2
        else:
            # 如果tip_txt==None，仅写入文件写入时间和标题
            with open(self.fullpath,'w') as f: #打开一个文件只用于写入
                f.write("Write @ {}\n".format(self.time))
                # f.write("av号, 投币, 弹幕, 收藏, 点赞, 评论, 分享, 播放, 评分, 标题\n")
                f.write("aid, coin, danmaku, favorite, like, reply, share, view, score, title\n")
                self.__counter += 2

    def write_data(self,info_dict):
        """
        # 写视频统计信息
        info_dict = {
            "aid":92901768,"view":4172775,"danmaku":23545,"reply":13834,
            "favorite":162624,"coin":207696,"share":66406,"like":335059,'score':132,"title":"adfa"}
        Write
        """
        # 写入视频统计信息
        keys = ['aid','coin', 'danmaku', 'favorite', 'like', 'reply', 'share', 'view', 'score']
        try:
            with open(self.fullpath,'a') as f: # a-打开一个文件用于追加
                for key in keys:
                    # f.write("{}, ".format(info_dict[key]))
                    f.write("{}\t ".format(info_dict[key]))
                f.write("{}\n".format(info_dict["title"]))
                self.__counter += 1
                # print(self.__counter)
            return 0 # 写入成功
        except Exception as e:
            raise Exception("{}:The error occurred in Write Video Info.".format(e))

if __name__ == "__main__":
    """
    测试
    """
    yaml_path = "./urllib4bili/items.yaml"
    url_list = bili.urlbuilder(yaml_path)

    # url = "https://www.bilibili.com/ranking/all/0/0/5"
    # url = "https://api.bilibili.com/x/web-interface/archive/stat?aid=92954385"
    for i in range(len(url_list[0])):

        tip_txt,tltlist,avlist,ptslist = ext_list(url_list[1][i])

        if len(ptslist) == len(avlist):
            # 榜单列表遍历
            dirpath = "./urllib4bili/data/"
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            sub_dir = url_list[0][i]
            fullpath = os.path.join(dirpath, sub_dir)
            if not os.path.exists(fullpath):
                os.mkdir(fullpath)
            fname = time.strftime("%Y%m%d",time.localtime())
            fullpath = os.path.join(fullpath, fname)
            thewriter = Writer(fullpath,tip_txt)  # 实例化Writer类
            for i in range(len(avlist)):
                # 榜单内视频列表遍历
                info_dict = ext_stats(avlist[i])
                info_dict["aid"] = avlist[i]
                info_dict["score"] = ptslist[i]
                info_dict["title"] = tltlist[i]
                # 调用Writer.write_data写入视频统计信息
                a = thewriter.write_data(info_dict)
                print(i+1)
            print('*'*20)
        else:
            raise Exception("ptslist(综合评分列表) and avlist(视频URL列表) 长度不匹配")
    # {"code":0,"message":"0","ttl":1,"data":{"aid":92954385,"bvid":"","view":666979,"danmaku":5308,"reply":2869,"favorite":11392,"coin":39891,"share":3765,"like":69103,"now_rank":0,"his_rank":25,"no_reprint":1,"copyright":1,"argue_msg":"","evaluation":""}}