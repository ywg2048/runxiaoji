# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PurchaseOrders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mipurchaseorderdata',
            old_name='AppID',
            new_name='AppId',
        ),
        migrations.RenameField(
            model_name='mipurchaseorderdata',
            old_name='CpOrderID',
            new_name='CpOrderId',
        ),
        migrations.RenameField(
            model_name='mipurchaseorderdata',
            old_name='OrderID',
            new_name='OrderId',
        ),
    ]
