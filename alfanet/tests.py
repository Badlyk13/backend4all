from datetime import datetime

import requests
from django.test import TestCase

from alfanet.utils import get_all_leads


def pars_beeline(ls_num):
    url = 'https://partnerweb.beeline.ru/'
    accounts = [{'login': 'VV41-221', 'workercode': '2000000002', 'password': 'alfanet2022'},
                {'login': 'S88-181', 'workercode': '2000000001', 'password': 'qwerty-123'}]
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
        # r4 = requests.get(f'https://partnerweb.beeline.ru/restapi/tickets/ticket_popup/{r3.json()[0]["id"]}',
        #                   headers=headers, params=data)
        session.close()
        print(r3.json())
    return True


# Create your tests here.
def beeline(pk):
    leads = get_all_leads(pk)
    provider, city, order_num = None, None, None
    for lead in leads[:5]:
        for field in lead['custom_fields_values']:
            if field['field_id'] == 755993:  # 755993 - Поле "Провайдер"
                provider = field['values'][0]['value']
            if field['field_id'] == 972871:  # 972871 - Поле "Город"
                city = field['values'][0]['value']
            if field['field_id'] == 757315:  # 757315 - Поле "Номер заявки"
                order_num = field['values'][0]['value'] # 755993 - Поле "Номер заявки"
        if provider == 'Билайн' and city == 'Москва':
            pars_beeline(order_num)

print(beeline)