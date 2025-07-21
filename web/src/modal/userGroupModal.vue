<template>
  <modal-layout
    :show="visibly"
    @after-enter="getList"
    @after-leave="inputValue = ''"
  >
    <modal-form-layout
      :width="600"
      :title="$t('用户组')"
      :show-btn="false"
      @on-cancel="closeModal"
    >
      <div style="padding: 0 10px">
        <n-input
          v-model:value="inputValue"
          clearable
          :placeholder="$t('请输入')"
          style="margin-right: 20px; width: 500px"
          type="text"
        />
        <n-button type="primary" @click="addType">
          {{ $t('添加') }}
        </n-button>
        <n-checkbox v-model:checked="checked" style="margin-top: 5px">
          {{ $t('是否添加') }}sudoers
        </n-checkbox>
      </div>

      <n-data-table
        style="padding: 10px; width: calc(100% - 20px)"
        :columns="columns"
        :data="list"
        :max-height="250"
      />
    </modal-form-layout>
  </modal-layout>
</template>
<script lang="ts" setup>
  import naiveui from '@/utils/naiveui';
  import { h, ref } from 'vue';
  import { NButton, NSwitch } from 'naive-ui';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import modalLayout from '@/layout/ModalLayout.vue';
  import { useI18n } from 'vue-i18n';
  // import { vpnAuth } from '@/api/vpn/type.ts';
  // import { vpnEnableAuthApi } from '@/api/vpn';
  import { Igroup } from '@/api/type';
  import {
    addSysUserGroupsApi,
    delSysUserGroupsApi,
    getFetchGroupsApi,
    updateSudoersApi,
  } from '@/api';

  const i18n = useI18n();
  defineProps<{ visibly: boolean }>();
  const emit = defineEmits(['update:visibly', 'onUpdate']);
  const checked = ref(false);

  const columns = [
    {
      title: i18n.t('名称'),
      key: 'label',
    },
    {
      title: 'sudoers',
      key: 'is_sudoers',
      minWidth: 80,
      resizable: true,
      render(row: Igroup) {
        return h(NSwitch, {
          value: row.is_sudoers,
          'on-update:value': (checked: boolean) => {
            row.is_sudoers = checked;
            naiveui.dialog.info({
              title: `${row.is_sudoers ? i18n.t('开启') : i18n.t('关闭')}`,
              content: `${i18n.t('是否')}${row.is_sudoers ? i18n.t('开启') : i18n.t('关闭')}【${row.label}】sudoers？`,
              positiveText: `${i18n.t('确定')}`,
              negativeText: `${i18n.t('取消')}`,
              class: 'dialog-warning',
              maskClosable: false,
              onPositiveClick: () => {
                updateSudoersApi({
                  g_name: row.label,
                  is_sudoers: row.is_sudoers ? '1' : '0',
                })
                  .then((res) => {
                    naiveui.message.success(res.msg);
                  })
                  .finally(getList);
              },
              onNegativeClick: getList,
              onAfterLeave: getList,
            });
          },
        });
      },
    },
    {
      width: 100,
      title: i18n.t('操作'),
      key: 'gid',
      render(row: Igroup) {
        return h(
          NButton,
          {
            text: true,
            size: 'small',
            color: 'rgb(232, 17, 35)',
            focusable: false,
            onClick: () => onDelType(row),
          },
          { default: () => i18n.t('删除') }
        );
      },
    },
  ];
  const inputValue = ref('');
  const onDelType = (row: Igroup) => {
    naiveui.dialog.warning({
      title: i18n.t('警告'),
      content: `${i18n.t('是否删除')}${row.label}?`,
      positiveText: `${i18n.t('确定')}`,
      negativeText: `${i18n.t('取消')}`,
      class: 'dialog-warning',
      maskClosable: false,
      onPositiveClick: () => {
        delSysUserGroupsApi(row.label).then((res) => {
          naiveui.message.success(res.msg);
          getList();
        });
      },
    });
  };
  const addType = () => {
    addSysUserGroupsApi({
      g_name: inputValue.value,
      is_sudoers: checked.value ? '1' : '0',
    }).then((res) => {
      naiveui.message.success(res.msg);
      inputValue.value = '';
      getList();
    });
  };
  const closeModal = () => {
    emit('update:visibly', false);
  };
  const list = ref<Igroup[]>([]);
  const getList = () => {
    getFetchGroupsApi().then((res) => {
      list.value = res.data;
    });
  };
</script>
<style lang="scss" scoped></style>
