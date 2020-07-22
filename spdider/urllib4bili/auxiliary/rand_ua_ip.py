"""
产生随机UA与IP
random_ua(ualist=None, ismobile=False)
random_ip(iplist=None)
random_ua_ip(ualist = None, ismobile=False,iplist=None)
"""
import random
# 随机User_Agent
def random_ua(ualist=None, ismobile=False):
    # 不提供ualist参数时，使用内置UA list，ismobile参数指定是否为移动端，默认False为PC。
    if ualist == None and ~ismobile:
        # PC user_agent
        ualist = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
        # "Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.2)",
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52",
        "Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
       ]
    elif ualist == None and ismobile:
        # Mobile user_agent
        ualist = [
        # android phone
        "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19",
        "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        # windows phone
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; LG; GW910)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; SAMSUNG; SGH-i917)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)"
        # iOS
        "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
        "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3",
        # Firefox on Android Mobile	
        "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0",
        # Firefox on Android Tablet	
        "Mozilla/5.0 (Android; Tablet; rv:14.0) Gecko/14.0 Firefox/14.0",
        ]
    else:
        if len(ualist) < 1:
            raise Exception("Parameter 'ualist' must be a Non-Empty list")
    user_agent = random.choice(ualist)
    return user_agent
# 随机IP
def random_ip(iplist=None):
    if iplist == None:       
        iplist = [
            "186.148.168.243:8080", # 高匿 return > 186.148.168.243
            "118.250.2.157:8060", # 高匿 return > 118.250.2.157
            "220.168.86.37:3128", # 透明 return > 114.249.114.207
            "114.249.114.207:9000", # 透明 return > 114.249.114.207
        ]
    else:
        if len(iplist) < 1:
            raise Exception("Parameter 'iplist' must be a Non-Empty list")
    proxy_ip = random.choice(iplist)
    return proxy_ip
# 同时随机User_Agent与IP
def random_ua_ip(ualist = None, ismobile=False,iplist=None):
    user_agent = random_ua(ualist, ismobile)
    proxy_ip = random_ip(iplist)
    return (user_agent, proxy_ip)

if __name__ == "__main__":
    ua = random_ua()
    ip = random_ip()
    print("UA is: {}\n IP is: {}".format(ua, ip))
    print('*'*20)
    (ua,ip) = random_ua_ip()
    print("UA is: {}\n IP is: {}".format(ua, ip))
    ual = [
        "ads"
        ]
    ua = random_ua(ualist=ual)
    print(ua)
    print('*'*20)
    random_ip([])
    print(random_ua(ismobile=True))