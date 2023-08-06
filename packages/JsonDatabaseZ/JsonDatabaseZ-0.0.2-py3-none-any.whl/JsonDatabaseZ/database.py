import os
import json

class JsonDatabase(object):
    def __init__(self, path: str='new_db'):
        self.path = f'{path}.jdb'
        self.items = {}
        
    def check_exist(self):
        exist = os.path.isfile(str(self.path))
        if not exist:
            db = open(self.path, 'w')
            db.write('')
            db.close()
            
    def save(self):
        dbfile = open(self.path, 'w')
        aux = 0
        
        for user in self.items:
            separator = ''
            if aux<len(self.items):
                separator = '\n'
            dbfile.write(user+'='+str(self.items[user])+separator)
            aux+=1
            
        dbfile.close()
            
    def create_user(self,name:str, data:dict):
        self.items[name] = data
    
    def create_admin(self, name:str, data:dict):
        self.items[name] = data
        
    def delete(self, name:str):
        try:
            del self.items[name]
        except Exception as ex:
            print("ERROR: "+str(ex))
            
    def get_user(self, name: str=None):
        try:
            return self.items[name]
        except:
            return None
        
    def is_admin(self, name:str, value_admin: str=None) ->bool:
        user = self.get_user(name)
        if user:
            if user[value_admin]=='true':
                return True
        return False
    
    def load(self):
        dbfile = open(self.path, 'r')
        lines = dbfile.read().split('\n')
        
        for li in lines:
            if li=='':continue
            tokens = li.split('=')
            user = tokens[0]
            data = json.loads(tokens[1].replace("'", '"'))
            self.items = data
        
        

    
