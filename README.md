# ClassifyTwitterImages
Twitterで流れてくる画像をディープラーニングで分類します

#概要
1.Twitter Streaming APIで日本語＆画像付きツイートをMongoDBに保存（saveimages.py）  
2.CNN（畳み込みニューラルネットワーク）のモデルを使って分類しつつディレクトリに保存（api.py,classify.py）  
3.それぞれ分類した画像をFlaskを使って表示（display.py）
