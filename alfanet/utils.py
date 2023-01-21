import json
import logging
from time import sleep

import requests
from django.http import JsonResponse

from amocrm.models import Client
from amocrm.utils.upd_access_token import update_access_token

logger = logging.getLogger(__name__)


def get_all_leads(pk):
    client = Client.objects.get(pk=pk)
    head = {"Authorization": f'Bearer {client.access_token}', "Content-Type": "application/json"}
    status = 'application/hal+json'
    i = 0
    leads = []
    try:
        while status == 'application/hal+json':
            data = {'page': i}
            response = requests.get(f'https://{client.amo_url}/api/v4/leads', headers=head, params=data)
            if response.status_code == 200:
                status = response.headers['Content-Type']
                if status == 'application/hal+json':
                    res = response.json()['_embedded']['leads']
                    for j in res:
                        if j['status_id'] != 143 and j['status_id'] != 142:
                            leads.append(j)
                    i += 1
                    sleep(0.3)
                else:
                    break
            if response.status_code == 204:
                break
            if response.status_code == 401:
                update_access_token(client)
            # response = requests.get(f'https://{client.amo_url}/api/v4/leads/custom_fields', headers=head)
        logger.info(f'{client} get_leads ok')
        return leads
    except Exception as e:
        logger.error(f'{client} get_leads {e}')
        return False


def patch_to_lead(pk, lead_id, status):
    client = Client.objects.get(pk=pk)
    head = {"Authorization": f'Bearer {client.access_token}', "Content-Type": "application/json"}
    data = [{"id": lead_id, "custom_fields_values": [{"field_id": 904099, "values": [{"value": f"{status}"}]}]}]
    response = requests.patch(f'https://{client.amo_url}/api/v4/leads', headers=head, data=json.dumps(data))
    if response.status_code == 401:
        update_access_token(client)
        response = requests.patch(f'https://{client.amo_url}/api/v4/leads', headers=head, data=json.dumps(data))
        if response.status_code != 200:
            logger.warning(f'{client}, заявка {lead_id}, статус не обновлен!')
            return False
    else:
        return True


def sorted_leads(dealer, pk):
    leads = get_all_leads(pk)
    order_num, provider = None, None
    leads_to_parse = []
    for lead in leads:
        for field in lead['custom_fields_values']:
            if field['field_id'] == 755993:  # 755993 - Поле "Провайдер"
                provider = field['values'][0]['value']
        if provider == dealer:
            leads_to_parse.append(lead)
    return leads_to_parse



def test_alfa(pk):
    client = Client.objects.get(pk=pk)
    head = {"Authorization": f'Bearer {client.access_token}', "Content-Type": "application/json"}
    status = 'application/hal+json'
    i = 80
    leads = []
    field_id = 755993
    enum_id = 358263
    response = requests.get(f'https://{client.amo_url}/api/v4/leads?filter[custom_fields_values][{field_id}][]={enum_id}', headers=head)
    print(response.json())

