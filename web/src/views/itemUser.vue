<template>
  <container-layout :title="$t('用户管理')">
    <div class="user">
      <div class="user-head">
        <svg-icon
          icon="icon-yonghuliebiao"
          color="var(--jm-accent-7)"
          font-size="24"
        />
        <div class="user-head-text">
          <p>{{ $t('用户列表') }}</p>
          <p>{{ $t('在列表中管理用户账号权限') }}</p>
        </div>

        <n-button
          :color="useRootElementCssVariable('jm-accent-3')"
          @click="groupVisibly = true"
        >
          {{ $t('用户组设置') }}
        </n-button>
        <n-button
          style="margin-left: 10px"
          :color="useRootElementCssVariable('jm-accent-3')"
          @click="addVisibly = true"
        >
          {{ $t('添加用户') }}
        </n-button>
      </div>
      <n-data-table
        :columns="columns"
        :data="data"
        :max-height="windowHeight - 260"
        class="user-table"
        scroll-x="600"
        size="small"
      />
    </div>
  </container-layout>

  <add-user-modal v-model:visibly="addVisibly" @on-update="getList" />
  <password-modal
    v-model:visibly="pwdVisibly"
    :user-info="userInfo"
    @on-update="getList"
  />
  <user-group-modal v-model:visibly="groupVisibly" @on-update="getList" />
  <edit-user-modal
    v-model:visibly="editVisibly"
    :user-info="userInfo"
    @on-update="getList"
  />
</template>

