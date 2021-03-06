# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def logical_device_by_attributes(apps, schema_editor):
    Computer = apps.get_model('server', 'Computer')
    Attribute = apps.get_model('server', 'Attribute')
    db_alias = schema_editor.connection.alias
    for computer in Computer.objects.using(db_alias).exclude(devices_logical=None):
        try:
            cid = Attribute.objects.using(db_alias).get(
                value=computer.pk,
                property_att__prefix='CID'
            )
            for logical_device in computer.devices_logical.all():
                logical_device.attributes.add(cid)
        except:
            print("Computer id: %s, does not have CID attribute!!!" % computer.id)


def logical_device_by_computer(apps, schema_editor):
    Computer = apps.get_model('server', 'Computer')
    DeviceLogical = apps.get_model('server', 'DeviceLogical')
    db_alias = schema_editor.connection.alias
    for device in DeviceLogical.objects.using(db_alias).exclude(attributes=None):
        for attribute in device.attributes.filter(property_att__prefix='CID'):
            computer = Computer.objects.using(db_alias).get(
                pk=int(attribute.value)
            )
            computer.devices_logical.add(device)


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_4_13_changes'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicelogical',
            name='attributes',
            field=models.ManyToManyField(
                blank=True,
                help_text='Assigned Attributes',
                to='server.Attribute',
                verbose_name='attributes'
            ),
        ),
        migrations.AddField(
            model_name='computer',
            name='default_logical_device',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='server.DeviceLogical',
                verbose_name='default logical device'
            ),
        ),
        migrations.RunPython(
            logical_device_by_attributes,
            logical_device_by_computer
        ),
        migrations.RemoveField(
            model_name='computer',
            name='devices_copy',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='devices_logical',
        ),
        migrations.RemoveField(
            model_name='checking',
            name='alert',
        ),
    ]
