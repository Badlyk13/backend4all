from django.db import models
import requests



# Create your models here.


class Client(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=64, blank=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=16, blank=True)
    amo_url = models.CharField(verbose_name='Адрес AmoCrm', max_length=50, blank=True)
    access_token = models.CharField(verbose_name='Access token', max_length=1000, blank=True)
    refresh_token = models.CharField(verbose_name='Refresh token', max_length=1000, blank=True)
    client_id = models.CharField(verbose_name='App Client ID', max_length=200, blank=True)
    client_secret = models.CharField(verbose_name='App Client Secret', max_length=1000, blank=True)
    auth_code = models.CharField(verbose_name='App AuthCode', max_length=2000, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return f'{self.name} {self.phone} {self.amo_url}'

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)
        if not self.access_token:
            params = {
                "client_id": f"{self.client_id}",
                "client_secret": f"{self.client_secret}",
                "grant_type": "authorization_code",
                "code": f"{self.auth_code}",
                "redirect_uri": "https://smartbot4u.ru/"
            }
            r = requests.post(f'https://{self.amo_url}/oauth2/access_token', params)
            self.access_token = r.json()['access_token']
            self.refresh_token = r.json()['refresh_token']
            super(Client, self).save(*args, **kwargs)