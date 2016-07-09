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
	shutil.move('images/'+os.path.basename(url), 'images/'+movedir)

# mongodb へのアクセスを確立
client = pymongo.MongoClient('localhost', 27017)
# データベースを作成 (名前: my_database)
db = client.my_database2
# コレクションを作成 (名前: my_collection)
co = db.my_collection


for data in co.find({},{ "_id": 0 }).sort("_id", -1).limit(3):
	tmp_data = data.values()
	file_path = download(str(tmp_data[0]))
	r = requests.post('http://localhost:5000/classify',{'url':str(file_path)})
	print r.text
	
	#movingfile(str(tmp_data[0]),'ramen')