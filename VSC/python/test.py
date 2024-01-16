import random
import requests
from threading import Thread
import time
 
class ProxyPool(object):
    def __init__(self):
        self.pool = []
        self.check_interval = 600  # 代理IP检查周期，单位为秒
        Thread(target=self.check_proxy_loop).start()
 
    def add_proxy(self, proxy):
        if self.check_proxy(proxy):
            self.pool.append(proxy)
 
    def check_proxy(self, proxy):
        try:
            res = requests.get('http://www.baidu.com', proxies=proxy, timeout=5)
            if res.status_code == 200:
                return True
            else:
                return False
        except:
            return False
 
    def get_proxy(self):
        if not self.pool:
            return None
        return random.choice(self.pool)
 
    def check_proxy_loop(self):
        while True:
            for proxy in self.pool:
                if not self.check_proxy(proxy):
                    self.pool.remove(proxy)
                    print('{} removed from proxy pool'.format(proxy))
            time.sleep(self.check_interval)
 
def main():
    proxy_pool = ProxyPool()
    url = 'https://www.baidu.com'
    proxy = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    html = get_html(url, proxy)
    print(html)
 
if __name__ == '__main__':
    main()