#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project :Omc
@File    :SysUtils.py.py
@IDE     :PyCharm
@Date    :2025/7/2 14:39
@Author  :xiaozheng
"""
import importlib
import os
import re

from app.services.SshServices import SshService
from app.utils import helpers


class UniversalLinuxSys:
    """ """

    OS_RELEASE = "/etc/os-release"
    OS_CMD = "lsb_release -a"
    CENTOS_RELEASE = "/etc/centos-release"
    KEY_MAPS = {
        "NAME": "name",
        "VERSION": "version",
        "ID": "id",
        "ID_LIKE": "id_like",
        "VERSION_ID": "v_id",
        "PRETTY_NAME": "pretty_name",
        "ANSI_COLOR": "ansi_color",
        "ANSI_VERSION": "ansi_version",
        "CPE_NAME": "cpe_name",
        "HOME_URL": "home_url",
        "CENTOS_MANTISBT_PROJECT": "CMP",
        "CENTOS_MANTISBT_PROJECT_VERSION": "CMP_V",
        "REDHAT_SUPPORT_PRODUCT": "RSP",
        "REDHAT_SUPPORT_PRODUCT_VERSION": "RSP_V",
        "Distributor ID": "id",
        "Release": "v_id",
    }

    def get_centos_release_data(self):
        """通过获取/etc/centos-release获取版本信息"""
        info = {}
        if os.path.exists(self.CENTOS_RELEASE):
            info["id"] = "centos"
            with open(self.CENTOS_RELEASE, "r", encoding="utf-8") as f:
                release_desc = f.read()
            versions = re.findall(r"(\d+(\.\d+)+)", release_desc)
            if versions:
                info["v_id"] = versions[0][0]
        return info

    def get_lsb_release_data(self):
        """通过lsb_release -a 命令 获取系统信息"""
        data = helpers.exec_shell(self.OS_CMD)[0].split("\n")
        release_info = {}
        for info in data:
            if not info:
                continue
            info_list = info.split(":")
            if len(info_list) < 2:
                continue
            key = info_list[0].strip()
            sys_key = self.KEY_MAPS.get(key, key)
            release_info[sys_key] = info_list[1].strip().lower()
        return release_info

    def get_os_release_data(self):
        """通过读取/etc/os-release文件获取系统信息
        .. note::
            返回数据举例如下
            {
                'name': 'CentOS Linux',
                'version': '7 (Core)',
                'id': 'centos',
                'id_like': 'rhel fedora',
                'v_id': '7',
                'pretty_name': 'CentOS Linux 7 (Core)',
                'ansi_color': '0;31',
                'cpe_name': 'cpe:/o:centos:centos:7',
                'home_url': 'https://www.centos.org/',
                'BUG_REPORT_URL': 'https://bugs.centos.org/',
                'CMP': 'CentOS-7',
                'CMP_V': '7',
                'RSP': 'centos',
                'RSP_V': '7',
            }
        """
        sys_info = {}
        if os.path.exists(self.OS_RELEASE):
            with open(self.OS_RELEASE, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    l_line = line.lstrip()
                    if not l_line:
                        continue
                    if l_line.startswith("#") or l_line.startswith(";"):
                        continue
                    quote_delimit = max(line.find("'", line.find("'") + 1), line.find('"', line.rfind('"')) + 1)
                    comment_delimit = line.find("#", quote_delimit)
                    line = line[:comment_delimit]
                    key, value = map(lambda x: x.strip().strip("'").strip('"'), line.split("=", 1))

                    sys_key = self.KEY_MAPS.get(key, key)
                    sys_info[sys_key] = value
        return sys_info

    def get_os_machine_info(self):
        """通过uname -m 获取系统架构信息"""
        return helpers.exec_shell("uname -m")[0].strip()

    def get_sys_info(self):
        """ """

        sys_info = self.get_os_release_data()
        if not sys_info:
            lsb_release_info = self.get_lsb_release_data()
            sys_info.update(lsb_release_info)
            if not lsb_release_info:
                centos_info = self.get_centos_release_data()
                sys_info.update(centos_info)

        sys_info["machine"] = helpers.exec_shell("uname -m")[0].strip()
        return sys_info


def ssh_obs():
    """ """
    sys_info = UniversalLinuxSys().get_sys_info()
    sys_id = sys_info.get("id").capitalize()
    sys_vid = sys_info.get("v_id", "").split(".")[0]
    class_name = f"Ssh{sys_id}{sys_vid}Service"
    try:
        module = importlib.import_module("app.services.SshServices")
        cls = getattr(module, class_name)
        return cls()  # 实例化返回
    except Exception as e:
        return SshService()
