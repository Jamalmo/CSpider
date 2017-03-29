#coding:utf-8

import re
import IPy
import queue
import requests
import argparse
import threading
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 配置
Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class CSpider:
	def __init__(self,target,threads,timeout):
		self.target  = target
		self.threads = threads
		self.timeout = timeout
		self.queue   = queue.Queue()
		self.semaphore = threading.Semaphore(self.threads) # 限制线程数量 - 并发数
		
		self.load_ip() # 加载ip

	# 添加ip地址至queue
	def load_ip(self):
		ips = IPy.IP(self.target)	
		for ip in ips:
			ip = str(ip)
			ip_d = re.match(r'((\d{1,3}\.){3,})(\d{1,3})',ip).group(3) # 删除c段中的0和255
			if ip_d == '255' or ip_d == '0':
				continue;
			self.queue.put(ip)

	# 爬取信息
	def scan(self):
		ip = self.queue.get()
		try:
			url = 'http://'+ip+'/'
			req = requests.get(url,headers=Headers,timeout=self.timeout,verify=False)
			content = req.content.decode()
			soup = BeautifulSoup(content, "lxml")
			size = len(content)
			code = req.status_code
			try:
				title = soup.title.string
			except:
				title = ''

			title = title.strip().strip('\r').strip('\n')[:40]
			print("%-20s %-6d %-10s %-50s" % (ip,code,size,title))
		except:
			pass

		self.semaphore.release() # 解锁线程

		try:
			url = 'https://'+ip+'/'
			req = requests.get(url,headers=Headers,timeout=self.timeout,verify=False)
			content = req.content.decode()
			soup = BeautifulSoup(content, "lxml")
			size = len(content)
			code = req.status_code
			try:
				title = soup.title.string
			except:
				title = ''

			title = title.strip().strip('\r').strip('\n')[:40]
			print("%-20s %-6d %-10s %-50s" % (ip+':443',code,size,title))
		except:
			pass

		self.semaphore.release() # 解锁线程

	# 启动线程
	def run(self):
		print("开始扫描,发生错误不会打印...")
		print("%-24s %-6s %-10s %-50s" % ("IP","状态","返回大小","标题"))
		while not self.queue.empty():
			if self.semaphore.acquire():
				t = threading.Thread(target=self.scan)
				t.start()

if __name__ == '__main__':

	# 处理参数
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('target',help='Set Target IP or IP section.')
	parser.add_argument('-t',type=int,default=50,dest='threads',help="thread num.")
	parser.add_argument('-o',type=int,default=8,dest='timeout',help="timeout.")
	args = parser.parse_args()

	target  = args.target
	threads = args.threads
	timeout = args.timeout

	cspider = CSpider(target,threads,timeout)
	cspider.run()
