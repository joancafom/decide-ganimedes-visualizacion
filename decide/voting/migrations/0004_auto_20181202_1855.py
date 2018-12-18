# Generated by Django 2.0 on 2018-12-02 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionoption',
            name='gender',
            field=models.NullBooleanField(choices=[(True, 'Male'), (False, 'Female')]),
        ),
        migrations.AlterField(
            model_name='questionoption',
            name='team',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionoption',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='voting',
            name='postproc_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Identity'), (1, 'Weight'), (2, 'Seats'), (3, 'Parity'), (4, 'Team')], default=0, null=True),
        ),
    ]
