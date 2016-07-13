# -*- coding: utf-8 -*-
#!/usr/bin/env python2
import json
import os
import tempfile
import pymongo

# pip install flask
from flask import Flask, request, make_response, abort, render_template  


# Flask Settings
DEBUG = True
UPLOAD_FOLDER = "tmp"
MODEL_FOLDER = "model"
SUPPORT_EXTENSIONS = set([".jpg", ".jpeg", ".png"])
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def help():
	print 'test'
	html=""
	category = request.args.get('category')
	#category = request.form['category']
	print 'processing'

	images_list = os.listdir('static/images/'+category)
	print images_list
	# for data in co.find({},{ "_id": 0 }).sort("_id", -1).limit(10):
	# 	#temp_data = json.dumps(data)
	# 	#print type(temp_data)
	# 	tmp_data = data.values()
	# 	html=str(html)+'<a href="https://twitter.com/'+str(tmp_data[2])+'"><img width="100px" src="'+str(tmp_data[0])+'">'+'<BR>'
	print 'finish'
	return render_template('index.html',html=images_list,category=category)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,processes=3)
