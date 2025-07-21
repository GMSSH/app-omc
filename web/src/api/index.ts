import {
  DiskInfoRes,
  Igroup,
  LinuxDnsRes,
  MfaItem,
  ProcessRes,
  Result,
  SshLog,
  SshRes,
  SysCert,
  SysSessionsRes,
  SystemInfoRes,
  SystemLoadRes,
  SysUserRes,
  UserRole,
} from '@/api/type';
import request from '@/utils/request';
/**
 * 获取系统用户列表
 */
export const getSysUserListApi = () =>
  request<SysUserRes>(`/api/call/official/omc/fetch_user_list`);
/**
 * 获取用户组
 */
export const getFetchGroupsApi = () =>
  request<
    Result<
      {
        label: string;
        value: string;
        is_sudoers: boolean;
      }[]
    >
  >(`/api/call/official/omc/fetch_groups`);
/**
 * 删除用户组
 */
export const delSysUserGroupsApi = (g_name: string) =>
  request(`/api/call/official/omc/del_group`, { g_name });
/**
 * 添加用户组
 */
export const addSysUserGroupsApi = (data: {
  g_name: string;
  is_sudoers: string;
}) => request(`/api/call/official/omc/add_group`, data);
/**
 * 修改Sudoers
 */
export const updateSudoersApi = (data: {
  is_sudoers: string;
  g_name: string;
}) => request<Result<Igroup>>(`/api/call/official/omc/update_sudoers`, data);
/**
 * 新增系统用户
 */
export const addSysUserApi = (data: {
  username: string;
  passwd: string;
  allow: string;
  gid: string;
  role_id: number;
  des: string;
}) => request(`/api/call/official/omc/add_user`, data);
/**
 * 编辑系统用户
 */
export const editSysUserApi = (data: {
  username: string;
  gid: string;
  des: string;
}) => request(`/api/call/official/omc/update_user`, data);
/**
 * 系统用户禁用启用
 */
export const deactivateSysUserApi = (
  username: string,
  disable: string,
  passwd?: string
) =>
  request(`/api/call/official/omc/user_deactivate`, {
    username,
    disable,
    passwd,
  });
/**
 * 系统用户登录状态修改
 */
export const allowSysUserApi = (
  username: string,
  allow: string,
  passwd?: string
) =>
  request(`/api/call/official/omc/user_allow`, {
    username,
    allow,
    passwd,
  });
/**
 * 删除系统用户
 */
export const delSysUserApi = (username: string) =>
  request(`/api/call/official/omc/user_remove`, { username });
/**
 * 修改系统用户密码
 */
export const changeSysUserPasswdApi = (username: string, passwd: string) =>
  request(`/api/call/official/omc/change_passwd`, { username, passwd });
/**
 * 修改系统用户描述
 */
export const changeSysUserDesApi = (username: string, des: string) =>
  request(`/api/call/official/omc/update_user_des`, { username, des });
/**
 * 获取角色列表
 */
export const getUserRoleListApi = () =>
  request<Result<UserRole[]>>(`/api/call/official/omc/get_roles`);
/**
 * 新增角色
 */
export const addUserRoleApi = (data: {
  name: string;
  note: string;
  submenu_ids: string;
}) => request(`/api/call/official/omc/add_role`, data);
/**
 * 编辑角色
 */
export const updateUserRoleApi = (data: {
  id: string;
  name: string;
  note: string;
  submenu_ids: string;
}) => request(`/api/call/official/omc/update_role`, data);
/**
 * 获取角色菜单列表
 */
export const getRoleMenuListApi = () =>
  request(`/api/call/official/omc/get_all_menu_list`);
/**
 * 编辑角色
 */
export const getUserRoleApi = (role_id: string) =>
  request<Result<{ submenu_ids: number[] }>>(
    `/api/call/official/omc/get_filtered_policy`,
    {
      role_id,
    }
  );
/**
 * 删除角色
 */
export const delUserRoleApi = (id: string) =>
  request(`/api/call/official/omc/delete_role`, { id });
