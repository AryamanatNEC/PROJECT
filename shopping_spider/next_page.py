import requests
from bs4 import BeautifulSoup

links = []

def next_page(formatted_query):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "Accept": "text/html"
        }
        
        base_url = f"https://www.google.com/search?q={formatted_query}&tbm=shop&gl=ind"
        print(base_url)
        
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        tab = soup.find("table", {"class": "AaVjTc"})
        
        next_page_links = tab.find_all('a', class_='fl')
        for link in next_page_links:
            link_href = link.get('href')
            if link_href:
                next_page_url = "https://www.google.com" + link_href
                #print(next_page_url)
                links.append(next_page_url)
        print(links)  # To see the collected links outside the function
        with open('next_page_links.txt', 'w') as f:
                    for link in links:
                        f.write(link + '\n')        
                
                
    except Exception as e:
        print(e)

#next_page('f1')
'''
print(links)  # To see the collected links outside the function
with open('next_page_links.txt', 'w') as f:
                    for link in links:
                        f.write(link + '\n')
'''                        

