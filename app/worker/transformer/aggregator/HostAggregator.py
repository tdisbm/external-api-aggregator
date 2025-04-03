from datetime import datetime
from uuid import uuid4

from app.components.transformer.ModelAggregator import ModelAggregator
from app.components.dto.CPU import CPU
from app.components.dto.Cloud import Cloud
from app.components.dto.Hardware import Hardware
from app.components.dto.Host import Host
from app.components.dto.Identity import Identity
from app.components.dto.Metadata import Metadata
from app.components.dto.Network import Network
from app.components.dto.OS import OS
from app.components.dto.Security import Security
from app.components.dto.Software import Software
from app.components.dto.Timestamp import Timestamps
from app.utils.data_utils import merge_dicts_priority
from app.utils.date_utils import latest, earliest
from app.worker.transformer.aggregator.NetworkInterfaceAggregator import NetworkInterfaceAggregator


class HostAggregator(ModelAggregator):
    def merge(self, model1: Host, model2: Host):
        newest, oldest = _get_models_by_last_seen(host1=model1, host2=model2)
        merge_id = f"merge-{uuid4()}"
        new_identity = Identity(
            hostname=newest.identity.hostname or oldest.identity.hostname,
            instance_id=newest.identity.instance_id or oldest.identity.instance_id,
            external_ids=list(set(newest.identity.external_ids + oldest.identity.external_ids)),
            fqdn=newest.identity.fqdn or oldest.identity.fqdn,
            serial_number=newest.identity.serial_number or oldest.identity.serial_number,
        )
        new_metadata = Metadata(
            source=merge_id,
            collection_time=datetime.now(),
        )
        new_network = Network(
            public_ips=list(set(newest.network.public_ips + oldest.network.public_ips)),
            dns_names=list(set(newest.network.dns_names + oldest.network.dns_names)),
            open_ports=list(set(newest.network.open_ports + oldest.network.open_ports)),
            interfaces=NetworkInterfaceAggregator().aggregate(
                models=newest.network.interfaces + oldest.network.interfaces
            ),
        )
        new_os = OS(
            name=newest.os.name or oldest.os.name,
            version=newest.os.version or oldest.os.version,
            kernel=newest.os.kernel or oldest.os.kernel,
            boot_time=latest(newest.os.boot_time, oldest.os.boot_time),
        )
        new_hardware = Hardware(
            manufacturer=newest.hardware.manufacturer or oldest.hardware.manufacturer,
            model=newest.hardware.model or oldest.hardware.model,
            bios=merge_dicts_priority(newest.hardware.bios, oldest.hardware.bios),
            cpu=CPU(**merge_dicts_priority(newest.hardware.cpu.model_dump(), oldest.hardware.cpu.model_dump())),
            memory_mb=newest.hardware.memory_mb or oldest.hardware.memory_mb,
            volumes=list(set(newest.hardware.volumes + oldest.hardware.volumes)),
        )
        new_software = Software(
            packages=list(set(newest.software.packages + oldest.software.packages)),
            agents=list(set(newest.software.agents + oldest.software.agents)),
        )
        new_security = Security(
            vulnerabilities=list(set(newest.security.vulnerabilities + oldest.security.vulnerabilities)),
            policies=list(set(newest.security.policies + oldest.security.policies)),
            last_vulnerability_scan=newest.security.last_vulnerability_scan or oldest.security.last_vulnerability_scan,
            last_compliance_scan=newest.security.last_compliance_scan or oldest.security.last_compliance_scan
        )
        new_cloud = Cloud(
            provider=newest.cloud.provider or oldest.cloud.provider,
            account_id=newest.cloud.account_id or oldest.cloud.account_id,
            region=newest.cloud.region or oldest.cloud.region,
            zone=newest.cloud.zone or oldest.cloud.zone,
            vpc_id=newest.cloud.vpc_id or oldest.cloud.vpc_id,
            subnet_id=newest.cloud.subnet_id or oldest.cloud.subnet_id,
            security_groups=list(set(newest.cloud.security_groups + oldest.cloud.security_groups)),
            tags=list(set(newest.cloud.tags + oldest.cloud.tags)),
        )
        new_accounts = list(set(newest.accounts + oldest.accounts))
        new_timestamps = Timestamps(
            created=earliest(model1.timestamps.created, oldest.timestamps.created),
            modified=latest(model1.timestamps.modified, oldest.timestamps.modified),
            first_seen=earliest(model1.timestamps.first_seen, oldest.timestamps.first_seen),
            last_seen=latest(model1.timestamps.last_seen, oldest.timestamps.last_seen),
        )
        return Host(
            metadata=new_metadata,
            identity=new_identity,
            network=new_network,
            os=new_os,
            hardware=new_hardware,
            software=new_software,
            security=new_security,
            cloud=new_cloud,
            accounts=new_accounts,
            timestamps=new_timestamps,
            extras={
                **model1.extras,
                **oldest.extras
            }
        )


def _get_models_by_last_seen(host1: Host, host2: Host):
    if host1.timestamps.last_seen > host2.timestamps.last_seen:
        return host2, host1
    return host1, host2
