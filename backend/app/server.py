"""
@文件        :__init__.py
@说明        :omc是Operation & Maintenance Center 的首字母缩写
@时间        :2025/06/06 18:58:40
@作者        :xiaozheng
@邮箱        :13124421402@163.com
@版本        :1.0.0
"""

from app.consts import Settings
from app.schemas import (
    DnsForm,
    MemdiskForm,
    SshForm,
    SwapForm,
    SysLogsForm,
    TimeZoneForm,
    UserForm,
)
from app.services.DnsServices import DnsServices
from app.services.MemdiskServices import MemdiskServices
from app.services.SwapServices import SwapServices
from app.services.SyslogsServices import SysLogsServices
from app.services.TimeZoneServices import TimezoneServices
from app.services.UserServices import UserService
from app.utils.SysUtils import ssh_obs
from simplejrpc.app import ServerApplication
from simplejrpc.i18n import T as i18n
from simplejrpc.response import jsonify

app = ServerApplication(
    Settings.OMC_SOCKET_FILE_PATH, i18n_dir=Settings.OMC_I18N_DIR_PATH, config_path=Settings.OMC_CONFIG_FILE_PATH
)


@app.route(name="ping")
async def ping():
    """ """
    return jsonify(data="pong", msg="OK")


############################################### 用户模块 ###############################################
user_service = UserService()


@app.route(name="fetch_user_list")
async def fetch_user_list(**kwargs):
    """获取系统用户列表"""
    res = user_service.fetch_user_list(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="fetch_groups")
async def fetch_groups(**kwargs):
    """获取系统用户组"""
    res = user_service.fetch_groups(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="change_passwd", form=UserForm.UserChangePasswdForm)
async def change_passwd(**kwargs):
    """修改用户密码"""
    res = user_service.change_passwd(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="add_user", form=UserForm.UserAddUserForm)
async def add_user(**kwargs):
    """新增系统用户"""
    res = user_service.add_user(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="user_allow", form=UserForm.UserAllowUpdateForm)
async def user_allow(**kwargs):
    """用户登录状态变更"""
    res = user_service.user_allow(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="user_deactivate", form=UserForm.UserDeactivateForm)
