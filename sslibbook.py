import urllib.request as request
import urllib.parse as parse
import re,json,os,img2pdf, PyPDF2

class ssBook(object):
	"""
	ssBook 用于下载超星汇雅图书的类；
	参数：bookurl -- 图书详情页而地址，
	方法：
		getInfo():获取图书的名称，作者等信息，以及图书的在线阅读地址（可用于下载）
		getPages():获取图书的各页的下载地址（对于扫描图书与PDF图书有所不同）
		download():下载图书的每一页
		onekey():下载正本图书
	静态方法：
		openurl():打开网页，返回网页数据
		merge_pdf():合并PDF文件
		merge_img():转换、合并图片到PDF
	"""
	def __init__(self, bookurl):
		super(ssBook, self).__init__()
		self.bookurl = bookurl
		self.booktype = None
		self.bookinfo = self.getInfo()

	def getInfo(self):
		"""
		提取图书的信息，包含标题、作者、正文页数、出版时间、出版社、中图分类号、简介，在线阅读地址；
		返回包含图书信息的字典。
		"""
		# img page
		dat = self.openurl(self.bookurl)
		info = {}
		title = re.compile('<h2 class="zli_i_h2" title=.*>(.*)</h2>').findall(dat)[0]
		info['标题']=title
		tmp = re.compile('<p><em class="zli_i_field">(.*)</em>(.*)</p>').findall(dat)
		for i,j in tmp:
			info[i] = j
		readurl = re.compile('<span class="zli_i_web"><a href="(.*)" target="_blank">').findall(dat)[0]
		info['readurl'] = readurl
		content = re.compile('<div class="zco_content">\s*(.*)\s*</div>').findall(dat)[0]
		info['content'] = content
		return info

	def getPages(self):
		"""
		提取构建图书各页的地址，以及图书类型（扫描图书-img、PDF图书-pdf）
		返回 图书各页的”根目录“、图书各页的名称（保存名称）
		"""
		fpath = self.bookinfo.get("readurl")
		readurl = parse.urljoin(self.bookurl,fpath)
		dat = self.openurl(readurl)
		if fpath.split("/")[2]=='jpath':
			self.booktype = 'img'
			# 扫描（图片）书籍
			# /n/60cd2714d67b3d150988ff2cd3757302MC271538866611/img1/4A0592CDC7931964E27F189D239EB66DB3D7D8793FF4193B119E44D34A5D3A53930C4936A659FFD6B1C66DF17FCB15664093A85827F0B04586B093F92E64F856881120D359240BF9DA4E70CF7EB8EE7DAF2703688583E42B62A0030D907F927EE4BB65694074E7CDA6ABE1D815873745172A/nf1/qw/96212832/50ADAB89596144C59A4B63C0B4E1E78D/000003?zoom=0
			pages = re.compile('pages = (.*);').findall(dat)[0]
			pages = json.loads(pages)
			# [[1, 0], [1, 1], [1, 0], [1, 13], [1, 9], [1, 523], [1, 0], [2, 2]]
			jpgPath = re.compile('jpgPath: "(.*)"').findall(dat)[0]
			# /n/d0dc469f...381053566/img1/DD40...DE/nf1/qw/14538123/B8485..035DE08/
			pagestype = ['cov','bok','leg','fow','!'  ,'' ,'att','cov']
			# pagestype = ['封面','书名','版权','前言','目录','正文','附录','封底']
			urlroot = 'http://img.sslibrary.com'
			urlPath = parse.urljoin(urlroot,jpgPath)
			# zoom = 0 # [-2,-1,0,1,2]
			pNames = []
			for i,tp in enumerate(pagestype):
				if tp == 'cov':
					if pages[i][1] == 2:
						pNames.append("cov{0:03d}".format(2))
				else:
					for j in range(pages[i][1]):
						pNames.append(tp+"{0:0{1}}".format(j+1,6-len(tp)))
		elif fpath.split("/")[2] == 'pdf':
			self.booktype = 'pdf'
			# PDF书籍
			# https://pdfssj.sslibrary.com/download/getFile?fileMark=96191716&userMark=&pages=239&time=1595400414672&enc=93f10723f5b7cfdaf8e0cb508648f435&code=0e3207db29ec97a97e4724ac06206dcf&cpage=238
			fileMark = re.compile('fileMark = "(.*)";').findall(dat)[0]
			userMark = re.compile('userMark = "(.*)";').findall(dat)[0]
			total = re.compile('total = (.*);').findall(dat)[0]
			durl = re.compile("DEFAULT_BASE_DOWNLOAD_URL = '(.*)';").findall(dat)[0]
			urlPath = durl.replace("' + fileMark + '",fileMark)
			urlPath = urlPath.replace("' + userMark + '",userMark)
			pNames = ["{0:06d}".format(i) for i in range(1,int(total))]

		else:
			# 没有找到扫描书籍与PDF书籍的判断依据，程序可能过时
			raise Exception("文件路径中没有找到'jpath'或'pdf',请检查程序是否过时")
		self.pNames= pNames 
		self.urlPath = urlPath
		return [urlPath,pNames]
	
	def download(self,savePath,zoom=0):
		'''
		下载图书各页
		savePath：保存路径
		zoom：图书清晰度 [-2,-1,0,1,2],仅对扫描图书有效。
		'''
		if self.booktype==None:
			print("Nothing download! please use `getPages` to get download path.")
		else:
			# 检查路径
			if not os.path.exists(savePath):
				os.mkdir(savePath)
			urlPath = self.urlPath
			pNames = self.pNames
			if self.booktype == 'img':
				for i,th in enumerate(pNames):
					durl = parse.urljoin(urlPath,th)+'?zoom={}'.format(zoom)
					# print(durl)
					fname = os.path.join(savePath,th+'.jpg')
					print("Downloading...{}".format(fname))
					request.urlretrieve(durl,fname)
			elif self.booktype == 'pdf':
				for i,th in enumerate(pNames):
					durl = urlPath + '&cpage={}'.format(i+1)
					# print(durl)
					fname = os.path.join(savePath,th+'.pdf')
					print("Downloading...{}".format(fname))
					request.urlretrieve(durl,fname)

	def onekey(self,outfile):
		"""
		下载整本图书
		outfile: 图书保存名称
		"""
		tmp = '.tmp'
		print('get pages...')
		self.getPages()
		print('download pages...')
		self.download(tmp)
		print('mergering...')
		if self.booktype == 'img':
			ssBook.merge_img(tmp,outfile)
		elif self.booktype == 'pdf':
			ssBook.merge_pdf(tmp,outfile)
		for i in os.listdir(tmp):
			os.remove(os.path.join(tmp,i))
		os.removedirs(tmp)
		print('Ok!')

	@staticmethod
	def openurl(url,header=None):
		"""
		打开网页。
		参数：
			url: 网页地址
			header: 头信息
		返回：
			网页内容文本数据
		"""
		if header is None:
			header = {
				"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
				"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
				}
		req = request.Request(url=url,headers=header)
		res = request.urlopen(req)
		dat = res.read().decode('utf-8','ignore')
		return dat

	@staticmethod
	def merge_pdf(fpath,outfile):
		"""
		将目录内的PDF文件合并为一个
		参数：
			fpath：要合并的PDF所在目录
			outfile：输出PDF文件地址
		"""
		if not outfile.endswith(".pdf"):
			outfile = outfile+'.pdf'
		pdf = PyPDF2.PdfFileMerger()
		print('mergering...')
		for i in os.listdir(fpath):
			if i.endswith(".pdf") and i != outfile:
				pdf.append(os.path.join(fpath,i))
		with open(os.path.join(outfile),'wb') as f:
			pdf.write(f)
		pdf.close()
		print('Ok!')

	@staticmethod
	def merge_img(fpath,outfile,img_type='jpg'):
		"""
		将目录内的图片转为PDF并合并为一个PDF文件
		参数：
			fpath：要转换合并的图片文件所在目录
			outfile：输出PDF文件地址
		"""
		if not outfile.endswith(".pdf"):
			outfile = outfile+'.pdf'
		with open(outfile,'wb') as f:
			img_list = []
			print('mergering...')
			for i in os.listdir(fpath):
				if i.endswith(img_type):
					img_list.append(os.path.join(fpath,i))
			f.write(img2pdf.convert(img_list))
		print('Ok!')
	


