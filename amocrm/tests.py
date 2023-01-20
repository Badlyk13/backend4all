from datetime import datetime, timedelta

import requests
import fake_useragent
from bs4 import BeautifulSoup


def pars_beeline(url):
    ls_num = 255089799
    accounts = [{'login': 'VV41-221', 'workercode': '2000000002', 'password': 'alfanet2022'}, ]
    headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        }
    for account in accounts:
        params = {
            'login': f'{account["login"]}',
            'workercode': f'{account["workercode"]}',
            'password': f'{account["password"]}'

        }
        session = requests.Session()
        session.post(url, headers=headers, data=params)
        headers['Cookie'] = f"sessionid={session.cookies.get_dict()['sessionid']}"
        headers['content-type'] = 'application/json'
        data = {
            'dateFrom': datetime.strftime(datetime.now() - timedelta(days=90), '%d.%m.%Y'),
            'dateTo': datetime.strftime(datetime.now(), '%d.%m.%Y'),
            'number': ls_num,
            'format': 'json',
        }
        r3 = requests.get(f'https://partnerweb.beeline.ru/restapi/tickets/', headers=headers, params=data)
        r4 = requests.get(f'https://partnerweb.beeline.ru/restapi/tickets/ticket_popup/{r3.json()[0]["id"]}', headers=headers, params=data)
        session.close()
        return r4.json()

