/* 系统用户 */
// 公共返回结构
export type Result<T = any> = {
  code: number;
  msg: string;
  data: T;
  meta: any;
};

export type SysUser = {
  username: string; // 系统用户名
  encrypted: string; // 系统加密的规则
  uid: string; // 用户标识
  gid: string; // 用户组标识
  g_name: string; // 用户组名
  des: string; // 描述信息
  wd: string; // 工作目录
  is_login: string; // 是否授权登录
  disable: string; // 是否禁用
  role_name: string;
  role_id: string;
};
/* 系统用户列表返回值类型 */
export type SysUserRes = Result<SysUser[]>;
export type Igroup = {
  label: string;
  value: string;
  is_sudoers: boolean;
};

export type UserRole = {
  created_at: string;
  deleted_at: string;
  id: string;
  name: string;
  note: string;
  operator: string;
  updated_at: string;
};

export type SshInfo = {
  port: string;
  rsa_auth: string;
  pubkey_auth: string;
  password_auth: string;
  root_is_login: string;
  root_login_type: string;
  root_login_type_list: any;
  ssh_key_list: string[];
  key_path: string;
  type: string;
};
/* ssh信息返回值类型 */
export type SshRes = Result<SshInfo>;

export type SshLog = {
  address: string;
  port: string;
  time: string;
  user: string;
  status: number;
};
export type SysCert = {
  key_id: string;
  user_principal: string[];
  validity_period: string;
  user_key_path: string;
  certificate_path: string;
  remark: string;
  status: boolean;
  valid_from: string;
  valid_to: string;
  serial_number: string;
};
export type DiskItem = {
  name: string;
  type: string;
  total: string;
  used: string;
  free: string;
  percent: string;
  percent_num: number;
  mount: string;
};
/* 磁盘信息返回值类型 */
export type DiskInfoRes = Result<DiskItem[]>;
export type SystemItem = {
  name: string;
  cpu: string;
  mem: string;
  disk: string;
  os: string;
  run_days: number;
  sys_time: string;
};
/* 系统信息返回值类型 */
export type SystemInfoRes = Result<SystemItem>; // linux获取dns
export type LinuxDnsRes = Result<{
  dns: {
    dns1: string;
    dns2: string;
  };
  zone: {
    area: string;
    area_list: any;
    date: string;
    zone: string;
    zone_list: any;
  };
  swap: {
    free: number;
    size: number;
    total: number;
    used: number;
  };
  memory_disk: any;
  status: boolean;
}>; /* 服务器信息 */
/* 进程 */
export type Process = {
  cpu: number;
  io: number;
  mem: number;
  name: string;
  pid: number;
  fid?: number;
  status: string;
  ps: string;
  status_zh: string;
  cpu_color: number;
  mem_color: number;
  io_color: number;
  cmdline: string;
  sub_process_count: number;
  children: Process[];
};
/* 进程返回值类型 */
export type ProcessRes = Result<{
  count: {
    cpu: string;
    io: string;
    mem: string;
  };
  process_list: Process[];
}>;
/* 负载状态 */
export type SystemLoad = {
  cpu_loads: {
    one: number;
    five: number;
    fifteen: number;
    cpu_load: number;
  };
  cpu_times: {
    user: number;
    nice: number;
    system: number;
    idle: number;
    iowait: number;
    irq: number;
    softirq: number;
    steal: number;
    guest: number;
    guest_nice: number;
    total_processes: number;
    active_processes: number;
  };
  cpu_monitor: {
    used: number;
    cpu_name: string;
    cpu_count: number;
    cpu_num: number;
    process_count: number;
    thread_count: number;
    cpu_now_ghz: number;
    handle: number;
    run_time: string;
    cpu_ghz: number;
    slots: number;
    l1_cache: number;
    l2_cache: number;
    l3_cache: number;
    virt: number;
  };
  mem_monitor: {
    used: number;
    mem_used: number;
    mem_free: number;
    mem_total: number;
    form_factor: string;
    slots: number;
    used_slots: number;
    mem_cache: number;
    mem_mhz: string;
  };
  io_monitor: {
    used: number;
    part_name: string;
    part_type: string;
    disk_total: number;
    disk_used: number;
    disk_free: number;
    disk_percent: number;
    system_disk: number;
    swap_file: number;
    read_kb: number;
    write_kb: number;
    speed_kb: number;
  }[];
  net_monitor: {
    net_name: string;
    ipv4: string;
    ipv6: string;
    sent_kbps: number;
    recv_kbps: number;
    speed_kbps: number;
  }[];
};
/* 负载状态返回值类型 */
export type SystemLoadRes = Result<SystemLoad>;
export type Server = {
  name: string;
  public_ip: string;
  private_ip: string;
  desktop_bg_type: string;
  desktop_bg_value: string;
  desktop_bg_fit: string;
}; /* 启动项列表返回值类型 */
/* 启动项 */
export type Startup = {
  file: string;
  name: string;
  server_name: string;
  cmd: string;
  hash_id: string;
};
export type startupRes = Result<{ items: Startup[] }>;
/* 系统用户列表返回值类型 */
/* 系统日志 */
export type SysLog = {
  id: number;
  type1: string;
  type1_des: string;
  type2: string;
  type2_des: string;
  details: string;
  ip: string;
  created_at: string;
};
export type SysLogRes = Result<{
  count: number;
  list: SysLog[];
}>;
/* sessions用户列表返回值类型 */
/* sessions用户 */
export type SysSessions = {
  sid: string;
  host: string;
  ip: string;
  last_time: string;
  mfa: string;
  current_user: number;
};
interface Permission {
  system: {
    is_open: boolean;
    way: 1;
  };
  app: {
    name: string;
    icon: string;
    is_open: boolean;
    way: 1;
    title: string;
  }[];
}
export type SysSessionsRes = Result<SysSessions[]>;
export type Permissions = Result<Permission>;
export type MfaItem = {
  alias: string;
  uuid: string;
};
