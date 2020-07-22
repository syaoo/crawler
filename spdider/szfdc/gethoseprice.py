# 爬取深圳市房地产信息平台的稳租金商品房数据
# http://zjj.sz.gov.cn:8004/
# 需要使用post方式爬取信息
# Response headers:
# Request URL: http://zjj.sz.gov.cn:8004/api/marketInfoShow/getWzjfyInfoList
# Request Method: POST
# Request headers:
# Origin: http://zjj.sz.gov.cn:8004
# FormData:
    # pageIndex: 1
    # region: 全市
    # minPrice: 0
    # maxPrice: 0
    # type: 0
    # orien: 0
    # status: 0
    # houseNumber:
# FormData source code: pageIndex=1&region=%E5%85%A8%E5%B8%82&minPrice=0&maxPrice=0&type=0&orien=0&status=0&houseNumber=
"""
需要提取的内容较多，使用re正则表达式匹配会很慢，由于解码出来的数据是json文件，因此使用json.loads()转换成字典处理更便捷。
"""
import urllib.request,urllib.parse,json,os,time
import auxiliary.rand_ua_ip as rand_ua_ip

class Writer:
    """
    数据写入器类
    """
    __counter = 0 # 计数器(全局变量)
    def __init__(self,fullpath,title,tip_txt=None):
        self.fullpath = fullpath
        self.title = title
        self.tip_txt = tip_txt
        self.time = time.strftime("%Y-%m-%d,%H:%M:%S",time.localtime())
        self.__write_head()

    def __write_line(self):
        """
        # 将列表写入文件，列表元素间用\t分隔，末位写入\n
        """
        with open(self.fullpath,'a') as f: # 注意这里应使用追加模式写入
            for i in range(len(self.title)-1):
                f.write("{}\t".format(self.title[i]))
            f.write("{}\n".format(self.title[-1]))
            
    def __write_head(self):
        """
        写入文件头
        """
        if self.tip_txt:
            # 如果tip_txt~=None，写入提示信息,文件写入时间和标题
            with open(self.fullpath,'w') as f: # 打开一个文件只用于写入
                f.write("Tip: {} Write @ {}\n".format(self.tip_txt,self.time))
            self.__write_line()
            self.__counter += 2
        else:
            # 如果tip_txt==None，仅写入文件写入时间和标题
            with open(self.fullpath,'w') as f: #打开一个文件只用于写入
                f.write("Write Time @ {}\n".format(self.time))
                # f.write("av号, 投币, 弹幕, 收藏, 点赞, 评论, 分享, 播放, 评分, 标题\n")
            self.__write_line()
            self.__counter += 2

    def write_data(self,info_dict):
        """
        将字典info_dict的数据按行写入文件，info_dict中的键值应包含title中的值所有值
        return：写入数据的行数
        """
        with open(self.fullpath,'a') as f: # a-打开一个文件用于追加
            # 中间\t分割，末位\n
            for key in self.title[:-1]:
                f.write("{}\t ".format(info_dict[key]))
            f.write("{}\n".format(info_dict[self.title[-1]]))
            self.__counter += 1
            # print(self.__counter)
        return self.__counter # 写入成功

if __name__ == "__main__":
    url = 'http://zjj.sz.gov.cn:8004/api/marketInfoShow/getWzjfyInfoList'
    ua = rand_ua_ip.random_ua()
    headers = {
        'User-Agent':ua,
        'host': 'zjj.sz.gov.cn:8004',
        'Origin':'http://zjj.sz.gov.cn:8004',
    }
    dirpath = 'spdider/szfdc/data'
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    fname = time.strftime('%Y%m%d%H%M',time.localtime())+'.txt'
    fullpath = os.path.join(dirpath,fname)
    title = ['rownum_', 'houses_floor_space', 'rent_price', 'ho_orien', 'houses_floor_no',  'houses_rm_no', 'houses_type', 'proj_region', 'proj_name', 'deco_type', 'ho_id']
    thewriter = Writer(fullpath,title) # 初始化写入器
    for i in range(1,13):
        formdata = {'pageIndex': 1,'region': '全市','minPrice': 0,'maxPrice': 0,
            'type': 0,'orien': 0,'status': 0,'houseNumber':'',}
        formdata['pageIndex']=i
        formdata = urllib.parse.urlencode(formdata)
        formdata = formdata.encode('utf-8') # 需要编码成字节
        req = urllib.request.Request(url, headers=headers,data=formdata,method='POST')
        try:
            return_data = urllib.request.urlopen(req)
            raw_data = return_data.read().decode('utf-8')
            # 将json转换为字典
            data_dict = json.loads(raw_data)
            data_list = data_dict['data']['list']
            for i in data_list:
                count = thewriter.write_data(i)
            print("写入{}条数据".format(count))
        except Exception as e:
                print(e)