from .google_spider import LoadUpProxies,extract_number_from_string
import random
from bs4 import BeautifulSoup
import requests
import csv
import json
proxies = []
'''
def append_next_pages():
    with open('next_page_links.txt','r') as f:
        lines=f.readlines()
    print(lines)
    for line in lines:
        append_shopping_data(line)
'''

def append_shopping_data(use_proxy=False,custom_proxy=None):
     with open('next_page_links.txt','r') as f:
        lines=f.readlines()
     print(lines)
     for line in lines:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                "Accept": "text/html"
            }
            '''
            proxies = {"http": "http://10.10.1.10:3128",
            "https": "http://10.10.1.10:1080"}
            '''
            LoadUpProxies()
            proxies_server = None
            #print(proxies)
            if use_proxy and proxies:
                random_proxy = random.choice(proxies)
                proxy_url_http = f"http://{random_proxy['ip']}:{random_proxy['port']}" 
                proxy_url_https = f"https://{random_proxy['ip']}:{random_proxy['port']}"   
                proxies_server={"http": proxy_url_http,"https":proxy_url_https}
                print("Random Proxy:", random_proxy)
            elif custom_proxy:
                proxy_url_http = f"http://{custom_proxy}"
                proxy_url_https = f"https://{custom_proxy}"
                proxies_server = {"http": proxy_url_http, "https": proxy_url_https}    
            else:
                print("No proxies available.")
            base_url = line
            print(base_url)
            #print(proxies_server)
            response = requests.get(base_url, headers=headers, proxies=proxies_server, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            ads = []
            shopping_results = []

            while True:
                for el in soup.select(".sh-np__click-target"):
                    ad = {
                        "title": el.select_one(".sh-np__product-title").get_text() if el.select_one(".sh-np__product-title") else None,
                        "link": "https://google.com" + el.get("href"),
                        "source": el.select_one(".sh-np__seller-container").get_text() if el.select_one(".sh-np__seller-container") else None,
                        "price": el.select_one(".hn9kf").get_text() if el.select_one(".hn9kf") else None,
                        "delivery": el.select_one(".U6puSd").get_text() if el.select_one(".U6puSd") else None,
                    }
                    extensions = el.select_one(".rz2LD")
                    if extensions:
                        ad["extensions"] = extensions.get_text()
                    ads.append(ad)

                for el in soup.select(".sh-dgr__gr-auto"):
                    result = {
                        "title": el.select_one("h3.tAxDx").get_text() if el.select_one("h3.tAxDx") else None,
                        "link": el.select_one(".zLPF4b .eaGTj a.shntl")["href"][el.select_one("a.shntl")["href"].index("=") + 1:] if el.select_one(".zLPF4b .eaGTj a.shntl") else None,
                        "source": el.select_one(".IuHnof").get_text().replace(".aULzUe{.*?}.aULzUe::after{.*?}", "") if el.select_one(".IuHnof") else None,
                        "price": el.select_one(".XrAfOe .a8Pemb").get_text() if el.select_one(".XrAfOe .a8Pemb") else None,
                        "rating": None,
                        "reviews": None,
                        "delivery": el.select_one(".vEjMR").get_text() if el.select_one(".vEjMR") else None,
                    }

                    rating_element = el.select_one(".NzUzee .QIrs8")
                    if rating_element:
                        rating_text = rating_element.get_text().strip()
                        #print(rating_text)
                        if "out" in rating_text:
                            try:
                                result["rating"] = float(rating_text.split("out")[0].strip())
                                #print(result["rating"])
                                result["reviews"] = extract_number_from_string(rating_text)
                                #print(result["reviews"])
                            except ValueError:
                                pass

                    extensions = el.select_one(".Ib8pOd")
                    if extensions:
                        result["extensions"] = extensions.get_text()
                    shopping_results.append(result)
                
                for ad in ads:
                    ad.pop("", None)

                for result in shopping_results:
                    result.pop("", None)

                append_into_csv_and_json(ads, shopping_results)
                break
        except Exception as e:
            print(e)

def append_into_csv_and_json(ads,shopping_results):
    with open("shopping_results_data.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "link", "source", "price", "rating", "reviews", "delivery", "extensions"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in shopping_results:
            writer.writerow(result)
    with open("shopping_results_data.json", "a", encoding="utf-8") as jsonfile:
        json.dump(shopping_results, jsonfile, ensure_ascii=False, indent=2)        


#append_next_pages()

    
       
        