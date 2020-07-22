#爬取CSDN
'''
import urllib.request,re
url="http://blog.csdn.net"
headers=("user-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
#安装为全局
urllib.request.install_opener(opener)
data=urllib.request.urlopen(url).read().decode('utf-8','ignore')
pat = '<a href="(.*?)" target="_blank">'
alllink = re.compile(pat).findall(data)
print(alllink)
for lin in alllink:
  pass
  #urllib.request.urlretrieve(lin,filename=localpath) #将网页下载到本地
'''
# 糗百
import urllib.request,re
url = "
headers=("user-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36")
