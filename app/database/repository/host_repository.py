from typing import List

from pymongo import UpdateOne

from app.components.dto.Host import Host
from app.database.connection import collections, Session


def get_hosts(skip: int, limit: int) -> List[Host]:
    return list(
        Host(**host)
        for host in collections.hosts.find().skip(skip).limit(limit)
    )


def get_host(hostname_or_instance_id: str) -> Host:
    return Host(**collections.hosts.find_one({
        "$or": [
            {"identity.hostname": hostname_or_instance_id},
            {"identity.instance_id": hostname_or_instance_id}
        ]
    }))


def get_hosts_audit_date_ordered(skip: int, limit: int, newest_first: bool = True) -> List[Host]:
    hosts = (collections.hosts.find()
             .sort("timestamps.last_seen", -1 if newest_first else 1)
             .skip(skip).limit(limit))
    return list(Host(**host) for host in hosts)


def get_hosts_vuln_count_ordered(skip: int, limit: int, vulnerable_first: bool = True) -> List[Host]:
    hosts = collections.hosts.aggregate([
        {"$addFields": {"vuln_length": {"$size": "$security.vulnerabilities"}}},
        {"$sort": {"vuln_length": -1 if vulnerable_first else 1}},
        {"$skip": skip},
        {"$limit": limit}
    ])
    return list(
        Host(**host)
        for host in hosts
    )


def get_hosts_last_vuln_date_scan_ordered(skip: int, limit: int, newest_first: bool = True) -> List[Host]:
    hosts = (collections.hosts.find()
             .sort("security.last_vulnerability_scan", -1 if newest_first else 1)
             .skip(skip).limit(limit))
    return list(Host(**host) for host in hosts)


def get_hosts_by_agent(agent_name: str, skip: int, limit: int) -> List[Host]:
    hosts = collections.hosts.find({"identity.external_ids": {"$regex": agent_name}})
    return list(Host(**host) for host in hosts.skip(skip).limit(limit))


def update_hosts(hosts: List[Host], session: Session = None):
    if hosts:
        collections.hosts.bulk_write(
            session=session,
            requests=list(
                UpdateOne(
                    filter={"identity.instance_id": host.identity.instance_id},
                    update={"$set": host.model_dump()},
                    upsert=True
                )
                for host in hosts
            )
        )


def delete_hosts(hosts: List[Host], session: Session = None):
    collections.hosts.delete_many(
        session=session,
        filter={
            "$or": [
                {"identity.instance_id": {"$in": list(host.identity.instance_id for host in hosts)}},
                {"identity.hostname": {"$in": list(host.identity.hostname for host in hosts)}}
            ]
        }
    )


def find_similar_hosts(hosts: List[Host]):
    return list(Host(**host) for host in collections.hosts.find({
        "$or": [
            {"identity.instance_id": {"$in": list(host.identity.instance_id for host in hosts)}},
            {"identity.hostname": {"$in": list(host.identity.hostname for host in hosts)}}
        ]
    }))
