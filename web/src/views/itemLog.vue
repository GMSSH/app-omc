<template>
  <container-layout :title="$t('系统日志')">
    <div class="log">
      <div class="log-head">
        <svg-icon
          icon="icon-rizhi"
          color="var(--jm-accent-7)"
          style="margin-left: 20px"
          font-size="24"
        />
        <div class="log-head-text">
          <p>{{ $t('系统日志') }}</p>
          <p>{{ $t('查看并管理自动生成的系统日志') }}</p>
        </div>
        <n-button
          :color="useRootElementCssVariable('jm-accent-3')"
          :focusable="false"
          style="margin-right: 30px"
          @click="onUpdate"
        >
          {{ $t('刷新') }}
        </n-button>
      </div>
      <div class="log-search">
        <n-input
          v-model:value="inputValue"
          clearable
          :placeholder="$t('搜索')"
          style="width: 150px"
          @clear="
            inputValue = '';
            page = 1;
            getList();
          "
          @keyup.enter="
            page = 1;
            getList();
          "
        >
          <template #prefix>
            <svg-icon
              color="var(--jm-accent-7)"
              icon="icon-sousuo"
              font-size="16"
            />
          </template>
        </n-input>
        <n-cascader
          v-model:value="selectValue"
          :options="options"
          children-field="children"
          clearable
          label-field="des"
          :placeholder="$t('请选择')"
          placement="bottom-end"
          show-path
          style="width: 200px"
          value-field="name"
          @update:value="onCascaderUpdate"
        />
      </div>
      <n-spin :show="loading">
        <n-data-table
          :columns="columns"
          :data="data"
          :max-height="windowHeight - 380"
          class="log-table"
          scroll-x="600"
          size="small"
        />
        <n-pagination
          v-if="data.length"
          v-model:page="page"
          v-model:page-size="pageSize"
          :item-count="pageCount"
          :page-sizes="pageSizes"
          show-size-picker
          style="margin-top: 10px"
          @update:page="getList"
          @update:page-size="
            page = 1;
            getList();
          "
        />
      </n-spin>
    </div>
  </container-layout>
</template>

<script lang="ts" setup>
  import { h, nextTick, onActivated, ref } from 'vue';
  import naiveui from '@/utils/naiveui';
  import { NButton } from 'naive-ui';
  import { SysLog } from '@/api/type';
  import { useI18n } from 'vue-i18n';
  import { useApp } from '@/hooks/useApp';
  import { useRootElementCssVariable } from '@/utils';
  import { getSysLogTypeApi, getSysLogListApi } from '@/api';
  import ContainerLayout from '@/layout/ContainerLayout.vue';

  const i18n = useI18n();
  const { windowHeight } = useApp();
  onActivated(() => {
    getList();
    getOptions();
  });
  const pageSizes = [
    {
      label: i18n.t('10 每页'),
      value: 10,
    },
    {
      label: i18n.t('20 每页'),
      value: 20,
    },
    {
      label: i18n.t('30 每页'),
      value: 30,
    },
    {
      label: i18n.t('40 每页'),
      value: 40,
    },
  ];
  const columns = [
    {
      title: i18n.t('操作类型'),
      key: 'type_des',
      minWidth: 80,
      resizable: true,
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: i18n.t('详情'),
      key: 'details',
      minWidth: 80,
      resizable: true,
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: 'IP',
      key: 'ip',
      minWidth: 80,
      resizable: true,
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: i18n.t('时间'),
      key: 'created_at',
      minWidth: 80,
      resizable: true,
      ellipsis: {
        tooltip: true,
      },
    },
  ];
  const data = ref<SysLog[]>([]);
  const onCascaderUpdate = () => {
    nextTick(() => {
      page.value = 1;
      getList();
    });
  };
  const loading = ref(false);

  const getOptions = () => {
    getSysLogTypeApi().then((res) => {
      options.value = res.data;
    });
  };

  const getList = () => {
    loading.value = true;
    let type1 = '';
    let type2: any = '';

    if (typeof selectValue.value == 'string') {
      const i = (selectValue.value as string).indexOf('_');
      if (i >= 0) {
        type1 = (selectValue.value as string).substring(0, i);
        type2 = selectValue.value;
      } else {
        type1 = selectValue.value;
      }
    }
    getSysLogListApi({
      type1,
      type2,
      search: inputValue.value,
      page: page.value,
      limit: pageSize.value,
    })
      .then((res) => {
        pageCount.value = res.data.count;
        data.value = res.data.list;
      })
      .finally(() => {
        loading.value = false;
      });
  };
  const inputValue = ref('');
  const selectValue = ref(null);
  const pageSize = ref(20);
  const page = ref(1);
  const pageCount = ref(0);
  const onUpdate = () => {
    naiveui.message.success(i18n.t('刷新成功'));
    data.value = [];
    getList();
    getOptions();
  };

  const options = ref([]);
</script>

<style lang="scss" scoped>
  .log {
    &-head {
      height: 78px;
      background: var(--jm-accent-1);
      color: var(--jm-accent-7);
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

    &-search {
      margin-top: 10px;
      height: 62px;
      background: var(--jm-accent-1);
      border-radius: 4px;
      margin-bottom: 1px;
      border-bottom: none;
      @include flex(space-between);
      padding: 0 20px;
    }

    &-table {
      :deep(.td-control) {
        @include flex(flex-start);

        div {
          width: 1px;
          height: 16px;
          background: #dddddd;
          margin: 0 10px;
        }
      }
    }
  }
</style>
