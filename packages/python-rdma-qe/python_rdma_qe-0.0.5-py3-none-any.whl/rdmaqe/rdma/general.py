#!/usr/bin/env python

"""roce.py: Module to check or configure RDMA. """

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

import os
import json
from libsan.host.cmdline import run

RDMA_BASE = '/sys/class/infiniband'
DEV_INFO_JSON = "/tmp/devinfo.json"


def is_rdma_device() -> bool:
    return os.path.exists(RDMA_BASE)


def is_opa_device() -> bool:
    """
    Check if it contains OPA device
    :return:
    True: if yes
    False: if no
    """
    if is_rdma_device():
        for _ in os.listdir("/sys/class/infiniband"):
            if "hfi" in _:
                return True
            else:
                continue

        return False


def get_ibdev():
    # return: ['mlx5_1', 'mlx5_0']
    _ibdev = []
    for dev in os.listdir(RDMA_BASE):
        _ibdev.append(dev)

    return _ibdev


def get_netdev(dev):
    """
    :param dev: ibdev, like mlx5_0
    :return: netdev, like ['mlx5_roce']
    """
    if not dev:
        return None
    _netdev = []
    _dir = '/sys/class/infiniband/{}/device/net/'.format(dev)
    for dev in os.listdir(_dir):
        _netdev.append(dev)

    return _netdev


def ibv_devinfo_2_json(dev=None, port=None):
    """
    Convert the output of utility ibv_devinfo to json
    @param dev: hca_id, like mlx5_0
    @param port: the port number, 1 is the first port
    @return:
    """
    if dev is not None and port is not None:
        _cmd = "ibv_devinfo -d " + dev + " -i " + port
    elif dev is None and port is not None:
        _cmd = "ibv_devinfo -i " + port
    elif dev is not None and port is None:
        _cmd = "ibv_devinfo -d " + dev
    else:
        _cmd = "ibv_devinfo"

    retcode, devinfo = run(_cmd, return_output=True)
    if retcode == 0:
        data = {}
        pre_hca_id_list = []
        current_hca_id = None
        current_port = None

        for line in devinfo.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('hca_id:'):
                current_hca_id = line.split('hca_id:')[1].strip()
                data[current_hca_id] = {}
            elif line.startswith('port:'):
                current_port = line.split('port:')[1].strip()
                data[current_hca_id][current_port] = {}
            else:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if current_hca_id not in pre_hca_id_list:
                    current_port = None
                    pre_hca_id_list.append(current_hca_id)
                if current_port is None:
                    data[current_hca_id][key] = value.strip()
                else:
                    data[current_hca_id][current_port][key] = value.strip()

        with open(DEV_INFO_JSON, 'w') as f:
            json.dump(data, f, indent=4)

    return retcode
