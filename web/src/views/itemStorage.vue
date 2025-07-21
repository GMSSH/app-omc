<template>
  <container-layout :title="$t('内存盘')">
    <div class="container">
      <div class="main">
        <div class="actionbar">
          <n-space align="center" style="margin-bottom: 14px">
            <select-directory v-model:value="path" />
            <n-input-number
              v-model:value="storage"
              clearable
              :placeholder="$t('请输入')"
              :min="0"
              :max="10240000"
              :precision="0"
              :show-button="false"
            >
              <template #suffix>
                <div style="color: var(--jm-accent-7); font-size: 12px">MB</div>
              </template>
            </n-input-number>
            <n-button type="primary" @click="onAdd">
              {{ $t('添加内存盘') }}
            </n-button>
          </n-space>
        </div>

        <n-data-table
          :columns="columns"
          :data="List"
          size="small"
          style="margin-bottom: 10px"
        />
        <div class="main-str">
          <div class="main-str-list">
            {{
              $t(
                '内存盘具有物理磁盘无法比拟的读写速度，但只能用于保存临时数据!'
              )
            }}
          </div>
          <div class="main-str-list">
            {{
              $t(
                '内存盘是直接将部分物理内存挂载为磁盘，请根据当前服务器内存使用情况合理安排挂载容量!'
              )
            }}
          </div>
          <div class="main-str-list">
            {{
              $t('重启服务器，或卸载内存盘后，保存在该内存盘的数据将被清空!')
            }}
          </div>
        </div>
      </div>
    </div>
  </container-layout>
</template>
<script lang="ts" setup>
  import { h, onActivated, ref } from 'vue';
  import { NButton } from 'naive-ui';
  import naiveui from '@/utils/naiveui';
  import SelectDirectory from '@/components/SelectDirectory.vue';
  import Uninstall from '@/render/uninstall.vue';
  import { useI18n } from 'vue-i18n';
  import ContainerLayout from '@/layout/ContainerLayout.vue';
  import {
    linuxDelMemoryApi,
    linuxGetMemoryApi,
    linuxSetMemoryApi,
  } from '@/api';

  const i18n = useI18n();

  const path = ref('');
  const storage = ref(0);
  const List = ref([]);
  const columns = [
    {
      title: i18n.t('目录'),
      key: 'mount_path',
      minWidth: 80,
      resizable: true,
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: i18n.t('容量'),
      key: 'mount_szie',
      minWidth: 80,
      resizable: true,
    },
    {
      title: i18n.t('已使用'),
      key: 'useed_szie',
      minWidth: 80,
      resizable: true,
    },
    {
      title: i18n.t('操作'),
      width: 100,
      render(row: any) {
        return h(Uninstall, {
          clickFn: () => onDel(row),
        });
      },
    },
  ];
  const onAdd = () => {
    if (!path.value) {
      naiveui.message.error(i18n.t('请选择目录'));
      return;
    }
    if (!storage.value) {
      naiveui.message.error(i18n.t('请输入内存'));
      return;
    }
    const params = {
      mount_path: path.value,
      mount_szie: storage.value.toString(),
    };
    linuxSetMemoryApi(params).then((res) => {
      getLoad();
      naiveui.message.success(res.msg);
      path.value = '';
      storage.value = 0;
    });
  };
  const onDel = (row: any) => {
    naiveui.dialog.warning({
      title: i18n.t('删除'),
      content: i18n.t('您确定要删除吗？'),
      positiveText: `${i18n.t('确定')}`,
      negativeText: `${i18n.t('取消')}`,
      class: 'dialog-warning',
      maskClosable: false,
      onPositiveClick: () => {
        linuxDelMemoryApi(row.mount_path).then((res) => {
          getLoad();
          naiveui.message.success(res.msg);
        });
      },
    });
  };

  const getLoad = async () => {
    const res = await linuxGetMemoryApi();
    List.value = res.data['memory_disk'];
  };
  onActivated(() => {
    getLoad();
  });
</script>

<style lang="scss" scoped>
  .container {
    .main {
      .actionbar {
        border-radius: 4px 4px 0 0;
        background: var(--jm-accent-1);
        padding: 20px;
        margin-bottom: 1px;
      }
      &-str {
        background: var(--jm-accent-1);
        padding: 20px;
        color: var(--jm-accent-5);
        &-list {
          display: flex;
          &::before {
            content: '';
            flex-shrink: 0;
            display: block;
            width: 4px;
            height: 4px;
            background: var(--jm-accent-5);
            border-radius: 50%;
            margin-right: 12px;
            transform: translateY(8px);
          }
        }
      }
    }
  }
</style>