if __name__ == '__main__':
	# # 测试图片
	# bookurl = "http://sslibbook1.sslibrary.com/book/card?cnFenlei=J205.2&ssid=12335701&d=9fcfe044d610994e1312fe7ca3bc2d3f&isFromBW=false&isjgptjs=false"
	# book=ssBook(bookurl)
	# print(book.bookinfo)
	# fpath,pnames = book.getPages()
	# book.download('./img1')
	# print(fpath)
	# ## 测试PDF
	# bookurl = "http://sslibbook1.sslibrary.com/book/card?cnFenlei=J221&ssid=96085635&d=d41921cafcb72d2e806d41e0d418178e&isFromBW=true&isjgptjs=false"
	# book=ssBook(bookurl)
	# print(book.bookinfo)
	# fpath,pnames = book.getPages()
	# book.download('./pdf1')
	# print(fpath)
	b1=ssBook('http://sslibbook1.sslibrary.com/book/card?cnFenlei=J2&ssid=11090258&d=36e735fb0bce82159b1344d773736ef4&isFromBW=false&isjgptjs=false')
	b1.onekey('wv.pdf')
	# b1.getPages()
	# for i in b1.pNames:
	# 	print(i)
	print('*'*10)
	b2=ssBook('http://sslibbook1.sslibrary.com/book/card?cnFenlei=E92-49&ssid=13681974&d=07661cc5064d5fde654e49a2cec8ccc7&isFromBW=true&isjgptjs=false')
	b2.onekey('ludi.pdf')
	print('all')