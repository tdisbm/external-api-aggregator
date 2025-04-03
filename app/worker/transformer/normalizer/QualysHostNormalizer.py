from datetime import datetime
from typing import List

from app.components.dto.Account import Account
from app.components.dto.Agent import Agent
from app.components.dto.CPU import CPU
from app.components.dto.Cloud import Cloud
from app.components.dto.CloudSecurityGroup import CloudSecurityGroup
from app.components.dto.Tag import Tag
from app.components.dto.Volume import Volume
from app.components.dto.Hardware import Hardware
from app.components.dto.Identity import Identity
from app.components.dto.Metadata import Metadata
from app.components.dto.Network import Network
from app.components.dto.NetworkInterface import NetworkInterface
from app.components.dto.OS import OS
from app.components.dto.OpenPort import OpenPort
from app.components.dto.Security import Security
from app.components.dto.Software import Software
from app.components.dto.SoftwarePackage import SoftwarePackage
from app.components.dto.Timestamp import Timestamps
from app.components.dto.Vulnerability import Vulnerability
from app.utils.data_access_utils import get_list, get_datetime, get_headless_list, get_decimal, get_index_safe
from app.worker.transformer.normalizer.HostNormalizer import HostNormalizer


class QualysHostNormalizer(HostNormalizer):
    SOURCE_QUALIFIER = "qualys"

    def _normalize_metadata(self, data: dict) -> Metadata:
        return Metadata(
            source=self.SOURCE_QUALIFIER,
            collection_time=datetime.now(),
        )

    def _normalize_identity(self, data: dict) -> Identity:
        cloud_info = _get_cloud_data(data=data)
        return Identity(
            hostname=data.get("name"),
            fqdn=data.get("fqdn"),
            instance_id=str(cloud_info.get("instanceId")),
            external_ids=[
                f"{self.SOURCE_QUALIFIER}:{str(data.get('_id'))}"
            ]
        )

    def _normalize_network(self, data: dict) -> Network:
        cloud_info = _get_cloud_data(data=data)
        network_interfaces_data = get_headless_list(data.get("networkInterface", list()))
        open_ports_data = get_headless_list(data.get("openPort", list()))
        return Network(
            interfaces=_build_network_interfaces(network_interfaces_data=network_interfaces_data),
            open_ports=_build_open_port_dtos(open_ports_data=open_ports_data),
            public_ips=[cloud_info.get("publicIpAddress")] if cloud_info.get("publicIpAddress") else [],
            dns_names=list(set(filter(None, [
                data.get("dnsHostName", None),
                data.get("fqdn", None),
                cloud_info.get("publicDnsName", None),
                cloud_info.get("privateDnsName", None)
            ]))),
        )

    def _normalize_os(self, data: dict) -> OS:
        return OS(
            name=data.get("os"),
            boot_time=get_datetime(data.get("lastSystemBoot", None))
        )

    def _normalize_hardware(self, data: dict) -> Hardware:
        disk_data = get_headless_list(data.get("volume", list()))
        cpus_data = get_headless_list(data.get("processor", list()))
        return Hardware(
            manufacturer=data.get("manufacturer", None),
            model=data.get("model", None),
            memory_mb=data.get("totalMemory", None),
            volumes=_build_volumes_dtos(volumes_data=disk_data),
            cpu=_build_cpu_dto(cpus_data=cpus_data),
            bios=_get_bios_data(description=data.get("biosDescription")),
        )

    def _normalize_software(self, data: dict) -> Software:
        agent_info = data.get("agentInfo", dict())
        software_package_data = get_headless_list(data.get("software", list()))
        return Software(
            packages=_build_software_package_dtos(software_package_data=software_package_data),
            agents=[
                Agent(
                    name=self.SOURCE_QUALIFIER,
                    external_id=agent_info.get("agentId"),
                    version=agent_info.get("agentVersion"),
                    status=agent_info.get("status"),
                    remote_address=agent_info.get("connectedFrom"),
                    location=dict(
                        name=agent_info.get("location"),
                        latiture=agent_info.get("locationGeoLatitude"),
                        longitude=agent_info.get("locationGeoLongtitude"),
                    ),
                    last_seen=get_datetime(agent_info.get("lastCheckedIn")),
                    extra=dict(
                        platform=agent_info.get("platform"),
                        chirp_status=agent_info.get("chirpStatus"),
                        config=agent_info.get("agentConfiguration"),
                        activation_key=agent_info.get("activationKey"),
                        activation_module=agent_info.get("activatedModule"),
                        manifest_version=agent_info.get("manifestVersion"),
                    )
                )
            ]
        )

    def _normalize_security(self, data: dict) -> Security:
        vulnerability_data = get_headless_list(data.get("vuln", list()))
        return Security(
            policies=list(),
            vulnerabilities=_build_vulnerability_dtos(vulnerabilities_data=vulnerability_data),
            last_vulnerability_scan=get_datetime(data.get("lastVulnScan")),
            last_compliance_scan=get_datetime(data.get("lastComplianceScan")),
        )

    def _normalize_cloud(self, data: dict) -> Cloud:
        cloud_info = _get_cloud_data(data=data)
        tags_data = get_headless_list(data.get("tags", list()))
        return Cloud(
            provider=data.get("cloudProvider"),
            account_id=cloud_info.get("accountId"),
            region=cloud_info.get("region"),
            zone=cloud_info.get("availabilityZone"),
            vpc_id=cloud_info.get("vpcId"),
            subnet_id=cloud_info.get("subnetId"),
            tags=_build_tags_dtos(tags_data=tags_data),
            security_groups=[
                CloudSecurityGroup(
                    id=cloud_info.get("groupId"),
                    name=cloud_info.get("groupName")
                )
            ],
        )

    def _normalize_accounts(self, data: dict) -> List[Account]:
        accounts = list()
        for account in get_headless_list(data.get("account", list())):
            accounts.append(
                Account(
                    username=account.get("username")
                )
            )
        return accounts

    def _normalize_timestamps(self, data: dict) -> Timestamps:
        cloud_info = _get_cloud_data(data=data)
        agent_info = data.get("agentInfo", dict())
        return Timestamps(
            created=get_datetime(data.get("created")),
            modified=get_datetime(data.get("modified")),
            first_seen=get_datetime(cloud_info.get("firstDiscovered")),
            last_seen=get_datetime(agent_info.get("lastCheckedIn"))
        )

    def _normalize_extra(self, data: dict) -> dict:
        return dict(
            qwebHostId=data.get("qwebHostId"),
            trackingMethod=data.get("trackingMethod"),
            isDockerHost=data.get("isDockerHost"),
            networkGuid=data.get("networkGuid"),
        )


