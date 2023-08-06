from neutron_lib import exceptions as n_exc
from neutron._i18n import _


class DeviceNotFound(n_exc.NotFound):
    message = _("Device %(device_id)s could not be found")


class DeviceInUse(n_exc.InUse):
    message = _("Device %(device_id)s is currently used by "
                "loadbalancers: %(loadbalancer_ids)s")


class DeviceMemberNotFound(n_exc.NotFound):
    message = _("Device member %(device_member_id)s could not be found")


class DeviceMemberInUse(n_exc.InUse):
    message = _("Device %(device_id)s is currently used by "
                "device members: %(member_ids)s")
