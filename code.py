# -*- coding: utf-8 -*-
# author:memoryza(jincai.wang@foxmail.com)
import os
from pyquery import PyQuery as pq
from lxml import etree
import sys
import urllib
import urllib2
import json
import os
import cookielib
import time
# url = 'http://airportcode.911cha.com/'
url = 'http://airportcode.jyc.la/'
host_url = 'http://local.ituxing.com/airLineCode/insertCode'

def sendData(args, fo):
	try:
		data = urllib.urlencode(args)
		req = urllib2.Request(host_url, data)
		response = urllib2.urlopen(req)
		r_data = response.read()
		json_data = json.loads(r_data)
		print json_data
		if json_data['errcode']:
			print 'inset to mysql error:' + args
	except Exception,e:
		fo.write(data)

def getInfo(opener, fo):
	for i in range(51, 426):
		temp_url = url + 'list_' + str(i) +'.html'
		p = opener.open(temp_url)
		if p.getcode() != 200:
			fo.write('error_url:' + temp_url)
		   	continue;  
		html = p.read()
		al = pq(html)
		#这里应该改造成一个list，一次扔一页的数据
		post_args = {}
 		for j in al('#jichang').find('tr'):
 			td_list = al(j).find('td')
 	 		if td_list: 	 
 	 			post_args = {
	 				'city': al(td_list.eq(0)).html(),
	 				'code': al(td_list.eq(1)).html(),
	 				'fourcode': al(td_list.eq(2)).html(),
	 				'airportname': al(td_list.eq(3)).html(),
	 				'enname': al(td_list.eq(4)).html()
	 			}
	 		if post_args:
	 			sendData(post_args, fo)
	 	time.sleep(1)
	print 'collect compelete'
	fo.close()
def main():
	reload(sys)
	sys.setdefaultencoding('UTF-8')	
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	fo = open('D:/wnmp/apache/htdocs/trip/protected/log/python_error.log', 'w+')
	getInfo(opener, fo)

main()
