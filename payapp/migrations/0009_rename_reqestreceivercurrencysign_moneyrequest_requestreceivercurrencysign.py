# Generated by Django 4.2.11 on 2024-05-02 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0008_moneyrequest_reqestreceivercurrencysign_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moneyrequest',
            old_name='reqestReceiverCurrencySign',
            new_name='requestReceiverCurrencySign',
        ),
    ]
