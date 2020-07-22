#### 请求头、正则表达式及XPath、IP代理

# urllib.request 设置请求头及提取数据
import urllib.request,lxml.etree,re
# 两种添加headers的方法：
# 1. urllib.request的Function：build_opener() 返回一个OpenerDirector类
# 2. urllin.request的Class：Request()

url = "https://www.baidu.com/s?wd=ip"
url ="https://cn.bing.com/search?q=ip"
'''
# 法一
# headers使用元组列表的形式构造
headers=[("Cookie","BAIDUID=5C20BDC5049CC021CD18422E8C060591:FG=1"),("User-Agent","Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0")]
proxy_ip = "39.162.232.213:3128"
proxy = urllib.request.ProxyHandler({"http":proxy_ip}) # 实例化ProxyHandler，并指定代理IP及方式。
# opener = urllib.request.build_opener() # 未启用代理
opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler) # 启用代理
opener.addheaders= headers  # opener.addheaders是一个列表，具有以下方法：
                            # append, clear, copy, count, extend, index, insert, pop, remove, reverse, sort
# 可以直接使用open(url)打开，返回Request类；
# 或urllib.request.install_opener(opener)安装到全局，可用urlopen(url)打开
# urlreq = opener.open(url)
urllib.request.install_opener(opener)
urlreq = urllib.request.urlopen(url)

# 法二
'''
# headers使用字典的形式构造
headers={
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Cookie":"BAIDUID=5C20BDC5049CC021CD18422E8C060591:FG=1",
    }
req = urllib.request.Request(url, headers=headers) # 实例化Request类
# Request具有以下方法、属性
# add_header(), remove_header(), has_header(), header_items(),add_unredirected_header() ,set_proxy(), has_proxy(), get_header(), get_full_url(), get_method()
# data, fragment, full_url, headers, host, origin_req_host, selector, type, unredirected_hdrs, unverifiable
# req.add_header('Cookie',"BAIDUID=5C20BDC5049CC021CD18422E8C060591:FG=1") # 添加头信息
ip = "186.148.168.243:8080" # 高匿 return > 186.148.168.243
ip = "118.250.2.157:8060" # 高匿 return > 118.250.2.157
# ip = "220.168.86.37:3128" # 透明 return > 114.249.114.207
# ip = "114.249.114.207:9000" # 透明 return > 114.249.114.207
req.set_proxy(ip,'http')
# proxy = urllib.request.ProxyHandler({})
try:
    urlreq = urllib.request.urlopen(req)
    # '''

    print('*'*30)
    print(urlreq.info())
    print(urlreq.geturl())
    print(urlreq.getcode())
    print('*'*30)
