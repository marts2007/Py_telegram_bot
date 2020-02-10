import json
from logger import log
import http_fetcher as ht
from config import config



class Telegram:
    def do_tel_query(self,action: str='getMe',params: dict = {}):
        print(action)
        response = (ht.get_url('https://api.telegram.org/bot'+config.apikey+'/'+action,params))
        return response

    def __init__(self) -> None:
        response=self.do_tel_query('getMe')
        if type(response) == dict:
            if 'ok' in response:
                if response['ok']:
                    self.status=True
                    log('Connection succeeded')
                    return
        self.status=False
        return

    def get_updates(self):
        response=self.do_tel_query('getUpdates',{'offset': int(config.lastupdate_id+1),'limit':1})
        if type(response) == dict:
            if 'ok' in response:
                if 'result' in response:
                    if len(response['result'])>0:
                        config.change('lastupdate_id',response['result'][0]['update_id'])
                        print(response)
                        self.parse_message(response['result'][0]['message'])

        return  response

    def parse_message(self,msg: dict = {}):
        if msg['text'].find('/subscribe')>-1:
            config.change('subscribers',list(set((config.subscribers if config.subscribers else [])+[msg['chat']['id']])))


t = Telegram()
if t.status:
    print('connected!')
else:
    print('error')

t.get_updates()
