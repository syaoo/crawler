---
title: 网络爬虫
---

## 超星汇雅图书下载(扫描书籍)
网页有下载按钮，但是需要下载超星阅读器，而且下载后只能在阅读器内查看，显然不是我想要的，那么考虑能不能从web端入手。简单分析了一下，发现web端会以图片的形式分页加载书本内容，因此可以用爬虫将这些图片爬下来，然后再合并为一个PDF文件。
### 资源爬取
#### 资源路径分析
查看网页源代码发现书本各页的图片地址并不在这里，所以需要费些事找一下是否有js文件里包含图片地址，或者地址有么有什么规律。研究了一下没有发现有关js文件，但是图片地址有一规律。图片路径由三部分组成：1.网页根目录；2.书籍图片目录；3.图片名；此外还有一个zoom参数可以选择不同清晰度的图片。
```
http://img.sslibrary.com/n/d0dc469fe4f5466f493b51b698bca695MC271381053566/img1/DD40F4EA27915A9DEE69D9A0EF09275657F7C13243DF48BD23C577FB398E6C13BA36DAB954A5B63C24EC18E98E2FC6630A90B009F1A19E6D30CB26B70A72122D9E0ECFFADA760525BDD9E70EFF0BB6111745D90F190DAEE1F61A15B8E3FBF64185249C6A6136457C3819816597A3B1271EDE/nf1/qw/14538123/B84856D658BA4FCEAA917DD97035DE08/00001?/zoom=0
```
下一步就可以构造地址了。
#### 地址构造
网页根目录不变；图片目录可以在网页源码`jpgPath`参数中找到；zoom参数也有-2、-1、0、1、2可选。
关键就是图片名了，正文的图片都是六位数组，但是封面、前言等部分以字符+数字的形式组成，而且不同的书不一定都有，有些麻烦了。幸运的是，在源码中发现了这么一个数组
```javascript
var pages = [[1, 0], [1, 1], [1, 0], [1, 13], [1, 9], [1, 523], [1, 0], [2, 2]];
```
数组第一个元素数页面类型，第二个是页数，下面数页面类型对应关系
```javascript
	var PAGETYPE = {
			cov : 0, /* 封面 */
			bok : 1, /* 书名 */
			leg : 2, /* 版权 */
			fow : 3, /* 前言 */
			dir : 4, /* 目录 */
			cnt : 5, /* 正文 */
			att : 6, /* 附录 */
			bac : 7  /* 封底 */
		};
		
	var PAGETYPEINFO = [
			{v:PAGETYPE.cov, s:'cov', n:'封面'}, /* 封面cov001 */
			{v:PAGETYPE.bok, s:'bok', n:'书名'}, /* 书名 */
			{v:PAGETYPE.leg, s:'leg', n:'版权'}, /* 版权 */
			{v:PAGETYPE.fow, s:'fow', n:'前言'}, /* 前言 */
			{v:PAGETYPE.dir, s:'!'  , n:'目录'}, /* 目录 */
			{v:PAGETYPE.cnt, s:''   , n:'正文'}, /* 正文 */
			{v:PAGETYPE.att, s:'att', n:'附录'}, /* 附录 */
			//{v:PAGETYPE.bac, s:'bac', n:'封底'}  /* 封底 */
			{v:PAGETYPE.bac, s:'cov', n:'封底'}  /* 封底cov002 */
	];
```
这样地址构造的代码就可以写出来了
```python
pagestype = ['cov','bok','leg','fow','!'  ,'' ,'att','cov']
urlroot = 'http://img.sslibrary.com'
zoom = 0 # [-2,-1,0,1,2]
i = 0
for ptype,nums in pages:
	if ptype ==1 and nums != 0:
		for j in range(nums):
			thisjpg = urlroot+jpgPath+pagestype[i]+"{0:03d}".format(j+1)
			downloadjpg(thisjpg, zoom=0) # 下载图片
	elif ptype == 2 and nums !=0:
		# 封底也编号为cov002
		thisjpg = urlroot+jpgPath+pagestype[i]+"{0:03d}".format(2)
	i+=1
```
### 图片整合 
img2pdf https://pypi.org/project/img2pdf/#description

## 超星汇雅图书下载
### pdf链接
pdf是分页加载的，从下面代码可以找到每页pdf的链接
```
    var fileMark = "13456618";
    var userMark = "";
    var fileName = "水下热滑翔机推进";
    var cpage = "1";
    var readlogurl = "";
    var enc = "604df28d0776b83d84db028ea8f4d2f1";
    var readerType = 1;
    var total = 379;
    cpage = cpage > total ? total : cpage;
    var DEFAULT_CURRENT_PAGE =
    0||
    cpage;
    var DEFAULT_BASE_DOWNLOAD_URL = 'https://pdfssj.sslibrary.com/download/getFile?fileMark=' + fileMark + '&userMark=' + userMark + '&pages=379&time=1595293891054&enc=604df28d0776b83d84db028ea8f4d2f1&code=519920e5e26e9c90fd31aed038c4745c';
    var DEFAULT_URL = DEFAULT_BASE_DOWNLOAD_URL + "&cpage=" + DEFAULT_CURRENT_PAGE;
    var index_page = DEFAULT_CURRENT_PAGE;
```
提取出需要的变量`fileMark`,`userMark`,`total`

### 合并pdf
使用pyPDF2库合并
http://mstamy2.github.io/PyPDF2/

## Bilibili

