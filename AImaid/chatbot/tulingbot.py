import requests

class Tuling():
    def __init__(self):
        self.apikey = '8ab7db6599d543b1915a044045f42d64'
        self.apiurl = 'http://www.tuling123.com/openapi/api'

    def chat(self, msg, userid='febnobiowehjxc'):
        data = {'key':self.apikey, 'userid':userid}
        data['info'] = msg
        try:
            res = requests.post(self.apiurl, data=data, timeout=20)
        except Exception as e:
            print(e)
            return 'unknown error 1'
        else:
            try:
                response = res.json()
                code = res.json()['code']
                text = res.json()['text']
            except Exception as e:
                print(e)
                return 'unknown error 2'
            else:
                if code == 100000:
                    return text
                else:
                    return '不告诉你哟，这是淑女的秘密'


        