## 提取网页信息
# 1、正则表达式提取
# 2、XPath提取

    data = urlreq.read().decode('utf-8','ignore') # 读取打开的数据流，并使用UTF-8编码
    # 正则表达式
    '''
    data-tools="{title:'Python_百度百科',url:'https://baike.baidu.com/item/Python/407313?fr=aladdin'}">
    data-tools='{"title":"Python 基础教程 | 菜鸟教程","url":"http://www.baidu.com/link?url=nE1dJTZZkufD7u_QMWSeJlzTJdnckkIss6YEyfnejz72i9noq-HLoP4reFdqvv6oV4hijlw3agh1BOna2oavKa"}'>
    '''
    # pattern = '''data-tools=.*?:(?:'|")(.*?)(?:'|"),.*?:(?:'|")(.*?)(?:'|")}'''
    ## 百度搜索
    # pattern = r"data-tools=.*?:(?:\W)(.*?)(?:\W),.*?:(?:\W)(.*?)(?:\W)}"
    # urllist = re.compile(pattern).findall(data)
    ## 必应搜索
    pattern = '<a target="_blank" href="(.*?)h="ID=SERP,.*?">(.*?)</a>'
    urllist = re.compile(pattern).findall(data)

    for url in urllist:
        print("{} : {}".format(url[0], url[1]))
    print('*'*30)
    etree_data = lxml.etree.HTML(data)
    ## 百度IP时用于提取IP
    # res = etree_data.xpath("//div[contains(@class,'op-ip-detail')]//span/text()")
    # print(res)
    # res = etree_data.xpath("//div[contains(@class,'op-ip-detail')]//td/text()")
    # print(res)
    ## 必应IP时用于提取IP
    # res = etree_data.xpath("//div[@class='b_xlText')]/text()")
    res = re.compile(r'<div class="b_xlText">(.*?)</div>').findall(data)
    print(res)

    # XPath
    '''
    <div class="result c-container " id="1" srcid="1599" tpl="se_com_default">
        <h3 class="t c-title-en">
        <a data-click="" href="https://www.baidu.com/link?url=f***1" target="_blank"><em>python</em>官方网站 - Welcome to <em>Python</em>.org</a>
        </h3>
        <div class="f13">
            <div class="c-tools" id="tools_39_1" data-tools="{title:python官方网站 - Welcome to Python.org,url;:;http://www.baidu.com/link?url=fS***8g;}">
            </div>
        </div>
    </div>
    <div class="result-op c-container xpath-log" srcid="1547" id="2" tpl="bk_polysemy">
        <h3 class="t c-gap-bottom-small">
            <a href="https://www.baidu.com/link?url=o4D1***b1" target="_blank"><em>Python</em>_百度百科</a>
            </h3>
        <div class="c-row">       
            <div class="c-span18 c-span-last">
            <p class=" op-bk-polysemy-move"><span class="c-tools" id="tools_1786_2" data-tools="{title:'Python_百度百科',url:'https://baike.baidu.com/item/Python/407313?fr=aladdin'}"></span></p> 
            </div>  
        </div>    
    </div>
    '''
    '''
    etree_data = lxml.etree.HTML(data)
    # print(etree_data)
    # 下面两种匹配字符串效果不会，第一个只能提取文本，第二个只能提取链接
    # xpath_pattern = '//div[@tpl="se_com_default"]/h3[contains(@class,"t")]/a["data-click"]/text()'
    # xpath_pattern = '//div[@tpl="se_com_default"]/h3[contains(@class,"t")]/a["data-click"]/@href'
    # tiqu = etree_data.xpath(xpath_pattern)
    # print(tiqu)

    # 可以同时提取标题及链接
    urllist = etree_data.xpath('//div[contains(@class,"c-container")]//@data-tools')
    for item in urllist:
        item = [s for s in item.split(',')]
        print("{} : {}".format( item[0][10:-1],item[1][7:-2]))
    print('*'*30)
    '''
except Exception as err:
    print('ERROR IS {}'.format(err))


# =================================================================

#  IP代理设置：1、ProxyHandler(); 2、Request.set_proxy(host, type)
# 下面的例子使用ProxyHandler设置代理，并利用ProxyBasicAuthHandler进行授权认证
'''
# proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
# proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
# proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
# opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
# # This time, rather than install the OpenerDirector, we use it directly:
# opener.open('http://www.example.com/login.html')
'''

# import urllib.request,re,random
# #ip="127.0.0.1"
# ip = "186.148.168.243:8080" # 高匿 return > 186.148.168.243
# ip = "118.250.2.157:8060" # 高匿 return > 118.250.2.157
# ip = "220.168.86.37:3128" # 透明 return > 114.249.114.207
# # ip = "114.249.114.207:9000" # 透明 return > 114.249.114.207
# url = "http://icanhazip.com/"
# headers=("user-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36")
# ## 法一
# # proxy = urllib.request.ProxyHandler({'http':ip})
# # opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
# # opener.addheaders = [headers]
# # urllib.request.install_opener(opener)
# ## 法二
# headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
# req = urllib.request.Request(url, headers=headers)
# req.set_proxy(ip,'http')
# try:
#     # data = urllib.request.urlopen(url,timeout=30).read().decode('utf-8','ignore')
#     data = urllib.request.urlopen(req,timeout=30).read().decode('utf-8','ignore')
#     #print(data)
#     # pat = '<table><tr><td>.*?<span class="c-gap-right">(.*?)&nbsp;(.*?)</span>(.*?)\t'
#     # myip = re.compile(pat,re.S).findall(data)
#     print(data)
# except Exception as err:
#     print(err)

