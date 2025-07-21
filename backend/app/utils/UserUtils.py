# -*- coding:utf-8 -*-
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List

from loguru import logger

from app.consts import UserConst, Settings
from app.utils import helpers


class _UserFileLine:
    """ """

    def __init__(self, line: str) -> None:
        """ """
        self._line = line

    def format(self, owner: "UserAuthFileUtils", disable=None) -> Dict:
        """
        USER_AUTH_FILE Details of the document
        sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
        sshd ->                                           username
        x ->                                              Store the encrypted user password, and store the real encrypted user password in /etc/shadow
        74 ->                                             User identification number
        74 ->                                             Group identification number
        Privilege-separated SSH ->                        Annotation description
        /var/empty/sshd ->                                Home directory: This is the user's starting working directory
        /sbin/nologin ->                                  The user's shell, /sbin/nologin/, will have nologin environment by default.
        """
        g_info = owner.read_group_dict()
        columns = ["username", "encrypted", "uid", "gid", "des", "wd"]
        contents = self._line.split(":")
        user_item = owner.read_item(contents[0])
        info = dict()
        for k, v in zip(columns, contents):
            info[k] = v
            if k == "gid":
                info["g_name"] = g_info.get(v, "unknown")

        content = Path(contents[-1]).name
        info["is_login"] = "0" if content in UserConst.NOLOGIN_FLAGS else "1"
        info["disable"] = disable or user_item.get("disable", "0")
        return info