def _build_network_interfaces(network_interfaces_data: List[dict]) -> List[NetworkInterface]:
    network_interfaces_dtos = list()
    for network_interface in network_interfaces_data:
        address = network_interface.get("address", None)
        network_interfaces_dtos.append(NetworkInterface(
            name=network_interface.get("interfaceName"),
            mac=network_interface.get("macAddress"),
            ips=[address] if address else [],
            gateway=network_interface.get("gatewayAddress")
        ))
    return network_interfaces_dtos


def _build_open_port_dtos(open_ports_data: List[dict]) -> List[OpenPort]:
    open_ports_dtos = list()
    for open_port in open_ports_data:
        open_ports_dtos.append(OpenPort(
            port=str(open_port.get("port")),
            protocol=open_port.get("protocol"),
            service=open_port.get("serviceName")
        ))
    return open_ports_dtos


def _build_cpu_dto(cpus_data: list) -> CPU:
    if not cpus_data:
        return CPU()
    if len(set(str(cpu) for cpu in cpus_data)) > 1:
        raise Exception('No way!!')
    cpu_data = cpus_data[0]
    return CPU(
        model=cpu_data.get("name"),
        speed_mhz=get_decimal(cpu_data.get("speed"))
    )


def _build_volumes_dtos(volumes_data: List[dict]) -> List[Volume]:
    volumes_dtos = list()
    for disk in volumes_data:
        volumes_dtos.append(Volume(
            name=disk.get("name"),
            size_bytes=get_decimal(disk.get("size")),
            free_bytes=get_decimal(disk.get("free"))
        ))
    return volumes_dtos


def _build_software_package_dtos(software_package_data: List[dict]) -> List[SoftwarePackage]:
    software_package_dtos = list()
    for software_package in software_package_data:
        software_package_dtos.append(SoftwarePackage(
            name=software_package.get("name"),
            version=software_package.get("version")
        ))
    return software_package_dtos


def _build_vulnerability_dtos(vulnerabilities_data: List[dict]) -> List[Vulnerability]:
    vulnerability_dtos = list()
    for vulnerability in vulnerabilities_data:
        vulnerability_dtos.append(Vulnerability(
            id=str(vulnerability.get("qid")),
            instance_id=str(get_decimal(vulnerability.get("hostInstanceVulnId"))),
            first_seen=get_datetime(vulnerability.get("firstFound")),
            last_seen=get_datetime(vulnerability.get("lastFound")),
        ))
    return vulnerability_dtos


def _build_tags_dtos(tags_data: List[dict]) -> List[Tag]:
    tags_dtos = list()
    for tag in tags_data:
        tags_dtos.append(Tag(
            id=str(get_decimal(tag.get("id"))),
            name=tag.get("name")
        ))
    return tags_dtos


def _get_cloud_data(data: dict, cloud_info_type: str = "Ec2AssetSourceSimple") -> dict:
    # Yes, it's pretty greedy
    source_infos = get_list(data.get("sourceInfo", list()))
    for source_info in source_infos:
        if cloud_info_type in source_info:
            return source_info[cloud_info_type]
    return dict()


def _get_bios_data(description: str) -> dict:
    description_parts = description.split(" ")
    return dict(
        manufacturer=get_index_safe(description_parts, 0),
        version=get_index_safe(description_parts, 1),
        release_date=get_datetime(get_index_safe(description_parts, 2)),
        extra=description_parts[3:],
    )
