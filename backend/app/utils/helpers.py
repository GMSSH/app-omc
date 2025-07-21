import os
import re
import socket
import stat
import subprocess
import time
from typing import Callable

from app.consts import UserConst
from loguru import logger
from simplejrpc.client import GmSyncRpcClient
from simplejrpc.exceptions import RPCException
from simplejrpc.i18n import T as i18n


class GMResException(RPCException):
    """ """


class FormValidateError(RPCException):
    """ """


def exec_shell_raise(
    cmd_string,
    timeout=None,
    shell=True,
    cwd=None,
    env=None,
    user=None,
    error_msg="CONST_STATUS_EXPECTATION_FAILED",
):
    """ """
    res, err = exec_shell(cmd_string, timeout, shell, cwd, env, user)
    if err != "":
        # 解决sss数据库问题
        if "Removing cache files in /var/lib/sss/db should fix the issue" in err:
            exec_shell(
                "sudo systemctl stop sssd && sudo rm -rf /var/lib/sss/db/* && sudo systemctl start sssd && sudo systemctl status sssd"
            )
            return ""
        logger.error(err)
        raise GMResException(i18n.translate(error_msg))
    return res


def get_pre_exec_fn(run_user):
    """
    @name 获取指定执行用户预处理函数
    @param run_user<string> 运行用户
    @return 预处理函数
    """
    import pwd

    pid = pwd.getpwnam(run_user)
    uid = pid.pw_uid
    gid = pid.pw_gid

    def _exec_rn():
        os.setgid(gid)
        os.setuid(uid)

    return _exec_rn


def md5(strings):
    """
    @name 生成MD5
    @param strings 要被处理的字符串
    @return string(32)
    """
    if type(strings) != bytes:
        strings = strings.encode()
    import hashlib

    m = hashlib.md5()
    m.update(strings)
    return m.hexdigest()


def get_error_info():
    """ """
    import traceback

    return traceback.format_exc()


def exec_shell(cmd_string, timeout=None, shell=True, cwd=None, env=None, user=None):
    """
    @name 执行命令
    @param cmd_string 命令 [必传]
    @param timeout 超时时间
    @param shell 是否通过shell运行
    @param cwd 进入的目录
    @param env 环境变量
    @param user 执行用户名
    @return 命令执行结果
    """
    import subprocess
    import tempfile

    pre_exec_fn = None
    tmp_dir = "/dev/shm"
    if user:
        pre_exec_fn = get_pre_exec_fn(user)
        tmp_dir = "/tmp"
    try:
        rx = md5(cmd_string.encode("utf-8"))
        success_f = tempfile.SpooledTemporaryFile(
            max_size=4096,
            mode="wb+",
            suffix="_success",
            prefix=f"b_tex_{rx}",
            dir=tmp_dir,
        )
        error_f = tempfile.SpooledTemporaryFile(
            max_size=4096,
            mode="wb+",
            suffix="_error",
            prefix=f"b_tex_{rx}",
            dir=tmp_dir,
        )
        sub = subprocess.Popen(
            cmd_string,
            close_fds=True,
            shell=shell,
            bufsize=128,
            stdout=success_f,
            stderr=error_f,
            cwd=cwd,
            env=env,
            preexec_fn=pre_exec_fn,
        )
        if timeout:
            s = 0
            d = 0.01
            while sub.poll() is None:
                time.sleep(d)
                s += d
                if s >= timeout:
                    if not error_f.closed:
                        error_f.close()
                    if not success_f.closed:
                        success_f.close()
                    return "", "Timed out"
        else:
            sub.wait()

        error_f.seek(0)
        success_f.seek(0)
        a = success_f.read()
        e = error_f.read()
        if not error_f.closed:
            error_f.close()
        if not success_f.closed:
            success_f.close()
    except Exception as e:
        logger.error(e)
        return "", get_error_info()
    try:
        # 编码修正
        if type(a) == bytes:
            a = a.decode("utf-8")
        if type(e) == bytes:
            e = e.decode("utf-8")
    except Exception as e:
        logger.error(e)
        a = str(a)
        e = str(e)

    return a, e