class UserAuthFileUtils:
    """ """

    file = UserConst.USER_DEACTIVATE_RECORD_FILE

    def __init__(self) -> None:
        """ """
        file_dir = os.path.dirname(self.file)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        if not os.path.isfile(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

    def read(self, format_spec=""):
        """ """
        user_list = []
        user_name = {}
        uname_info = self.read_uname_dict()
        try:
            for line in self.read_iter():
                name = line.split(":")[0]
                if name in UserConst.ROOT_USER_FLAGS:
                    continue
                res = _UserFileLine(line.strip()).format(self)
                user_name[name] = res
                user_list.append(res)
        except Exception as e:
            logger.error(e)
            return user_list
        else:
            if not uname_info:
                return user_list
            diff_keys = uname_info.keys() - user_name.keys()
            if len(diff_keys) <= 0:
                return user_list
            user_list.extend(uname_info[k] for k in diff_keys if uname_info[k].get("delete") != "1")
            return user_list

    def read_list(self, format_spec=""):
        """ """
        user_list = []
        user_name = {}
        try:
            for line in self.read_iter():
                name = line.split(":")[0]
                # if name in UserConst.ROOT_USER_FLAGS:
                #     continue
                res = _UserFileLine(line.strip()).format(self, disable="0")
                user_name[name] = res
                # 更新缓存disable
                # 更新缓存deleted_at
                data = {"username": res.get("username")}
                data["create_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data["update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data["delete"] = "0"
                data["gid"] = res.get("gid")
                data["des"] = res.get("des")
                data["disable"] = "0"
                data["is_login"] = res.get("is_login")
                self.update_dict(data)
                user_list.append(res)
        except Exception as e:
            logger.error(e)
            return user_list
        else:
            return user_list

    def _read_iter(self, file: str) -> Generator:
        try:
            with open(file, "r") as f:
                """ """
                yield from f.readlines()
        except Exception as e:
            logger.error(e)
            yield from []

    def read_iter(self) -> Generator:
        """ """
        yield from self._read_iter(UserConst.USER_AUTH_FILE)

    def read_group_iter(self) -> Generator:
        """ """
        yield from self._read_iter(UserConst.USER_GROUP_FILE)

    def read_group_dict(self):
        """ """
        group_dic = {}
        for line in self.read_group_iter():
            line: str = line.strip()
            g_name, _, gid, _ = line.split(":")
            group_dic[gid] = g_name
        return group_dic

    def read_json(self) -> List[Dict[str, Any]]:
        """ """
        try:
            with open(self.file, "r") as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(e)
            return []

    def read_uname_dict(self):
        """ """
        o_data = self.read_json()
        return {item["username"]: item for item in o_data if item.get("username")} if o_data else None

    def write_json(self, data: Any):
        """ """
        with open(self.file, "w") as f:
            json.dump(data, f)

    def load_json(self) -> Any:
        """ """
        return self.read_json()

    def sync_user_file(self):
        """ """
        source_users = self.read_list()
        # TODO: Whether to consider adding the disabled feature
        # file_users = self.load_json()
        self.write_json(source_users)

    def update_dict(self, data: Dict[str, Any]):
        """ """
        o_data = self.read_json()
        if not o_data:
            o_data.append(data)
            self.write_json(o_data)
            return
        uname = data.get("username")

        unames = [x["username"] for x in o_data if x.get("username")]
        if uname not in unames:
            o_data.append(data)
            self.write_json(o_data)
            return

        def update(info: dict):
            """ """
            if info["username"] == uname:
                data.pop("create_time")
                for k, v in data.items():
                    info[k] = v
            return info

        n_data = list(map(update, filter(lambda x: bool(x), o_data)))
        self.write_json(n_data)

    def read_value(self, uname, k: str, default: Any = False) -> bool:
        """ """
        o_data = self.read_json()
        if not o_data:
            return default or False
        for item in o_data:
            if item["username"] == uname:
                return item[k]
        return default or False

    def read_item(self, uname):
        """ """
        if o_data := self.read_json():
            return next((item for item in o_data if item["username"] == uname), {})
        else:
            return {}

    def remove_item(self, uname):
        """ """
        o_data = self.read_json()

        def remove(item: dict):
            """ """
            return item["username"] != uname

        data = list(filter(remove, o_data))
        self.write_json(data)

    def get_group_name(self, gid):
        """ """
        for line in self.read_group_iter():
            g_name, _, gid, _ = line.split(":")
            if gid == gid:
                return g_name

    def create_user_root_dir(self, uname: str):
        """ """
        u_root = Settings.GMSSH_PATH
        if not os.path.exists(u_root):
            os.makedirs(u_root)
        return u_root

    def query_group_by_user(self, uname: str):
        """ """
        infos = self.read_list()
        for item in infos:
            """ """
            if item.get("username") == uname:
                return item.get("g_name")

    def query_gid_by_user(self, uname: str):
        """ """
        infos = self.read_list()
        for item in infos:
            """ """
            if item.get("username") == uname:
                return item.get("gid")

    def fetch_all_group_by(self):
        """ """
        infos = self.read_list()
        g_dic = defaultdict(list)
        for item in infos:
            """ """
            g_dic[item["g_name"]].append(item)


class UserSudoersUtils:
    """ """

    file = UserConst.SUDOERS_FILE
    template = "%{}	ALL=(ALL)	NOPASSWD: ALL"
    group_flag = "wheel.+NOPASSWD:.+ALL$"
    pattern1 = "%{}	ALL=(ALL) 	ALL"
    pattern2 = "{}	ALL=(ALL) 	ALL"

    def __init__(self) -> None:
        """ """

    def read(self) -> str:
        """ """
        with open(self.file, "r") as f:
            return f.read()

    def read_lines(self):
        """ """
        with open(self.file, "r") as f:
            yield from f.readlines()

    def has_item(self, group: str):
        """ """
        content = self.read()
        item = self.pattern1.format(group)
        item2 = self.pattern2.format(group)
        item1 = self.template.format(group)

        return item1 in content or item in content or item2 in content

    def do_sudoers_item(self, group: str) -> str:
        """ """
        return self.template.format(group)

    def add_item(self, item):
        """ """
        content = self.read()
        if item in content:
            return

        # 新增
        new_content = ""
        line_tag = self.group_flag
        markers = False
        for line in content.splitlines():
            """ """
            new_content += f"{line}\n"
            if re.search(line_tag, line):
                markers = True
                new_content += f"{item}\n"
        if not markers:
            new_content += f"{item}\n"

        self.write(new_content)

    def write(self, content):
        """ """
        with open(self.file, "w") as f:
            f.write(content)

    def update_item(self, old_item, new_item):
        """ """
        content = self.read()
        content = content.replace(old_item, new_item)
        self.write(content)

    def delete_item(self, item):
        """ """
        new_content = ""
        for line in self.read_lines():
            """ """
            if item in line:
                continue
            new_content += f"{line}"

        self.write(new_content)

    def is_exists(self, item) -> bool:
        """ """
        content = self.read()
        return item in content


# TODO : 用户执行命令管理
# 自定义命令执行sh，所有用户的执行命令均通过自定义的sh
# 自定义sh用来处理用户的管理，可以在自定义sh添加管理的逻辑
class UserCommandUtils:
    """ """

    content = """ 
#!/bin/bash
while getopts "a:b:" opt; do
 case $opt in
    p) a_value="$OPTARG" ;;
    a) b_value="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2 ;;
  esac
done

echo "$a_value" | sudo -S $b_value
"""
    file = "/usr/local/bin/custom-command"

    def __init__(self) -> None:
        """ """
        # Initialize the command
        # self.init_bash()
        # self.init_chmod()

    def chown(self, owner, group):
        """ """
        if not os.path.exists(self.file):
            return

        output = helpers.exec_shell_raise(f"chown -R {owner}:{group} {self.file}")
        return output

    def init_bash(self):
        """ """
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                f.write(self.content)

    def init_chmod(self):
        """ """
        output = helpers.exec_shell_raise(f"chmod 777 {self.file}")
        return output