/**
 * 获取角色菜单列表
 */
export const getRoleOptionsApi = () =>
  request<Result<{ value: string; label: string }[]>>(
    `/api/call/official/omc/get_role_options`
  );

/**
 * 获取角色权限
 */
export const getRolePoliciesApi = () =>
  request(`/api/call/official/omc/get_role_policies`);

/**
 * 获取 ssh管理信息
 */
export const getSshInfoApi = () =>
  request<SshRes>(`/api/call/official/omc/get_info`);
/**
 * 获取 ssh密钥
 */
export const getSshKey = () => request(`/api/call/official/omc/get_key`);
/**
 * 获取 ssh管理登录日志
 */
export const getSshLogApi = (
  status: string,
  keywords: string,
  page: number,
  page_size: number
) =>
  request<
    Result<{
      data: SshLog[];
      total: number;
    }>
  >(`/api/call/official/omc/get_ssh_list`, {
    status,
    keywords,
    page,
    page_size,
  });
/**
 * 修改ssh端口
 */
export const setSshPort = (data: { port: string }) =>
  request<Result>(`/api/call/official/omc/set_port`, data);
/**
 * 设置ssh 的key
 */
export const setSshKey = (data: { ssh: string; type: string }) =>
  request(`/api/call/official/omc/set_sshkey`, data);
/**
 * 关闭ssh key登录
 */
export const closeSshKey = () => request(`/api/call/official/omc/stop_key`);
/**
 * 获取证书状态
 */
export const getCertStatus = () =>
  request<Result<string>>(`/api/call/official/omc/get_ca_status`);
/**
 * 关闭证书登录
 */
export const disableCert = () =>
  request(`/api/call/official/omc/disable_ca_key`);
/**
 * 打开证书登录
 */
export const enableCert = () => request(`/api/call/official/omc/enable_ca_key`);
/**
 * 获取证书列表
 */
export const getCertList = (keyWord: string) =>
  request<Result<SysCert[]>>(`/api/call/official/omc/list_certificates`, {
    keyword: keyWord,
  });
/**
 * 查看证书key
 */
export const getCertKey = (serial_number: string) =>
  request<Result<string>>(`/api/call/official/omc/get_ca_key`, {
    serial_number,
  });
/**
 * 吊销证书
 */
export const revokeCert = (serial_number: string) =>
  request<Result<string>>(`/api/call/official/omc/revoke_certificate`, {
    serial_number,
  });
/**
 * 签发或续费证书
 */
export const generateCert = (data: {
  key_id: string;
  user_principal: string;
  validity_period: string;
  user_key_path: string;
  remark: string;
}) => request(`/api/call/official/omc/generate_certificate`, data);

/**
 * 获取磁盘
 */
export const getDiskApi = () =>
  request<DiskInfoRes>(`/api/call/official/omc/disk_list`);
/**
 * 获取系统信息
 */
export const getSystemApi = () =>
  request<SystemInfoRes>(`/api/call/official/omc/des_info`);
// linux相关
export const linuxGetSwapApi = () => request(`/api/call/official/omc/get_swap`);

export const linuxSetSwapApi = (swap_size: string) =>
  request(`/api/call/official/omc/set_swap`, {
    swap_size,
  });

export const linuxGetDnsApi = () =>
  request<LinuxDnsRes>(`/api/call/official/omc/get_dns`);

export const linuxSetDnsApi = (data: { dns1: string; dns2: string }) =>
  request(`/api/call/official/omc/set_dns`, data);

export const linuxTestDnsApi = (data: { dns1: string; dns2: string }) =>
  request(`/api/call/official/omc/test_dns`, data);

export const linuxGetMemoryApi = () =>
  request(`/api/call/official/omc/get_memory_disk`);

export const linuxSetMemoryApi = (data: any) =>
  request(`/api/call/official/omc/set_memory_disk`, data);

