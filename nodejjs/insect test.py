import requests
import os
#import bs4 from BeautifulSoup as bs
url="http://127.0.0.1:3000/b"
res=requests.get(url)
print(res.text)
