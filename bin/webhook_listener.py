import requests, json
url = 'http://127.0.0.1:5000/webhook'
while True:
    r = requests.get(url)
    with open('../usr/request.json','w') as req_son:
        json.dump(req_son, r.content).encode('utf-8')