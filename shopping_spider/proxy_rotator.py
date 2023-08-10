from bs4 import BeautifulSoup
import requests
import random
proxies = []

def LoadUpProxies():
    url = 'https://sslproxies.org/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
    }
    response = requests.get(url, headers=header)
    
    soup = BeautifulSoup(response.content, 'lxml')
    tab = soup.find("table", {"class": "table table-striped table-bordered"})
    
    for row in tab.select('tbody tr'):
        try:
            ip = row.select('td')[0].get_text()
            port = row.select('td')[1].get_text()
            proxies.append({'ip': ip, 'port': port})
        except IndexError:
            pass
'''
LoadUpProxies()
print(proxies)
if proxies:
    random_proxy = random.choice(proxies)
    print("Random Proxy:", random_proxy)
else:
    print("No proxies available.")
    '''