import urllib.request,re
#####
#这里也遇到了编码错误问题，在另一个脚本中注释Accept-Encoding可以解决，但是这里一开始并没有添加这项；最后通过gzip模块decompress才得以解决。
#####

def reExt(url,pattern,headers=None):
    """
    根据正则表达式提取网页中的数据
    参数：
        url - 网页地址
        pattern - 正则表达式
        headers - 请求头信息，默认为空
    返回值：包含匹配结果的元组
    """
    print(url)
    req = urllib.request.Request(url=url,headers=headers)
    try:
        res = urllib.request.urlopen(req)
        dat = res.read().decode('utf-8','ignore')
        rlist = re.compile(pattern).findall(dat)
        return rlist
    except Exception as e:
        print(e)

def Psearch(kwds,pages=1):
    headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    url = 'http://www.bilibili.com/video/search?search='+urllib.request.quote(kwds)
    print(url)
    # <a href="/view_video.php?viewkey=ph5e530f292587a" title="hezo_21" class=""  
    pat = 'viewkey=(.*?)".*?title="(.*?)".*?class=""'
    rlist = list(reExt(url, pat,headers))
    if pages>1:
        for i in range(2,pages+1):
            url = url+'page='+str(i)
            rlist.extend(list(reExt(url,pat,headers)))
    return rlist

if __name__ == "__main__":
    url = "https://www.bilibili.com/video/av92334934"
    headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    vl = Psearch("qw",2)
    for i in vl:
        print(i)
    print(len(vl))
    # base_url = "https://www.tubeoffline.com/downloadFrom.php?host=bilibili&video="
    # vurl = "http://www.bilibili.com/view_video.php?viewkey=cd3ded482659727ee9d9"
    # vurl = urllib.parse.quote(vurl,safe='')
    # pat = '<td>(.*?)p</td><td>mp4</td><td><a href="(.*?)"'
    # rlist = reExt(base_url+vurl,pat,headers)
    # print(rlist)
    # for i in rlist: