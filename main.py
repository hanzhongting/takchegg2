import json
import requests
import time
import pymongo
import http.client
from bs4 import BeautifulSoup as s
from datetime import datetime, timedelta
import telebot
import secrets
import uuid

client = pymongo.MongoClient("mongodb+srv://aa:bb@cluster0.w0cxy.mongodb.net/?retryWrites=true&w=majority")
mydb= client["a"]

mycol = mydb["save"]

TOKEN = "5034898394:AAGLhzqYHtqAjXieppMmNslri09pdgWnDgs"




headers = {
  'authority': 'auth.chegg.com',
  'accept': 'application/vnd.chegg-odin.v1+json',
}

def timeans(uuid):
    print("time uuid")
    headers = {'accept': 'application/vnd.chegg-odin.v1+json'}
    text=uuid
    r = requests.request("GET", str("https://proxy.chegg.com/v1/question/"+text),headers=headers)
    print(r.json())
    e = r.json()['result']['createdDate']
    i = datetime.strptime(e, '%Y-%m-%dT%H:%M:%SZ')
    e2=r.json()['result']['lastUpdatedDate']
    i2=datetime.strptime(e2, '%Y-%m-%dT%H:%M:%SZ')
    z = (i2 - i)
    print(z)
    return str(z)

def send_msg(text,chatidd):
   token = "your_token"
   chat_id = str(chatidd)
   url_req = "https://api.telegram.org/bot" + TOKEN + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text +"&parse_mode=Markdown"+"&disable_web_page_preview=True"
   results = requests.get(url_req)
   print(results.json())

#chuk url
def send_url(text):
    try:
        print(text)
        payload = json.dumps({
  "variables": {
    "questionUuid": str(text)
  },
  "operationName": "getQuestionByUuid"
})
        headers = {'Content-Type': 'application/json',
  'Authorization': 'Basic MFQxOE5HYmFsUURGYzBnWkh6b3ZwZVJkN0E1Y3BMQ3g6dnRnamFZa3Ric2p4OUFPUg==',
  'X-CHEGG-DEVICEID':  secrets.token_hex(8),
  'X-CHEGG-SESSIONID': str(uuid.uuid4()),
  'Host': 'proxy.chegg.com',
  'User-Agent': 'CheggApp/4.6.0 (com.chegg.mobile.consumer; build:4.6.0.0; iOS 14.8.1) Alamofire/5.2.2',
  'x-chegg-auth-mfa-supported': 'true'

}
        response = requests.request("POST", "https://proxy.chegg.com/mobile-study-bff/graphql", headers=headers  , data=payload)
        print(response.json())
        #print(response.json())
        if response.status_code == 500:
            print("oh is out")
            return "is out"
        elif response.json()['data']['getQuestionByUuid']['questionState'] =='AnsweredAndUnrated':
            print("is solve")
            return "is solve"
        elif response.json()['data']['getQuestionByUuid']['questionState']=='NeedMoreInfo':
            print ("need inf")
            return "need inf"
        else:
            return "is not slove"
    except:
        pass




def mem():
    while True:
        try:
            time.sleep(5)
            num=mycol.count()

            print(num)
            if num >0:


                j=[]
                mydoc2 = mycol.find()



                for x in mydoc2:

                    g=[x]
                    j.append(g)



                for ch in j:
                    #print(j)
                    time.sleep(2)
                    url = str(ch[0]['url'])

                    d=send_url(url)

                    print(d)
                    if d==None:
                       print("nan")
                       myquery = { "url": str(ch[0]['url']) }
                       dele=mycol.delete_one(myquery)
                       print(dele)

                    if "no slove" in d:
                        print(" not solve yet")
                    elif "is out" in d:

                        mention = "[" + str(ch[0]['name']) + "](tg://user?id=" + (str(ch[0]['id'])) + ")"
                        #texty=mention +"\nsolved :\nLink : "+ch[0]['url']
                        chatidd=str(ch[0]['chatidusr'])
                        s=send_msg( mention +"\n.it looks like your question has been deleted \nyour Link :\n"+ch[0]['cheggurl'],chatidd)
                        myquery = { "url": str(ch[0]['url']) }
                        dele=mycol.delete_one(myquery)
                        print(dele)
                        print("is good")
                    elif "is solve" in d:
                        print("is solved")
                        mention = "[" + str(ch[0]['name']) + "](tg://user?id=" + (str(ch[0]['id'])) + ")"
                        #texty=mention +"\nsolved :\nLink : "+ch[0]['url']
                        chatidd=str(ch[0]['chatidusr'])
                        uuid=str(ch[0]['url'])

                        s=send_msg( mention +"\nyour question Has Been solved on chegg \nnyour Link :\n"+ch[0]['cheggurl']+"\n\n"+"",chatidd)
                        myquery = { "url": str(ch[0]['url']) }
                        dele=mycol.delete_one(myquery)
                        print(dele)
                        print("is good")
                    elif "need inf" in d :
                        mention = "[" + str(ch[0]['name']) + "](tg://user?id=" + (str(ch[0]['id'])) + ")"
                        #texty=mention +"\nsolved :\nLink : "+ch[0]['url']
                        chatidd=str(ch[0]['chatidusr'])
                        s=send_msg( mention +"\nHello..Your question needs more information to be resolved\nyour Link : "+ch[0]['cheggurl'],chatidd)
                        myquery = { "url": str(ch[0]['url']) }
                        dele=mycol.delete_one(myquery)
                        print(dele)
                        print("is need informathen")


        except:
            pass

mem()
