import requests
from bs4 import BeautifulSoup

def fetch_proxies():


    url = "https://free-proxy-list.net"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    proxies = []

    table = soup.find('table', class_='table-striped')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            protocol = columns[6].text.strip().lower()
            if protocol == 'no':
                proxy = f'http://{ip}:{port}'
            elif protocol == '':
                proxy = f'{ip}:{port}'
            else:
                proxy = f'https://{ip}:{port}'
                proxies.append(proxy)
    return proxies
# fetch_proxies()

# print(fetch_proxies())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
}

url = "https://www.freeproxy.world/"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
print(response.status_code)

proxy_list = []
body = soup.find('tbody')
# print(body)
visi_tr = soup.find_all('td', class_='show-ip-div')
for i in visi_tr:
    ip = i.text.strip()
    proxy_list.append(ip)
# print(proxy_list)

# proxy_list2 = []
#
body = soup.find_all('a', href=True)
# for x in visi_td:
#     port = i.text.strip()
#     proxy_list2.append(port)
# print(visi_td)
# print(proxy_list2)
# print(visi_td)
print(body)