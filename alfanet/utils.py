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
    i = 80
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