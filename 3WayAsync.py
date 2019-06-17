#! /usr/bin/env python
from infinisdk import InfiniBox
from datetime import timedelta
import argparse
import base64
import requests
import os, sys


def args_from_cfgfile(file):
    with open('{}'.format(file)) as cfg:
        conf_file = dict(line for line in (l.split() for l in cfg) if line)
    return conf_file


def get_objects(v1_name,remote_ibox, remote_vol, rpo, interval):
    snaplist=[]
    v1 = src.volumes.get(name=v1_name)
    rep1=src.replicas.get(local_entity_name=v1.get_name())
    link = src.links.get(remote_system_name=remote_ibox)
    v1snaps = src.volumes.find(parent_id=v1.get_id())
    v2 = dst.volumes.get(name=remote_vol)
    v2snaps = dst.volumes.find(parent_id=v2.get_id())
    if rep1.get_job_state() == 'DONE':
        rep1.delete(retain_staging_area=True)
    for snap in v1snaps:
        for dsnap in v2snaps:
            if snap.get_rmr_snapshot_guid() == dsnap.get_rmr_snapshot_guid():
                snaplist.append([snap,dsnap])
    replica = src.replicas.replicate_entity_use_base( replication_type='ASYNC',entity=v1,member_mappings=None,link=link,local_snapshot=snaplist[-1][0],remote_snapshot=snaplist[-1][1])
    replica.update_rpo(timedelta(minutes=int(rpo)))
    replica.update_sync_interval(timedelta(minutes=int(interval)))


def get_args():
    """
    Supports the command-line arguments listed below.
    """
    parser = argparse.ArgumentParser(description="Resize a replicated volume that is a member of a cg.")
    parser.add_argument('-v', '--volume', nargs=1, required=True, help='The local volume name', dest='v1_name', type=str)
    parser.add_argument('-b', '--remote_vol', nargs=1, required=True, help='The local volume name', dest='v2_name', type=str)
    parser.add_argument('-c', '--configfile', nargs=1, required=True, help='Config file name')
    parser.add_argument('-r', '--rpo', nargs=1, required=True, help='RPO in minutes')
    parser.add_argument('-i', '--interval', nargs=1, required=True, help='Sync interval in minutes')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    if args.configfile:
        if os.path.isfile('{}'.format(args.configfile[0])):
            cfgargs = args_from_cfgfile(args.configfile[0])
            ibox1=cfgargs['src_ibox']
            user1=cfgargs['src_user']
            enc_pw1=cfgargs['dst_password']
            ibox2=cfgargs['dst_ibox']
            user2=cfgargs['dst_user']
            enc_pw2=cfgargs['src_password']
            v1_name = args.v1_name[0]
            v2_name = args.v2_name[0]
            rpo=args.rpo[0]
            interval=args.interval[0]
            pw1 = base64.b64decode(enc_pw1).decode("utf-8", "ignore")
            pw2 = base64.b64decode(enc_pw2).decode("utf-8", "ignore")
            src = InfiniBox(ibox1 , auth=(user1, pw1))
            src.login()
            dst = InfiniBox(ibox2 , auth=(user2, pw2))
            dst.login()
            print(args.v1_name)
            get_objects(v1_name,ibox2, v2_name, rpo, interval)
