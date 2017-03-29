#coding:utf-8

import re
import IPy
import queue
import requests
import argparse
import threading
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Config
Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
# Close https error
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ports = ['21','80','81','82','88','90','443','8000','8001','8080','8081','8082','8443','8843','3306']

class CSpider:
	def __init__(self,target,threads,timeout):
		self.target  = target
		self.threads = threads
		self.timeout = timeout
		self.queue   = queue.Queue()
		self.semaphore = threading.Semaphore(self.threads) # Thread cound
		
		self.load_ip() # Load ip

	# Add ip on queue
	def load_ip(self):
		ips = IPy.IP(self.target)	
		for ip in ips:
			ip = str(ip)
			ip_d = re.match(r'((\d{1,3}\.){3,})(\d{1,3})',ip).group(3) # Delete a.b.c.0 & a.b.c.255
			if ip_d == '255' or ip_d == '0':
				continue;
			self.queue.put(ip)

	# Get Infomation
	def scan(self):
		ip = self.queue.get()
		for p in ports:
			try:
				url = 'http://'+ip+':%s/' % p
				req = requests.get(url,headers=Headers,timeout=self.timeout,verify=False)
				content = req.content.decode()
				soup = BeautifulSoup(content, "html.parser")
				size = len(content)
				code = req.status_code
				try:
					title = soup.title.string
				except:
					title = ''

				title = title.strip().strip('\r').strip('\n')[:55]
				print("%-20s %-6d %-10s %-50s" % (ip+':%s'%p,code,size,title))
			except:
				pass

		self.semaphore.release() # Unlock thread

	# Start thread
	def run(self):
		print("Start scan... No print error info.")
		print("%-20s %-6s %-10s %-50s" % ("IP","Status","Size","Title"))
		while not self.queue.empty():
			if self.semaphore.acquire():
				t = threading.Thread(target=self.scan)
				t.start()

if __name__ == '__main__':

	# Argument parser
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('target',help='Set Target IP or IP section.')
	parser.add_argument('-t',type=int,default=50,dest='threads',help="thread num.")
	parser.add_argument('-o',type=int,default=3,dest='timeout',help="timeout.")
	args = parser.parse_args()

	target  = args.target
	threads = args.threads
	timeout = args.timeout

	cspider = CSpider(target,threads,timeout)
	cspider.run()
