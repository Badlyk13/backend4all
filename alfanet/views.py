import csv
from datetime import datetime, timedelta
from random import random
from time import sleep

import requests
from django.http import JsonResponse
from django.shortcuts import render

from alfanet.forms import UploadFileForm
from alfanet.utils import get_all_leads, test_alfa, patch_to_lead, sorted_leads


# +++++++++++++++++++++++++++++ БИЛАЙН ++++++++++++++++++++++++++++++++++

def beeline(request, pk):
    leads = get_all_leads(pk)
    provider, order_num = None, None
    leads_to_parse = []
    for lead in leads:
        for field in lead['custom_fields_values']:
            if field['field_id'] == 755993:  # 755993 - Поле "Провайдер"
                provider = field['values'][0]['value']
            if field['field_id'] == 757315:  # 757315 - Поле "Номер заявки"
                order_num = field['values'][0]['value']  # 755993 - Поле "Номер заявки"
        if provider == 'Билайн':
            leads_to_parse.append(lead)
    pars_beeline(leads_to_parse)

    return JsonResponse('ok', safe=False)


def pars_beeline(leads):
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
    second_iter = []

    def get_status(iter):
        session = requests.Session()
        data = {
            'dateFrom': datetime.strftime(datetime.now() - timedelta(days=90), '%d.%m.%Y'),
            'dateTo': datetime.strftime(datetime.now(), '%d.%m.%Y'),
            'format': 'json',
        }
        if not iter:
            params = {
                'login': f'{accounts[iter]["login"]}',
                'workercode': f'{accounts[iter]["workercode"]}',
                'password': f'{accounts[iter]["password"]}'
            }
            session.post(url, headers=headers, data=params)
            headers['Cookie'] = f"sessionid={session.cookies.get_dict()['sessionid']}"
            headers['content-type'] = 'application/json'

            for lead in leads:
                for field in lead['custom_fields_values']:
                    if field['field_id'] == 757315:  # 757315 - Поле "Номер заявки"
                        data['number'] = field['values'][0]['value']  # 755993 - Поле "Номер заявки"
                r3 = requests.get(f'https://partnerweb.beeline.ru/restapi/tickets/', headers=headers, params=data)
                if r3.status_code == 200:
                    try:
                        print(lead['id'])
                        patch_to_lead(2, lead['id'], r3.json()[0]['status'])
                    except IndexError:
                        second_iter.append(lead)
                sleep(0.5)

            session.get(f'https://partnerweb.beeline.ru/logout/', headers=headers)
            session.close()
        else:
            params = {
                'login': f'{accounts[iter]["login"]}',
                'workercode': f'{accounts[iter]["workercode"]}',
                'password': f'{accounts[iter]["password"]}'
            }
            session.post(url, headers=headers, data=params)

            for lead in second_iter:
                for field in lead['custom_fields_values']:
                    if field['field_id'] == 757315:  # 757315 - Поле "Номер заявки"
                        data['number'] = field['values'][0]['value']  # 755993 - Поле "Номер заявки"
                r3 = requests.get(f'https://partnerweb.beeline.ru/restapi/tickets/', headers=headers, params=data)
                if r3.status_code == 200:
                    try:
                        patch_to_lead(2, lead['id'], r3.json()[0]['status'])
                    except IndexError:
                        patch_to_lead(2, lead['id'], "Заявка не найдена")
                sleep(0.5)

        if iter == 0:
            del headers['content-type']
            session.get(f'https://partnerweb.beeline.ru/logout/', headers=headers)
            sleep(5)
            session.close()
            sleep(5)
            return second_iter
        else:
            return False

    if get_status(0):
        get_status(1)
    return True


# +++++++++++++++++++++++++++++ MTC ++++++++++++++++++++++++++++++++++

def upload_mts_csv(request, pk):
    if request.method == 'POST':
        order_num = None
        form = UploadFileForm(request.POST, request.FILES)
        file_name = ''
        if form.is_valid():
            for filename, file in request.FILES.items():
                file_name = f'{file}'
            statuses = handle_uploaded_file(request.FILES['file'], file_name)
            leads = sorted_leads('Мтс', 2)
            for order in statuses:
                for lead in leads:
                    for field in lead['custom_fields_values']:
                        if field['field_id'] == 757315:  # 757315 - Поле "Номер заявки"
                            order_num = field['values'][0]['value']
                            break
                    if order[0] == order_num: # 755993 - Поле "Номер заявки"
                        try:
                            patch_to_lead(2, lead['id'], order[1])
                        except IndexError:
                            continue
                        finally:
                            break
            return render(request, 'alfanet/upload_form.html', {'form': form, 'status': 1})
    else:
        form = UploadFileForm()
    return render(request, 'alfanet/upload_form.html', {'form': form, 'status': 0})


def handle_uploaded_file(f, file):
    with open('alfanet/mts_orders_report/' + file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open('alfanet/mts_orders_report/' + file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        statuses_to_amo = []
        for i, row in enumerate(reader):
            mas = row.get('sep=\t').split('\t')
            order_num = mas[0]
            order_status = mas[5]
            statuses_to_amo.append([order_num, order_status])
    return statuses_to_amo





def test(request):
    return JsonResponse('ok', safe=False)
