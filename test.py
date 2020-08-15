import requests
from bs4 import BeautifulSoup

headers = {
    'authority': 'www.transdirect.com.au',
    'cache-control': 'max-age=0',
    'origin': 'https://www.transdirect.com.au',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.transdirect.com.au/quotes?redirect=true',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': '__cfduid=d081ae62dbf1c9046c958d24cfe7db74c1597431833; _vwo_uuid_v2=D5EAEB9DB086FE660E04C7326E5181A9B|9680554a673015e5d8da7d775c200f10; ext_name=ojplmecpdpgccookcobabopnaifgidhf; app[booking::11660217]=1; app[popupSession::11660217]=5; PHPSESSID=uo7jr6279i52ctl7sdv028e7e3; wpfront-notification-bar-landingpage=1; AWSELB=CB6D697910B21CBC215B0D2727D24B454055A6B88E12D599E824A5D7F298B77E2F8E528F6C3A95111CC5FFCCCEC47482558C8CDD78D24C3A16003D1DAF46FCA6C48CF2E463; AWSELBCORS=CB6D697910B21CBC215B0D2727D24B454055A6B88E12D599E824A5D7F298B77E2F8E528F6C3A95111CC5FFCCCEC47482558C8CDD78D24C3A16003D1DAF46FCA6C48CF2E463; transdirectrestapi=clnv53gtfdbnskog3jgple8rb7',
}

data = {
    'origin_iframe': '0',
    'iframe': '0',
    'from-postcode': '5966',
    'to-postcode': '14220',
    'from-address-type': 'residential',
    'to-address-type': 'residential',
    'collection-addresses': '0',
    'delivery-addresses': '0',
    'type[]': 'Carton',
    'weight[]': '20',
    'length[]': '100',
    'width[]': '100',
    'height[]': '50',
    'quantity[]': '1'
}

session = requests.session()

response = session.post('https://www.transdirect.com.au/quotes/bookings/build_quotes', headers=headers, data=data)
url = response.url


def get_price(link, token):
    headers = {
        'authority': 'www.transdirect.com.au',
        'accept': '*/*',
        'dnt': '1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.transdirect.com.au',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.transdirect.com.au/quotes/bookings/11663134/quotes',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': '__cfduid=d081ae62dbf1c9046c958d24cfe7db74c1597431833; _vwo_uuid_v2=D5EAEB9DB086FE660E04C7326E5181A9B|9680554a673015e5d8da7d775c200f10; ext_name=ojplmecpdpgccookcobabopnaifgidhf; app[booking::11660217]=1; app[popupSession::11660217]=5; PHPSESSID=uo7jr6279i52ctl7sdv028e7e3; wpfront-notification-bar-landingpage=1; AWSELB=CB6D697910B21CBC215B0D2727D24B454055A6B88E12D599E824A5D7F298B77E2F8E528F6C3A95111CC5FFCCCEC47482558C8CDD78D24C3A16003D1DAF46FCA6C48CF2E463; AWSELBCORS=CB6D697910B21CBC215B0D2727D24B454055A6B88E12D599E824A5D7F298B77E2F8E528F6C3A95111CC5FFCCCEC47482558C8CDD78D24C3A16003D1DAF46FCA6C48CF2E463; transdirectrestapi=clnv53gtfdbnskog3jgple8rb7; app[booking::11663134]=1; app[popupSession::11663134]=9; app[security][token]=8caf04673d586018740930a5bd6e512bcaf522aac3b1c8f6a37c1c04e44797b5ce95c5fb3ac7bc076cf9e4be4aac7fbc0a668afa9e91a4d96f04b3310bbce502',
    }

    data = {
        'security[token]': token
    }
    try:
        response = session.post(link, headers=headers,
                                data=data, timeout=2)
    except:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        return soup.find('span', {'class': 'total-price'}).text
    except:
        return None


soup = BeautifulSoup(response.content, 'html.parser')
token = soup.find('input', {'name': 'security[token]'})['value']
table = soup.find('tbody', {'id': 'list-quotes'})
trs = table.find_all('tr')
for tr in trs:
    try:
        tr_id = tr['id']
        link = url + '/' + tr_id.replace('loader-', '')
        print(link, end=': ')
        price = get_price(link, token)
        print(price)
    except:
        pass
