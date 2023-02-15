'''
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
'''

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=60, db_index=True)
    last_name = models.CharField(max_length=60, db_index=True)
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    phone1 = models.CharField(max_length=12)
    phone2 = models.CharField(max_length=12)
    email = models.CharField(max_length=200)
    web = models.CharField(max_length=400)
