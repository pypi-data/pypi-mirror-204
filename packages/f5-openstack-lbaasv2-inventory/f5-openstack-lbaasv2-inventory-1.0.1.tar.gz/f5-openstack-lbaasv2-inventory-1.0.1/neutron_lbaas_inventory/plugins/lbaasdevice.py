from oslo_log import log

from neutron_lbaas_inventory.db.inventory_db import InventoryDbPlugin
from neutron_lbaas_inventory.extensions import lbaasdevice

LOG = log.getLogger(__name__)


class LbaasDevicePlugin(lbaasdevice.LbaasDevicePluginBase):
    supported_extension_aliases = ["lbaas-device"]
    inventory_db = InventoryDbPlugin()

    def get_devices(self, context, filters=None, fields=None,
                    sorts=None, limit=None, marker=None,
                    page_reverse=False):
        LOG.debug("List lbaas devices")
        devices = self.inventory_db.get_devices(context, filters=filters)
        return devices

    def get_device(self, context, id, fields=None):
        LOG.debug("Get a lbaas device, id: {}".format(id))
        return self.inventory_db.get_device(context, id)

    def create_device(self, context, device):
        LOG.debug("Create lbaas device, device_info: {}".format(device))
        return self.inventory_db.create_device(context, device)

    def delete_device(self, context, id):
        LOG.debug("Delete lbaas device, id: {}".format(id))
        self.inventory_db.delete_device(context, id)

    def update_device(self, context, id, device):
        LOG.debug("Update lbaas device, id: {}, device: {}".format(id, device))
        return self.inventory_db.update_device(context, id, device)

    def get_loadbalanceragentbindings(self, context, filters=None, fields=None,
                                      sorts=None, limit=None, marker=None,
                                      page_reverse=False):
        LOG.debug("List loadbalancer device bindings")
        lb_device_bindings = self.inventory_db.get_bindings(context,
                                                            filters=filters)
        return lb_device_bindings

    def get_device_members(self, context, device_id, filters=None,
                           fields=None):
        LOG.debug("Get lbaas device members, device_id: {}".format(device_id))
        filters['device_id'] = [device_id]
        return self.inventory_db.get_members(context, filters=filters)

    def get_device_member(self, context, id, device_id, fields=None):
        LOG.debug("Get lbaas device member, device_id: {}, id: {}"
                  .format(device_id, id))
        return self.inventory_db.get_member(context, id)

    def create_device_member(self, context, device_id, member):
        LOG.debug("Create lbaas device member, device_id: {}, member: {}"
                  .format(device_id, member))
        return self.inventory_db.create_member(context, device_id, member)

    def update_device_member(self, context, id, device_id, member):
        LOG.debug("Update lbaas device member, device_id: {}, id: {}"
                  .format(device_id, id))
        return self.inventory_db.update_member(context, id, member)

    def delete_device_member(self, context, id, device_id):
        LOG.debug("Delete lbaas device member, device_id: {}, id: {}"
                  .format(device_id, id))
        self.inventory_db.delete_member(context, id)
