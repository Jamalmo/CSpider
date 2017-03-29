# CSpider 

使用HTTP协议的网段主机探测器

使用方法：
`python cspider.py 127.0.0.0/24`

可自定义线程数量：
`python cspider.py 127.0.0.0/24 -t 50 # 默认50`

自定义超时时间：
`python cspider.py 127.0.0.0/24 -t 50 -o 8 #默认为8`

输出格式：</br>
`IP                       状态     返回大小       标题`</br>
`45.77.19.6           200    47370      Ze7ore's Blog | 菜鸡的写字板`</br>
`45.77.19.6:443       200    47448      Ze7ore's Blog | 菜鸡的写字板`</br>
