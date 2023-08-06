import requests
import json

class Alapchari:
    def __init__(self) -> None:
        self.count=0
        self.url="http://chatrik.org/chatrik"
        self.method="POST"
    
    def ask(self,prompt:str) -> str:
        resp = requests.request(self.method,self.url,headers={
            "Content-Type":"application/json"
        },
        data= json.dumps({
            "prompt":prompt
        }))

        if resp.status_code == 200:
            self.count+=1
            return resp.json()['result']
        else:
            raise Exception(f"{self.url} responded with HTTP Code {resp.status_code}")
