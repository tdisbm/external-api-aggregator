from datetime import datetime
from typing import Optional, List, Dict

from app.components.dto.Account import Account
from app.components.dto.Agent import Agent
from app.components.dto.CPU import CPU
from app.components.dto.Cloud import Cloud
from app.components.dto.Hardware import Hardware
from app.components.dto.Identity import Identity
from app.components.dto.Metadata import Metadata
from app.components.dto.Network import Network
from app.components.dto.NetworkInterface import NetworkInterface
from app.components.dto.OS import OS
from app.components.dto.Security import Security
from app.components.dto.SecurityPolicy import SecurityPolicy
from app.components.dto.Software import Software
from app.components.dto.Tag import Tag
from app.components.dto.Timestamp import Timestamps
from app.utils.data_access_utils import get_datetime
from app.worker.transformer.normalizer.HostNormalizer import HostNormalizer


class CrowdstrikeHostNormalizer(HostNormalizer):
    SOURCE_QUALIFIER = "crowdstrike"

    def _normalize_metadata(self, data: dict) -> Metadata:
        return Metadata(
            source=self.SOURCE_QUALIFIER,
            collection_time=datetime.now(),
        )

    def _normalize_identity(self, data: dict) -> Identity:
        return Identity(
            hostname=data.get("hostname"),
            instance_id=data.get("instance_id"),
            serial_number=data.get("serial_number"),
            fqdn=None,
            external_ids=[
                f"{self.SOURCE_QUALIFIER}:{data.get('device_id')}"
            ]
        )

    def _normalize_network(self, data: dict) -> Network:
        external_ip = data.get("external_ip")
        return Network(
            public_ips=[external_ip] if external_ip else list(),
            dns_names=list(),
            open_ports=list(),
            interfaces=[
                NetworkInterface(
                    name=None,
                    mac=_normalize_mac_address(data.get("mac_address")),
                    gateway=data.get("default_gateway_ip"),
                    ips=list(set(filter(None, [
                        data.get("local_ip"),
                        data.get("connection_ip")
                    ]))),
                )
            ],
        )

    def _normalize_os(self, data: dict) -> OS:
        return OS(
            name=data.get("os_version"),
            version=f"{data.get('major_version', '')}.{data.get('minor_version', '')}",
            kernel=data.get("kernel_version"),
        )

    def _normalize_hardware(self, data: dict) -> Hardware:
        return Hardware(
            manufacturer=data.get("system_manufacturer"),
            model=data.get("system_product_name"),
            bios=dict(
                manufacturer=data.get("bios_manufacturer"),
                version=data.get("bios_version"),
                release_date=None
            ),
            cpus=CPU(
                signature=data.get("cpu_signature")
            ),
            memory_mb=0,
            disks=list()
        )

    def _normalize_software(self, data: dict) -> Software:
        return Software(
            packages=list(),
            agents=[
                Agent(
                    name=self.SOURCE_QUALIFIER,
                    version=data.get("agent_version"),
                    status=data.get("status"),
                    last_seen=get_datetime(data.get("last_seen")),
                    local_time=get_datetime(data.get("agent_local_time")),
                )
            ]
        )

    def _normalize_security(self, data: dict) -> Security:
        policy_data = data.get("policies", list())
        policy_data.extend(data.get("device_policies", dict()).values())
        return Security(
            vulnerabilities=list(),
            policies=_build_policy_dtos(policy_data)
        )

    def _normalize_cloud(self, data: dict) -> Cloud:
        return Cloud(
            provider=data.get("service_provider"),
            account_id=data.get("service_provider_account_id"),
            tags=_build_tag_dtos(tag_data=data.get("tags", list())),
            zone=data.get("zone_group"),
            security_groups=list(),
            region=None,
            vpc_id=None,
            subnet_id=None,
        )

    def _normalize_accounts(self, data: dict) -> List[Account]:
        return list()

    def _normalize_timestamps(self, data: dict) -> Timestamps:
        return Timestamps(
            created=None,
            modified=get_datetime(data.get("modified_timestamp")),
            first_seen=get_datetime(data.get("first_seen")),
            last_seen=get_datetime(data.get("last_seen"))
        )

    def _normalize_extra(self, data: dict) -> dict:
        return dict(
            cid=data.get("cid"),
            reduced_functionality_mode=data.get("reduced_functionality_mode"),
            agent_load_flags=data.get("agent_load_flags"),
            config_id_base=data.get("config_id_base"),
            config_id_build=data.get("config_id_build"),
            config_id_platform=data.get("config_id_platform"),
            product_type_desc=data.get("product_type_desc"),
            chassis_type=data.get("chassis_type"),
            chassis_type_desc=data.get("chassis_type_desc"),
            meta=data.get("meta")
        )


def _build_policy_dtos(policy_data: List[Dict]) -> List[SecurityPolicy]:
    policy_dtos = list()
    policy_ids = set()
    for policy in policy_data:
        policy_id = policy.get("policy_id")
        if policy_id not in policy_ids:
            policy_ids.add(policy_id)
            policy_dtos.append(SecurityPolicy(
                type=policy.get("policy_type"),
                id=policy_id,
                applied=policy.get("applied"),
                applied_date=get_datetime(policy.get("applied_date")),
                assigned_date=get_datetime(policy.get("assigned_date"))
            ))
    return list(policy_dtos)


def _build_tag_dtos(tag_data: list) -> List[Tag]:
    tag_dtos = list()
    for tag in tag_data:
        tag_dtos.append(Tag(id=tag))
    return tag_dtos


def _normalize_mac_address(mac: Optional[str]) -> Optional[str]:
    return mac.replace("-", ":").lower() if mac else None
