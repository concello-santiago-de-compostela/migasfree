# -*- coding: utf-8 -*-

import os
import shutil

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    User as UserSystem,
    UserManager
)
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from migasfree.middleware import threadlocals
from . import Pms, Platform, MigasLink


class VersionManager(models.Manager):
    def create(self, name, pms, platform, autoregister=False):
        obj = Version()
        obj.name = name
        obj.pms = pms
        obj.platform = platform
        obj.autoregister = autoregister
        obj.save()

        return obj


@python_2_unicode_compatible
class Version(models.Model, MigasLink):
    """
    Version of S.O. by example 'Ubuntu natty 32bit' or 'AZLinux-2'
    This is 'your distribution', a set of computers with a determinate
    Distribution for customize.
    """
    name = models.CharField(
        verbose_name=_("name"),
        max_length=50,
        unique=True
    )

    pms = models.ForeignKey(
        Pms,
        verbose_name=_("package management system")
    )

    computerbase = models.CharField(
        verbose_name=_("Actual line computer"),
        max_length=50,
        help_text=_("Computer with the actual line software"),
        default="---"
    )

    base = models.TextField(
        verbose_name=_("Actual line packages"),
        null=False,
        blank=True,
        help_text=_("List ordered of packages of actual line computer")
    )

    autoregister = models.BooleanField(
        verbose_name=_("autoregister"),
        default=False,
        help_text=_("Is not neccesary a user for register the computer in "
                    "database and get the keys.")
    )

    platform = models.ForeignKey(
        Platform,
        verbose_name=_("platform")
    )

    objects = VersionManager()

    def __str__(self):
        return self.name

    def create_dirs(self):
        _repos = os.path.join(
            settings.MIGASFREE_REPO_DIR,
            self.name,
            'REPOSITORIES'
        )
        if not os.path.exists(_repos):
            os.makedirs(_repos)

        _stores = os.path.join(
            settings.MIGASFREE_REPO_DIR,
            self.name,
            'STORES'
        )
        if not os.path.exists(_stores):
            os.makedirs(_stores)

    def update_base(self, base):
        self.base = base
        self.save()

    @staticmethod
    def get_version_names():
        return Version.objects.all().order_by('name').values_list('id', 'name')

    def save(self, *args, **kwargs):
        self.name = self.name.replace(" ", "-")
        self.create_dirs()
        self.base = self.base.replace("\r\n", "\n")

        super(Version, self).save(*args, **kwargs)

    class Meta:
        app_label = 'server'
        verbose_name = _("Version")
        verbose_name_plural = _("Versions")
        permissions = (("can_save_version", "Can save Version"),)
        ordering = ['name']


class UserProfile(UserSystem, MigasLink):
    """
    info = 'For change password use <a href="%s">change password form</a>.' \
        % reverse('admin:password_change')
    """

    version = models.ForeignKey(
        Version,
        verbose_name=_("version"),
        null=True,
        on_delete=models.SET_NULL
    )

    objects = UserManager()

    @staticmethod
    def get_logged_version():
        """
        Return the user version that is logged
        # TODO remove this method
        """
        try:
            return UserProfile.objects.get(
                id=threadlocals.get_current_user().id
            ).version
        except:
            return None

    def update_version(self, version):
        self.version = version
        self.save()

    def save(self, *args, **kwargs):
        if not (
            self.password.startswith("sha1$")
            or self.password.startswith("pbkdf2")
        ):
            super(UserProfile, self).set_password(self.password)

        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        app_label = 'server'
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        permissions = (("can_save_userprofile", "Can save User Profile"),)


@receiver(pre_delete, sender=Version)
def delete_project(sender, instance, **kwargs):
    path = os.path.join(settings.MIGASFREE_REPO_DIR, instance.name)
    if os.path.exists(path):
        shutil.rmtree(path)
