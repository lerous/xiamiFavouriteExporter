# coding=utf-8
# pyinotify

import sys
import time
import logging
import math
import os
from bs4 import BeautifulSoup
import urllib2 

reload(sys)
sys.setdefaultencoding( "utf-8" )

def getContent(url_b):
	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
	req = urllib2.Request(url = url_b ,headers = headers)
	myResponse  = urllib2.urlopen(req).read()
	soup = BeautifulSoup(myResponse, "html.parser")
	createList(soup)

def createList(soup):
	temp_consumer = []
	number = soup.find_all("span", class_="counts")[0].get_text().replace('首', '')
	mob = soup.find_all("td", class_="song_name")
	cra_num = int(math.ceil(float(number)/len(mob)))
	f=open('xiami.kwl','a')
	for key in mob:
		temp_consumer.append(key.get_text())
		f.write('\t<so name="'+ key.a.get_text().replace("&","").replace("<","").replace(">","").replace('"', "").replace("¹", "").replace("¨", "") + '" artist="' + key.find_all("a", class_="artist_name")[0].get_text().replace("&","").replace("<","").replace(">","").replace("    ", "") + '"></so>\n')

def line_prepender(filename, line):
	with open(filename, 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		f.write(line.rstrip('\r\n') + '\n' + content)	

if __name__ == "__main__":
	user_id = input("please input your xiami id:  ")

	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
	req = urllib2.Request(url = 'http://www.xiami.com/space/lib-song/u/'+str(user_id) ,headers = headers)
	myResponse  = urllib2.urlopen(req).read()
	mag = BeautifulSoup(myResponse, "html.parser")
	number = mag.find_all("span", class_="counts")[0].get_text().replace('首', '')
	mob = mag.find_all("td", class_="song_name")
	cra_num = int(math.ceil(float(number)/len(mob)))

	print 'total: '+str(cra_num)
	for i in range(cra_num):
		now_num = i+1
		print 'now downloading the page '+str(now_num)+'/'+str(cra_num)
		getContent('http://www.xiami.com/space/lib-song/u/'+str(user_id)+'/page/'+ str(i+1))
		if i == cra_num-1:
			g = open('xiami.kwl','a')	
			g.write('</so>')
			g.close()
			line_prepender('xiami.kwl', '<so>')

			gbkfile = open('xiami.kwl')
			tstr = gbkfile.read().encode('GBK',"ignore")
			gbkfile.close()
			w_file = open('xiami.kwl', 'w')
			w_file.write(tstr)
			w_file.close()
			print 'compelete!'