def check_sudo_permission():
    """ """
    try:
        subprocess.check_output('sudo -n echo "Sudo permission granted"', shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(e)
        return False
    return True


def get_env_user():
    """Read the user in the system environment variable"""

    output, _ = exec_shell("whoami")
    return os.environ.get("USER") or output


def wrapper_raise_root_except(fn: Callable):
    """处理一些特殊的需要权限的操作，当无权限操作时候需要显示的提醒用户时候使用，
    如果当无需提醒用户权限操作的时候则不需要考虑使用该方法，因会针对无权限操作
    抛出PermissionError异常，该异常可以用来做针对用户权限不同的响应提示(建议最好
    配合用户的信息来做，如果需要做RBAC等功能的话也是基于该功能之上的操作，
    这里拒绝策略中原生的优先级最高)

    """

    def inner(*args, **kwargs) -> None:
        """ """
        user = get_env_user()
        if user not in UserConst.DEFAULT_INIT_USER:
            raise GMResException(i18n.translate("CONST_STATUS_AUTHORITATIVE_FAILED_INFO"))
        return fn(*args, **kwargs)

    return inner


def wrapper_root_executer(fn: Callable):
    """ """

    def inner(*args, **kwargs) -> None:
        """ """
        user = get_env_user()
        if user not in UserConst.DEFAULT_INIT_USER:
            return
        return fn(*args, **kwargs)

    return inner


def add_localhost_mapping():
    """
    动态获取主机名并将其与 127.0.0.1 绑定到 /etc/hosts 文件
    """
    hosts_file = "/etc/hosts"
    ip = "127.0.0.1"
    hostname = socket.gethostname()
    # 检查是否有权限修改文件
    # if not os.access(hosts_file, os.W_OK):
    #     raise PermissionError("需要管理员权限才能修改 /etc/hosts 文件，请使用 sudo 运行脚本。")

    with open(hosts_file, "r") as f:
        lines = f.readlines()
    mapping_exists = any(line.strip().startswith(f"{ip} {hostname}") for line in lines)

    if mapping_exists:
        return
    with open(hosts_file, "a") as f:
        f.write(f"{ip} {hostname}\n")


def xor_strings(s1: str, s2: str) -> str:
    """将字符串转换为字节序列

    :param s1: 字符串1
    :param s2: 字符串2
    """
    b1 = bytes(s1, "utf-8")
    b2 = bytes(s2, "utf-8")
    bxor = bytes([b1[i] ^ b2[i] for i in range(len(b1))])

    return bxor.decode("utf-8")


def _write_file(file_mode, filename, user):
    """ """
    if file_mode:
        exec_shell(f"chmod {file_mode} {filename}")
    if user:
        exec_shell(f"chown {user}:{user} {filename}")
    return True


def write_file(filename, s_body, mode="w+", file_mode="", user="", encoding="utf-8") -> bool:
    """
    写入文件内容
    @filename 文件名
    @s_body 欲写入的内容
    return bool 若文件不存在则尝试自动创建
    """
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    try:
        with open(filename, mode, encoding=encoding) as fp:
            fp.write(s_body)
        return _write_file(file_mode, filename, user)
    except Exception as e:
        logger.error(e)
        try:
            with open(filename, mode, encoding=encoding) as fp:
                fp.write(s_body)
            return _write_file(file_mode, filename, user)
        except Exception as e:
            logger.error(e)
            return False


def write_json(filename, data, auto_create=False, auth_create_type="{}") -> bool:
    """
    写入 json 文件
    :param auth_create_type:
    :param auto_create:
    :param filename:
    :param data:
    :return:
    """
    import json

    if auto_create and not os.path.exists(filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        write_file(filename, auth_create_type)
    return write_file(filename, json.dumps(data))


def read_file(filename, mode="r") -> str:
    """
    读取文件内容
    @filename 文件名
    return string(bin) 若文件不存在，则返回False
    """
    import os

    if not os.path.exists(filename):
        return ""
    fp = None
    try:
        fp = open(filename, mode)
        f_body = fp.read()
    except Exception as e:
        logger.error(e)
        try:
            fp = open(filename, mode, encoding="utf-8", errors="ignore")
            f_body = fp.read()
        except Exception as e:
            logger.error(e)
            fp = open(filename, mode, encoding="GBK", errors="ignore")
            f_body = fp.read()
    finally:
        if fp and not fp.closed:
            fp.close()
    return f_body


def read_json(filename, auto_create=False, auth_create_type="{}"):
    """
    读取 json 文件
    :param auth_create_type:
    :param auto_create:
    :param filename:
    :return:
    """
    import json

    if auto_create and not os.path.exists(filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        write_file(filename, auth_create_type)
    contents = read_file(filename)
    return [] if contents == "" else json.loads(contents)


def centos_is78():
    """
    判断是否为CentOS 7/8
    :return:
    """
    if os.path.exists("/etc/redhat-release"):
        version = read_file("/etc/redhat-release")
        if isinstance(version, str) and (version.find(" 7.") != -1 or version.find(" 8.") != -1):
            return True
    return False


def format_date(format_str="%Y-%m-%d %H:%M:%S", times=None) -> str:
    """Get the current"""
    if not times:
        times = int(time.time())
    time_local = time.localtime(times)
    return time.strftime(format_str, time_local)


def xss_encode2(text):
    """ """
    try:
        from cgi import html

        return html.escape(text, quote=True)
    except Exception as e:
        logger.error(e)
        return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def get_sys_swap():
    """ """
    try:
        res = subprocess.check_output("free -m|grep Swap", shell=True)
        return res.decode()
    except subprocess.CalledProcessError as e:
        logger.error(e)
        return ""


def check_is_system_catalogue(catalogue) -> bool:
    """
    检查目录是否是系统的敏感目录，需要传入文件或者目录
    """

    system_catalogue = [
        "/boot",
        "/bin",
        "/sbin",
        "/lib",
        "/lib64",
        "/etc",
        "/var",
        "/mnt",
        "/media",
        "/srv",
        "/proc",
        "/sys",
        "/dev",
        "/root",
        "/tmp",
        "/run",
        "/usr",
        "/.__gmssh",
    ]
    return any(catalogue.startswith(i) for i in system_catalogue)


def set_path_permissions(root_path, expected_mode=0o755):
    # 获取当前权限
    current_mode = stat.S_IMODE(os.stat(root_path).st_mode)
    if current_mode != expected_mode:
        try:
            os.chmod(root_path, expected_mode)
        except PermissionError:
            return False
    return True


def restore_xor(s1, sxor) -> str:
    """还原异或操作

    :param s1: 字符串1
    :param sxor: 字符串2
    """
    # 将字符串转换为字节序列
    b1 = bytes(s1, "utf-8")
    bxor = bytes(sxor, "utf-8")
    brestored = bytes([bxor[i] ^ b1[i] for i in range(len(bxor))])

    return brestored.decode("utf-8")


def is_number(s) -> bool:
    # DNS regular expression
    return bool(re.fullmatch(r"[-+]?\d+(\.\d+)?", s))


def validate_dns_string(dns_str: str) -> bool:
    """ """
    dns_ls = dns_str.split(".")
    dns_isdigit = (is_number(x) for x in dns_ls)
    if all(dns_isdigit):
        """ """
        if len(dns_ls) != 4 or int(dns_ls[0]) <= 0:
            return False
        return all((int(x) <= 255 and int(x) >= 0 for x in dns_ls))
    else:
        return True


# 重要操作日志记录
def omc_log_report(plugin_name, plugin_name_des, fn_name, fn_name_des, data, o_name):
    data = {
        "plugin_name": plugin_name,
        "plugin_name_des": plugin_name_des,
        "fn_name": fn_name,
        "fn_name_des": fn_name_des,
        "data": data,
        "o_name": o_name,
    }
    req = GmSyncRpcClient()
    res = req.send_request("log_report", data)
    return res.to_dict().get("result").get("code") == 200


def kill_process(pid, signal=15):
    """ """
    exec_shell(f"kill -{signal} {pid}")
