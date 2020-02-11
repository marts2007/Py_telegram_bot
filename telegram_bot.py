import json
from logger import log
import http_fetcher as ht
from config import config
import time

#t={1,2,3,4}
#b={1,3,4,5}
#print(list({1,2,3,4}|{1,5}))
#quit()
class Telegram:
    def do_tel_query(self,action: str='getMe',params: dict = {}):
        print(action)
        response = (ht.get_url('https://api.telegram.org/bot'+config.apikey+'/'+action,params))
        return response

    def send_message(self,chat_id,text):
        response = self.do_tel_query('sendMessage',{'chat_id':chat_id,'text':text})
        pass

    def __init__(self) -> None:
        response=self.do_tel_query('getMe')
        if type(response) == dict:
            if 'ok' in response:
                if response['ok']:
                    self.status=True
                    log('Connection succeeded')
                    self.mainloop()
        self.status=False


    def mainloop(self):
        while 1:
            self.get_updates()
            time.sleep(5)
        pass

    def get_updates(self):
        response=self.do_tel_query('getUpdates',{'offset': int(config.lastupdate_id+1)})
        if type(response) == dict:
            if 'ok' in response:
                if 'result' in response:
                    if len(response['result'])>0:
                        for resp in response['result']:
                            config.change('lastupdate_id',resp['update_id'])
                            print(resp)
                            self.parse_message(resp['message'])
        return  response

    def parse_message(self,msg: dict = {}):
        if msg['text'].find('/subscribe')>-1:
            config.change('subscribers',list(set(config.subscribers if config.subscribers else {}) | {msg['chat']['id'],}))
            self.send_message(msg['chat']['id'],'You have been subscribed')
        if msg['text'].find('/unsubscribe') > -1:
            config.change('subscribers',list(set(config.subscribers if config.subscribers else {}) - {msg['chat']['id']}))
            self.send_message(msg['chat']['id'], 'You have been unsubscribed')

t = Telegram()
if t.status:
    print('connected!')
else:
    print('error')


