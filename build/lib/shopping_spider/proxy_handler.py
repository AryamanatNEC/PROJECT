import random

def setup_proxy(use_proxy, proxies, custom_proxy=None):
    proxies_server = None
    if custom_proxy:
        proxy_url_http = f"http://{custom_proxy}"
        proxy_url_https = f"https://{custom_proxy}"
        proxies_server = {"http": proxy_url_http, "https": proxy_url_https}
        print("User Defined Proxy:", custom_proxy)
    elif use_proxy and proxies:
        random_proxy = random.choice(proxies)
        proxy_url_http = f"http://{random_proxy['ip']}:{random_proxy['port']}"
        proxy_url_https = f"https://{random_proxy['ip']}:{random_proxy['port']}"
        proxies_server = {"http": proxy_url_http, "https": proxy_url_https}
        print("Random Proxy:", random_proxy)      
    else:
        print("No proxies available.")
      

    return proxies_server
