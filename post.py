# -*- coding: utf8 -*-
import os, sys
import requests
import json,base64

#print(sys.argv,len(sys.argv))
if len(sys.argv) < 2:
	print('入力エラー')
	print('{} [tag] message'.format(sys.argv[0]))
	sys.exit(1)

post_token_b64 = os.getenv('NODE_POST')
try:
	post_token = json.loads(base64.b64decode(post_token_b64).decode('utf8'))
	#print(post_token)
	post_url = post_token['url']
	post_wtoken = post_token['token']
	#print(post_url,post_wtoken)
except Exception as e:
	if not post_token_b64:
		print('環境変数「NODE_POST」にAPPトークンを設定してください')
	else:
		print('トークンエラー ({})'.format(e))
	sys.exit(1)

post_tag = os.getenv('NODE_POST_TAG')
msg = sys.argv[1]
if sys.argv[1] != sys.argv[-1]:
	msg = sys.argv[-1]
	post_tag = sys.argv[1]

secret_key_b64 = os.getenv('NODE_POST_SECRET')
if secret_key_b64:
	try:
		secret_key = base64.b64decode(secret_key_b64).decode('utf8')
	except Exception as e:
		print('シークレットKeyエラー ({})'.format(e))
		sys.exit(1)

	from Crypto.Cipher import AES
	from Crypto import Random
	BS = AES.block_size
	_pad = lambda s : s + (BS - len(s.encode('utf8')) % BS) * chr(BS - len(s.encode('utf8')) % BS)
	secret_b = secret_key.encode('utf8')
	iv_b = Random.new().read(BS)
	aes = AES.new(secret_b, mode=AES.MODE_CBC, IV=iv_b)
	msg = base64.b64encode(aes.encrypt(_pad(msg))).decode('utf8')
	iv = base64.b64encode(iv_b).decode('utf8')
	#print(secret_key,msg,iv)
else:
	iv = '';

post_data = {
	'wtoken': post_wtoken,
	'tag': post_tag,
	'msg': msg,
	'iv': iv
}
#print(post_data)

try:
	r = requests.post(post_url, data=post_data)
	#print(r.status_code)
	print(r.text)
except Exception as e:
	print('通信エラー')
	print('except: {}'.format(e))
