import json
from logger import log
# loaded config



# Read data from file:
try:
    conf = json.load( open( "config.json" ) )
except Exception as e:
    log('Config load failed')
    conf = {
        'apikey':'',
        'user_list':[],
        'proxies' : {
            "https": "http://192.168.0.3:8118"
        },
        'lastupdate_id':0
    }



class Config(object):

    def __init__(self):
        self._config = conf # set it to conf

    def __getattr__(self, name):
        return self.get_property(name)

    def change(self,name,value):
        self._config[name]=value
        self.store_config()

    def _config(self,name,value):
        self._config[name]=value

    def get_property(self, property_name:str):
        log(property_name)
        if property_name not in self._config.keys(): # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]

    def store_config(self):
        json.dump(self._config, open("config.json", 'w'))



config=Config()