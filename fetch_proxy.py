import requests
from bs4 import BeautifulSoup

def get_free_proxy():
    url = "https://www.free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find(id='proxylisttable')
    rows = table.tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols[4].text.strip() == 'elite proxy' and cols[6].text.strip() == 'yes':
            proxy = f"{cols[0].text.strip()}:{cols[1].text.strip()}"
            return proxy
    return None
