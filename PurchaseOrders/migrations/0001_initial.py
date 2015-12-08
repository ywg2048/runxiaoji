# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MiPurchaseOrderData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('AppID', models.CharField(null=True, blank=True, max_length=80)),
                ('CpOrderID', models.CharField(null=True, blank=True, max_length=40)),
                ('CpUserInfo', models.CharField(null=True, blank=True, max_length=40)),
                ('UId', models.CharField(null=True, blank=True, max_length=40)),
                ('OrderID', models.CharField(null=True, blank=True, max_length=40)),
                ('OrderStatus', models.CharField(null=True, blank=True, max_length=40)),
                ('PayFee', models.CharField(null=True, blank=True, max_length=40)),
                ('ProductCode', models.CharField(null=True, blank=True, max_length=40)),
                ('ProductName', models.CharField(null=True, blank=True, max_length=40)),
                ('ProductCount', models.CharField(null=True, blank=True, max_length=40)),
                ('PayTime', models.CharField(null=True, blank=True, max_length=40)),
                ('OrderConsumeType', models.CharField(null=True, blank=True, max_length=40)),
                ('PartnerGiftConsume', models.CharField(null=True, blank=True, max_length=40)),
                ('Signature', models.CharField(null=True, blank=True, max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
