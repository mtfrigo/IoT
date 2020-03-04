import requests 

class Http(object):

    def sendRequest(self, ip, port, api, data):

        URL = "http://"+str(ip)+":"+str(port)+"/"+str(api)

        r = requests.post(url = URL, data = data) 

        # extracting response text  
        pastebin_url = r.text 
        print("The pastebin URL is:%s"%pastebin_url) 