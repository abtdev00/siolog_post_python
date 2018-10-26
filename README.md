sio log ServerにメッセージをpostするためのPythonクライアント  
  
(必要モジュール)  
requests  
pycrypto  
  
(使い方)  
・sio log Serverにログインし、設定ページでAPPトークンとシークレットKeyを確認  
・環境変数「NODE_POST」にAPPトークン、「NODE_POST_SECRET」にシークレットKeyを設定  
・「python post.py [tag] メッセージ」で、メッセージをサーバへ送信  
