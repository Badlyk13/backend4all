import json
import logging
from django.shortcuts import render
from amocrm.utils.upd_access_token import *
from amocrm.models import Client

logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    logs = []
    with open('debug.log', 'r') as f:
        for line in f.readlines():
            logs.append(json.loads(line))
    return render(request, 'index.html', {'logs': logs})