async def user_deactivate(**kwargs):
    """用户禁用状态变更"""
    res = user_service.user_deactivate(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


# todo::接口弃用
# @app.route(name="user_del",form=UserForm.UserNameForm)
# async def user_del(**kwargs):
#     """ 用户删除 """
#     res = user_service.user_del(kwargs)
#     return jsonify(data=res, msg=i18n.translate("STATUS_OK"))

# todo::接口弃用
# @app.route(name="user_remove",form=UserForm.UserNameForm)
# async def user_remove(**kwargs):
#     """ 用户移除 """
#     res = user_service.user_remove(kwargs)
#     return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="update_user_des", form=UserForm.UserUpdateDesc)
async def update_user_des(**kwargs):
    """更新用户描述"""
    res = user_service.update_user_des(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="add_group", form=UserForm.UserGroupForm)
async def add_group(**kwargs):
    """新增用户组"""
    res = user_service.add_group(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="del_group", form=UserForm.UserDelGroupForm)
async def del_group(**kwargs):
    """删除用户组"""
    res = user_service.del_group(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


# todo::接口弃用
# @app.route(name="check_user_login",form=UserForm.UserCheckLoginForm)
# async def check_user_login(**kwargs):
#     """ 检查用户的状态 """
#     res = user_service.check_user_login(kwargs)
#     return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="update_sudoers", form=UserForm.UserDeleteGroupSudoersForm)
async def update_sudoers(**kwargs):
    """变更sudoers组"""
    res = user_service.update_sudoers(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


# todo::接口弃用
# @app.route(name="query_role_options")
# async def query_role_options(**kwargs):
#     """ 获取角色选项 """
#     res = user_service.query_role_options(kwargs)
#     return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="update_user", form=UserForm.UserUpdateForm)
async def update_user(**kwargs):
    """更新用户信息"""
    res = user_service.update_user(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


# todo::接口弃用
# @app.route(name="access_save",form=UserForm.UserAccessSaveForm)
# async def access_save(**kwargs):
#     """ 保存sudo会话 """
#     res = user_service.access_save(kwargs)
#     return jsonify(data=res, msg=i18n.translate("STATUS_OK"))
#
# todo::接口弃用
# @app.route(name="has_sudo_access")
# async def has_sudo_access(**kwargs):
#     """ 是否有sudo命令 """
#     res = user_service.has_sudo_access(kwargs)
#     return jsonify(data=res, msg=i18n.translate("STATUS_OK"))
#
# todo::接口弃用
# @app.route(name="access_status")
# async def access_status(**kwargs):
#     """ 读取用户的会话信息 """
#     res = user_service.access_status(kwargs)
#     return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


############################################### SSH模块 ###############################################


ssh_service = ssh_obs()


@app.route(name="get_info")
async def get_info(**kwargs):
    """获取ssh信息"""
    res = ssh_service.get_info(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="set_port", form=SshForm.SshSetPortForm)
async def set_port(**kwargs):
    """修改ssh端口"""
    res = ssh_service.set_port(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="set_sshkey", form=SshForm.SshSetSshKeyForm)
async def set_sshkey(**kwargs):
    """设置ssh的key"""
    res = ssh_service.set_sshkey(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="stop_key")
async def stop_key(**kwargs):
    """关闭sshkey登陆"""
    res = ssh_service.stop_key(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="get_key")
async def get_key(**kwargs):
    """获取ssh key"""
    res = ssh_service.get_key(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="get_ssh_list")
async def get_ssh_list(**kwargs):
    """获取ssh 登陆日志列表"""
    res = ssh_service.get_ssh_list(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="generate_certificate", form=SshForm.SshCaKeyForm)
async def generate_certificate(**kwargs):
    """生成客户端证书"""
    res = ssh_service.generate_certificate(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="list_certificates")
async def list_certificates(**kwargs):
    """获取已签发的证书信息"""
    res = ssh_service.list_certificates(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="enable_ca_key")
async def enable_ca_key(**kwargs):
    """生成 CA 密钥"""
    res = ssh_service.enable_ca_key(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="disable_ca_key")
async def disable_ca_key(**kwargs):
    """禁用 CA 认证"""
    res = ssh_service.disable_ca_key(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="revoke_certificate", form=SshForm.SshSetCaKeyForm)
async def revoke_certificate(**kwargs):
    """吊销证书"""
    res = ssh_service.revoke_certificate(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="get_ca_key", form=SshForm.SshSetCaKeyForm)
async def get_ca_key(**kwargs):
    """获取证书内容"""
    res = ssh_service.get_ca_key(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="get_ca_status")
async def get_ca_status(**kwargs):
    """获取证书开关"""
    res = ssh_service.get_ca_status(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


############################################### 日志模块 ###############################################

log_service = SysLogsServices()


@app.route(name="logs", form=SysLogsForm.LogsForm)
async def logs(**kwargs):
    """获取日志内容"""
    res = log_service.logs(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="logs_type")
async def logs_type(**kwargs):
    """获取日志类型"""
    res = log_service.logs_type(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


############################################### DNS模块 ###############################################

dns_service = DnsServices()


@app.route(name="get_dns")
async def get_dns(**kwargs):
    """获取dns"""
    res = dns_service.get_dns(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="set_dns", form=DnsForm.SetDnsForm)
async def set_dns(**kwargs):
    """设置dns"""
    res = dns_service.set_dns(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="test_dns", form=DnsForm.TestDnsForm)
async def test_dns(**kwargs):
    """测试DNS"""
    res = dns_service.test_dns(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


############################################### Swap/虚拟内存模块 ###############################################

swap_service = SwapServices()


@app.route(name="get_swap")
async def get_swap(**kwargs):
    """获取SWAP信息"""
    res = swap_service.get_swap(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="set_swap", form=SwapForm.SetSwapForm)
async def set_swap(**kwargs):
    """设置虚拟内存"""
    res = swap_service.set_swap(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


############################################### 时区模块 ###############################################

timezone_service = TimezoneServices()


@app.route(name="get_zone")
async def get_zone(**kwargs):
    """获取时区"""
    res = timezone_service.get_zone(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="get_sync_date", form=TimeZoneForm.SynCZoneForm)
async def get_sync_date(**kwargs):
    """同步时间"""
    res = timezone_service.get_sync_date(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="set_zone", form=TimeZoneForm.SetZoneForm)
async def set_zone(**kwargs):
    """设置时区"""
    res = timezone_service.set_zone(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


############################################### 内存盘模块 ###############################################

memdisk_service = MemdiskServices()


@app.route(name="get_memory_disk")
async def get_memory_disk(**kwargs):
    """获取内存盘大小"""
    res = memdisk_service.get_memory_disk(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="set_memory_disk", form=MemdiskForm.SetMemoryDiskForm)
async def set_memory_disk(**kwargs):
    """添加内存盘"""
    res = memdisk_service.set_memory_disk(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))


@app.route(name="del_memory_disk", form=MemdiskForm.DelMemoryDiskForm)
async def del_memory_disk(**kwargs):
    """删除内存盘"""
    res = memdisk_service.del_memory_disk(kwargs)
    return jsonify(data=res, msg=i18n.translate("STATUS_OK"))
