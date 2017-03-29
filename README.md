# CSpider
使用HTTP协议的C段主机探测器。

使用方法：
`python cspider.py 127.0.0.0/24`

可自定义线程数量：
`python cspider.py 127.0.0.0/24 -t 50 # 默认50`

自定义超时时间：
`python cspider.py 127.0.0.0/24 -t 50 -o 8 #默认为8`