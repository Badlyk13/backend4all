from amocrm.models import Client
from django.http import JsonResponse
import requests
import fake_useragent
# import pandas as pd
# import gspread


def get_leads(request, pk):
    client = Client.objects.get(pk=pk)
    head = {"Authorization": f'Bearer {client.access_token}', "Content-Type": "application/json"}
    data = {"with": 'contacts', 'page': 1}
    data = {
        'page': 1
    }
    # f'https://{AMO_URL}/api/v4/leads?filter[statuses][0][pipeline_id]=3572632&filter[statuses][0][status_id]={crater}&filter[closed_at][from]={date_from}&filter[closed_at][to]={date_to}',

    response = requests.get(f'https://{client.amo_url}/api/v4/leads/custom_fields', headers=head)
    status = response.headers['Content-Type']
    print(response.json())
    res = response.json()['_embedded']['leads']

    return JsonResponse(res, safe=False)
