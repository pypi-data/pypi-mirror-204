from neutron_lib.db import model_base
import sqlalchemy as sa


class Device(model_base.BASEV2, model_base.HasId, model_base.HasProject):
    """Represents a backend device"""

    NAME = "device"

    __tablename__ = "lbaas_devices"

    name = sa.Column(sa.String(255), nullable=True)
    description = sa.Column(sa.String(255), nullable=True)
    shared = sa.Column(sa.Boolean(), nullable=False)
    admin_state_up = sa.Column(sa.Boolean(), nullable=False)
    availability_zone = sa.Column(sa.String(255), nullable=True)
    device_info = sa.Column(sa.String(4095), nullable=False)
    provisioning_status = sa.Column(sa.String(255), nullable=True)


class DeviceMember(model_base.BASEV2, model_base.HasId):
    """Represents device members."""

    __tablename__ = "lbaas_device_members"

    device_id = sa.Column(sa.String(36),
                          sa.ForeignKey("lbaas_devices.id"),
                          nullable=False)
    type = sa.Column(sa.String(16), nullable=False)
    mgmt_ipv4 = sa.Column(sa.String(255), nullable=False)
    mgmt_ipv6 = sa.Column(sa.String(255), nullable=True)
    device_info = sa.Column(sa.String(4095), nullable=False)
    operating_status = sa.Column(sa.String(255), nullable=True)
    last_error = sa.Column(sa.String(4095), nullable=True)
