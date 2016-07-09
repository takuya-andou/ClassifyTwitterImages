#!/usr/local/bin/python
# -*- coding:utf-8 -*-
 
import json, urllib2, oauth2 as oauth
import ConfigParser
import pymongo

# mongodb へのアクセスを確立
client = pymongo.MongoClient('localhost', 27017)

# データベースを作成 (名前: my_database)
db = client.my_database

# コレクションを作成 (名前: my_collection)
co = db.my_collection

inifile = ConfigParser.SafeConfigParser()
inifile.read("./config.ini")


api_key = inifile.get("twitter","api_key")
api_secret = inifile.get("twitter","api_secret")
access_key = inifile.get("twitter","access_token")
access_secret = inifile.get("twitter","access_secret")


consumer = oauth.Consumer(api_key, api_secret)
token = oauth.Token(access_key, access_secret)
 
#エンドポイントURL
#https://dev.twitter.com/docs/api/1.1/get/statuses/sample あたり参照
#trackなどの条件を指定して絞り込むのも好いかも
url = 'https://stream.twitter.com/1.1/statuses/sample.json'
 
request = oauth.Request.from_consumer_and_token(consumer, token, http_url=url)
request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)
res = urllib2.urlopen(request.to_url())


for r in res:
    data = json.loads(r)
 
    try:
        #日本語のツイートだけ表示
        if data['user']['lang'] == 'ja':
            if data['entities']['media'][0] is None:
                pass
            else:
                print data['user']['screen_name']
                print data['text']
                print data['entities']['media'][0]['media_url_https']
                print
		# tweetを保存
		co.insert_one({"name": data['user']['screen_name'],"tweet":data['text'],"imageurl":data['entities']['media'][0]['media_url_https']})
 
    except:
        #たまーにデリートフラグのついたツイートが流れてくるので（？）適当に受け流す 詳しくは未調査
        pass
