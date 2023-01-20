import requests
import logging

logger = logging.getLogger(__name__)


def get_access_token(client):
    logger.info(f'{client} get_access_token ')
    params = {
        "client_id": f"{client.client_id}",
        "client_secret": f"{client.client_secret}",
        "grant_type": "authorization_code",
        "code": f"{client.auth_code}",
        "redirect_uri": "https://smartbot4u.ru/"
    }
    r = requests.post(f'https://{client.amo_url}/oauth2/access_token', params)
    try:
        client.access_token = r.json()['access_token']
        client.refresh_token = r.json()['refresh_token']
        client.save()
        logger.info(f'{client} Take access_token')
    except Exception as e:
        logger.error(f'{client}: get_access_token - {e}')

    return True


def update_access_token(client):
    params = {
        "client_id": f"{client.client_id}",
        "client_secret": f"{client.client_secret}",
        "grant_type": "refresh_token",
        "refresh_token": f"{client.refresh_token}",
        "redirect_uri": "https://smartbot4u.ru/"
    }
    r = requests.post(f'https://{client.amo_url}/oauth2/access_token', params)
    try:
        client.access_token = r.json()['access_token']
        client.refresh_token = r.json()['refresh_token']
        client.save()
        logger.info(f'{client} update access_token')
    except Exception as e:
        logger.error(f'{client}: update_access_token - {e}')

    return True

