# -*- coding: utf-8 -*- 

import requests
import urllib
import urllib2
import os.path
import sys
import json
import os
import tempfile
import pymongo
from HTMLParser import HTMLParser
import shutil
import stat

def download(url):
    img = urllib.urlopen(url)
    localfile = open('images/'+os.path.basename(url),'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()
    return os.path.basename(url)

def movingfile(url,movedir):
	try:
		shutil.move('images/'+os.path.basename(url), 'images/'+movedir)
	except:
		print 'ファイルが重複'
	


# mongodb へのアクセスを確立
client = pymongo.MongoClient('localhost', 27017)
# データベースを作成 (名前: my_database)
db = client.my_database2
# コレクションを作成 (名前: my_collection)
co = db.my_collection

passed = 0
for data in co.find({},{ "_id": 0 }):
	tmp_data = data.values()
	try:
		file_path = download(str(tmp_data[0]))
		r = requests.post('http://localhost:5000/classify',{'url':str(file_path)})
		
		#print r.data
		try:
			response = json.loads(r.text)
			#json_data = json.dumps(r.text, ensure_ascii=False)
			#print response.keys()

			#print type (response)
			#json_string = json.loads(response)
			#print type(response)

			#0:sky
			#1:ramen
			#2:fashion
			#3:shiba
			#4:yakiniku
			#5:selfee
			moved_flag=0
			sky_score = round(response['0']["score"][0]*100,1)
			ramen_score = round(response['0']["score"][1]*100,1)
			fashion_score = round(response['0']["score"][2]*100,1)
			shiba_score = round(response['0']["score"][3]*100,1)
			yakiniku_score = round(response['0']["score"][4]*100,1)
			selfee_score = round(response['0']["score"][5]*100,1)
			if sky_score>80:
				movingfile(str(tmp_data[0]),'sky')
				moved_flag = 1
				print 'sky'
			if ramen_score>80:
				movingfile(str(tmp_data[0]),'ramen')
				moved_flag = 1
				print 'ramen'
			if fashion_score>80:
				movingfile(str(tmp_data[0]),'fashion')
				moved_flag = 1
				print 'fashion'
			if shiba_score>80:
				movingfile(str(tmp_data[0]),'shiba')
				moved_flag = 1
				print 'shiba'
			if yakiniku_score>80:
				movingfile(str(tmp_data[0]),'yakiniku')
				moved_flag = 1
				print 'yakiniku'
			if selfee_score>80:
				movingfile(str(tmp_data[0]),'selfee')
				moved_flag = 1
				print 'selfee'
			if moved_flag ==0:
				movingfile(str(tmp_data[0]),'other')
				print 'other'
			passed = passed+1
			print passed
		except:  # includes simplejson.decoder.JSONDecodeError
		    print 'Decoding JSON has failed'
	except :
		pass