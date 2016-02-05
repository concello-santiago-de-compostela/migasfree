# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from . import DeviceType


@python_2_unicode_compatible
class DeviceConnection(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=50,
        null=True,
        blank=True
    )

    fields = models.CharField(
        verbose_name=_("fields"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Fields separated by comma")
    )

    devicetype = models.ForeignKey(
        DeviceType,
        verbose_name=_("device type")
    )

    def __str__(self):
        return '(%s) %s' % (self.devicetype.name, self.name)

    class Meta:
        app_label = 'server'
        verbose_name = _("Connection")
        verbose_name_plural = _("Connections")
        unique_together = (("devicetype", "name"),)
        permissions = (
            ("can_save_deviceconnection", "Can save Device Connection"),
        )
