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
	f=open('xiami.kgl','a')
	for key in mob:
		temp_consumer.append(key.get_text())
		f.write('\t<File>\n\t\t<MediaFileType>0</MediaFileType>\n\t\t<FileName>'+ key.get_text().replace("\r","").replace("\n","").replace("\t","").replace("&","").replace("<","").replace(">","").replace("    ", "") + '</FileName>\n\t</File>\n')

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
			g = open('xiami.kgl','a')	
			g.write('</List>')
			g.close()
			line_prepender('xiami.kgl', '<?xml version="1.0" encoding="windows-1252"?>\n<List ListName="虾米音乐">')
			print 'compelete!'