export const linuxDelMemoryApi = (mount_path: any) =>
  request(`/api/call/official/omc/del_memory_disk`, {
    mount_path,
  });

export const linuxGetZoneApi = (zone = '') =>
  request<Result<{ zone: string }>>(`/api/call/official/omc/get_zone`, {
    zone,
  });

export const linuxSetZoneApi = (data: any) =>
  request(`/api/call/official/omc/set_zone`, data);

export const linuxGetSyncDateApi = (continent: string, city: string) =>
  request(`/api/call/official/omc/get_sync_date`, {
    continent,
    city,
  });
/**
 * 获取进程列表
 */
export const getProcessListApi = (sort: string, reverse: string) =>
  request<ProcessRes>(`/api/call/official/omc/process_list`, {
    sort,
    reverse,
  });
/**
 * 结束进程
 */
export const killProcessApi = (data: { pid: number; act: string }) =>
  request(`/api/call/official/omc/kill_process`, data);
/**
 * 修改备注
 */
export const setProcessPsApi = (data: {
  process_name: string;
  ps_body: string;
}) => request(`/api/call/official/omc/set_process_ps`, data);
/**
 * 获取负载状态
 */
export const getSystemLoadApi = () =>
  request<SystemLoadRes>(`/api/call/official/omc/load_status`);
/**
 * 释放内存
 */
export const rememoryApi = () => request(`/api/call/official/omc/rememory`);
/**
 * 日志类型列表
 */
export const getSysLogTypeApi = () =>
  request(`/api/call/official/omc/logs_type`);
/**
 * 获取系统日志列表
 */
export const getSysLogListApi = (data: {
  type1: string;
  type2: string;
  search: string;
  page: number;
  limit: number;
}) => request(`/api/call/official/omc/logs`, data);
/**
 * 清空系统日志
 */
export const delSysLogApi = () => request(`/api/call/official/omc/clear_logs`);
/**
 * 新增系统启动项
 */
export const addStartupApi = (cmd: string) =>
  request(`/api/call/official/omc/add_startup`, { cmd });
/**
 * 禁止系统启动项
 */
export const disableStartupApi = (data: {
  file: string;
  server_name: string;
  hash_id: string;
  cmd: string;
}) => request(`/api/call/official/omc/disable_startup`, data);
/**
 * 获取系统启动项
 */
export const addStartupListApi = () =>
  request(`/api/call/official/omc/startup_list`);
/**
 * 获取会话列表
 */
export const getSysSessionsListApi = () =>
  request<SysSessionsRes>(`/api/call/official/omc/sessions`);
/**
 * 注销会话
 */
export const delSysSessionsApi = (sid: string) =>
  request(`/api/call/official/omc/del_session`, { sid });

/**
 * 获取mfa绑定列表
 */
export const mfaBindListApi = () => {
  return window.$gm.request<
    Result<{ is_valid: string; alias_list: MfaItem[] }>
  >(`${window.$gm.baseURL}/api/v1/mfa/list_mfa`, {
    method: 'get',
  });
};
/**
 * 添加mfa
 */
export const addMfaApi = (data: {
  alias: string;
  existing_uuid?: string;
  existing_code?: string;
}) => {
  return window.$gm.request<
    Result<{
      alias: string;
      secret: string;
      url: string;
      uuid: string;
    }>
  >(`${window.$gm.baseURL}/api/v1/mfa/create_mfa`, {
    method: 'post',
    data,
  });
};
/**
 * 认证mfa
 */
export const authMfaApi = (data: { uuid: string; code: string }) => {
  return window.$gm.request<Result<boolean>>(
    `${window.$gm.baseURL}/api/v1/mfa/activate_mfa`,
    {
      method: 'post',
      data,
    }
  );
};
/**
 * 移除mfa
 */
export const delMfaApi = (data: { uuid: string; code: string }) => {
  return window.$gm.request<Result<boolean>>(
    `${window.$gm.baseURL}/api/v1/mfa/delete_mfa`,
    {
      method: 'post',
      data,
    }
  );
};