<script lang="ts" setup>
  import { h, onActivated, ref } from 'vue';
  import naiveui from '@/utils/naiveui';
  import { NButton, NSwitch } from 'naive-ui';
  import ShowOrEditRender from '@/render/showOrEditRender.vue';
  import AddUserModal from '@/modal/addUserModal.vue';
  import EditUserModal from '@/modal/editUserModal.vue';
  import PasswordModal from '@/modal/passwordModal.vue';
  import UserGroupModal from '@/modal/userGroupModal.vue';
  import DeleteOrRecover from '@/render/deleteOrRecover.vue';
  import PermanentlyDelete from '@/render/permDelete.vue';

  import Edit from '@/render/edit.vue';
  import ChangePassword from '@/render/changePassword.vue';
  import { SysUser } from '@/api/type';
  import { useI18n } from 'vue-i18n';
  import { useApp } from '@/hooks/useApp';
  import {
    allowSysUserApi,
    changeSysUserDesApi,
    deactivateSysUserApi,
    delSysUserApi,
    getSysUserListApi,
  } from '@/api';
  import ContainerLayout from '@/layout/ContainerLayout.vue';
  import { useRootElementCssVariable } from '@/utils';
  const i18n = useI18n();

  const { windowHeight } = useApp();
  onActivated(() => {
    getList();
  });
  const addVisibly = ref(false);
  const editVisibly = ref(false);
  const pwdVisibly = ref(false);
  const groupVisibly = ref(false);
  const userInfo = ref<SysUser>({} as SysUser);

  const columns = [
    {
      title: i18n.t('用户名'),
      key: 'username',
      minWidth: 80,
      resizable: true,
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: i18n.t('所属组'),
      key: 'g_name',
      minWidth: 80,
      resizable: true,
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: i18n.t('是否可登录'),
      key: 'is_login',
      minWidth: 80,
      resizable: true,
      render(row: SysUser) {
        return h(
          NSwitch,
          {
            value: row.is_login == '1',
            'onUpdate:value': () => {
              forbiddenOrLoginFn(row);
            },
          }
          // {
          //   style: {
          //     color: row.is_login == '1' ? '#27B2BC' : 'rgba(255, 68, 0, 1)',
          //   },
          // },
          // {
          //   default: () => (row.is_login == '1' ? i18n.t('是') : i18n.t('否')),
          // },
        );
      },
    },
    {
      title: i18n.t('描述'),
      ellipsis: {
        tooltip: true,
      },
      key: 'des',
      minWidth: 80,
      resizable: true,
    },
    {
      title: i18n.t('状态'),
      key: 'disable',
      minWidth: 80,
      resizable: true,
      render(row: SysUser) {
        return h(
          'div',
          {},
          {
            default: () =>
              row.disable == '1' ? i18n.t('禁用') : i18n.t('正常'),
          }
        );
      },
    },
    {
      title: i18n.t('操作'),
      width: 170,
      fixed: 'right',
      render(row: SysUser) {
        return h('div', { class: 'td-control' }, [
          h(DeleteOrRecover, {
            row,
            clickFn() {
              naiveui.dialog.info({
                title: i18n.t('通知'),
                content: `${i18n.t('是否')}${row.disable == '1' ? i18n.t('恢复') : i18n.t('删除')} ${row.username}?`,
                positiveText: `${i18n.t('确定')}`,
                negativeText: `${i18n.t('取消')}`,
                class: 'dialog-warning',
                maskClosable: false,
                onPositiveClick: () => {
                  if (row.disable == '1') {
                    userInfo.value = row;
                    pwdVisibly.value = true;
                  } else {
                    deactivateSysUserApi(row.username, '1').then((res) => {
                      naiveui.message.success(res.msg);
                      getList();
                    });
                  }
                },
              });
            },
          }),
          row.disable == '1' && row.is_login == '1'
            ? h(PermanentlyDelete, {
                clickFn: () => {
                  naiveui.dialog.warning({
                    title: i18n.t('警告'),
                    content: `${i18n.t('是否彻底删除')}${row.username}?`,
                    positiveText: `${i18n.t('确定')}`,
                    negativeText: `${i18n.t('取消')}`,
                    class: 'dialog-warning',
                    maskClosable: false,
                    onPositiveClick: () => {
                      delSysUserApi(row.username).then((res) => {
                        naiveui.message.success(res.msg);
                        getList();
                      });
                    },
                  });
                },
              })
            : null,
          h(ChangePassword, {
            clickFn: () => {
              pwdVisibly.value = true;
              userInfo.value = row;
            },
          }),
          h(Edit, {
            clickFn() {
              editVisibly.value = true;
              userInfo.value = row;
            },
          }),
        ]);
      },
    },
  ];
  // 登录/禁止
  function forbiddenOrLoginFn(row: SysUser) {
    naiveui.dialog.info({
      title: i18n.t('通知'),
      content: `${i18n.t('是否')}${row.is_login == '1' ? i18n.t('禁止登录') : i18n.t('允许登录')}${row.username}?`,
      positiveText: `${i18n.t('确定')}`,
      negativeText: `${i18n.t('取消')}`,
      class: 'dialog-warning',
      maskClosable: false,
      onPositiveClick: () => {
        if (row.is_login == '1') {
          allowSysUserApi(row.username, row.is_login == '1' ? '0' : '1').then(
            (res) => {
              naiveui.message.success(res.msg);
              getList();
            }
          );
        } else {
          userInfo.value = row;
          pwdVisibly.value = true;
        }
      },
    });
  }

  const data = ref<SysUser[]>([]);
  const getList = () => {
    getSysUserListApi().then((res) => {
      data.value = res.data;
    });
  };
</script>

<style lang="scss" scoped>
  .user {
    &-head {
      padding: 0 20px;
      height: 78px;
      background: var(--jm-accent-1);
      border-radius: 4px;
      @include flex(flex-start);

      &-text {
        margin-left: 20px;
        margin-right: auto;

        p {
          margin: 0;

          &:nth-of-type(1) {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 7px;
            color: var(--jm-accent-7);
          }

          &:nth-of-type(2) {
            font-size: 12px;
            font-weight: 400;
            opacity: 0.7;
            line-height: 12px;
            color: var(--jm-accent-7);
          }
        }
      }
    }
    &-btn {
      background: var(--jm-accent-3);
      color: var(--jm-accent-7);
      --n-border: var(--jm-accent-3) !important
    ;
    }
    &-btn:nth-of-type(1) {
      margin-right: 10px;
    }
    &-table {
      margin-top: 10px;

      :deep(.td-control) {
        @include flex(flex-start);

        div {
          margin: 0 10px;
        }
      }
    }
  }
</style>
