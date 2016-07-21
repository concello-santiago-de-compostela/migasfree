# -*- coding: utf-8 -*-

# import order is very important!!!

from .stats import (
    daily_updated,
    delay_schedule,
    hourly_updated,
    monthly_updated,
    version_computer
)
from .queries import get_query, computer_messages, server_messages
from .hardware import hardware_resume, hardware_extract, load_hw, process_hw
from .client_api import api
from .public_api import (
    get_versions, get_computer_info, computer_label,
    get_key_repositories
)
from .packages import change_version, info
from .dashboard import alerts
from .login import login
from .computer import (
    ComputerDelete,
    computer_delete_selected,
    computer_replacement
)
from .version import VersionDelete
from .platform import PlatformDelete, platform_delete_selected
from .devices import append_devices_from_computer, connections_model
from .autocomplete import ComputerAutocomplete, AttributeAutocomplete
from .token import (
    ComputerViewSet, VersionViewSet, PlatformViewSet,
    PmsViewSet, StoreViewSet, PropertyViewSet,
    AttributeViewSet, ScheduleViewSet, PackageViewSet,
    RepositoryViewSet, ErrorViewSet, FaultDefinitionViewSet,
    FaultViewSet, NotificationViewSet, MigrationViewSet,
    HardwareComputerViewSet, HardwareViewSet, CheckingViewSet,
    UserViewSet,
)
