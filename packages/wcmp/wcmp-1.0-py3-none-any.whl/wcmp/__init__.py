from urllib.request import urlopen
from urllib.parse import urlencode
name = "wcmp"

class wcmp(object):
    def __init__(self,token,base_url='http://www.pushplus.plus/send') -> None:
        self.token=token
        self.base_url=base_url
        
    def send(self,content,title=None):
        if not isinstance(content,str):
            raise 'The message content must be string!'
        md={'token':self.token,'content':content}
        if title:
            if not isinstance(title,str):
                raise 'The message title must be string!'
            md['title']=title
        send_url=self.base_url+'?'+urlencode(md)
        urlopen(send_url)


if __name__=="__main__":
    s=wcmp('50a1bcd158c7410dadad532249e02ac0')
    s.send('messgaedf')