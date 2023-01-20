from datetime import datetime, timedelta

import requests
from django.http import JsonResponse
from django.shortcuts import render

from alfanet.utils import get_all_leads


def beeline(request, pk):
    leads = get_all_leads(pk)
    provider, city, order_num = None, None, None
    orders_to_parse = []
    for lead in leads:
        for field in lead['custom_fields_values']:
            if field['field_id'] == 755993:  # 755993 - Поле "Провайдер"
                provider = field['values'][0]['value']
            if field['field_id'] == 972871:  # 972871 - Поле "Город"
                city = field['values'][0]['value']
            if field['field_id'] == 757315:  # 757315 - Поле "Номер заявки"
                order_num = field['values'][0]['value'] # 755993 - Поле "Номер заявки"
        if provider == 'Билайн':
            print(provider, city, order_num)
            if order_num.isdigit():
                orders_to_parse.append(order_num)
    print('Передал заявок:', len(orders_to_parse))
    pars_beeline(orders_to_parse)

    return JsonResponse('ok', safe=False)


def pars_beeline(orders):
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

    for order in orders:
        account = 0
        while account < len(accounts):
            params = {
                'login': f'{accounts[account]["login"]}',
                'workercode': f'{accounts[account]["workercode"]}',
                'password': f'{accounts[account]["password"]}'

            }
            session = requests.Session()
            session.post(url, headers=headers, data=params)
            headers['Cookie'] = f"sessionid={session.cookies.get_dict()['sessionid']}"
            headers['content-type'] = 'application/json'
            data = {
                'dateFrom': datetime.strftime(datetime.now() - timedelta(days=90), '%d.%m.%Y'),
                'dateTo': datetime.strftime(datetime.now(), '%d.%m.%Y'),
                'number': order,
                'format': 'json',
            }
            r3 = requests.get(f'https://partnerweb.beeline.ru/restapi/tickets/', headers=headers, params=data)
            if
            print(r3.json(), '\n', r3.status_code)
            session.close()
            if r3.json()[0]['status']:
                print(order, r3.json()[0]['status'])
                break
            account += 1

    return True

