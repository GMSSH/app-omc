<template>
  <container-layout :title="$t('时区设置')">
    <div class="swap">
      <div class="swap-container">
        <div class="swap-container-title">
          {{ $t('时区设置') }}
        </div>
        <n-space align="center" style="margin-bottom: 20px">
          <n-input
            v-model:value="formState.date"
            disabled
            style="width: 310px"
            type="text"
          />
          <n-button type="primary" :disabled="loading" @click="onSave(1)">
            {{ $t('同步') }}
          </n-button>
        </n-space>
        <n-space align="center" style="margin-bottom: 20px">
          <n-select
            v-model:value="formState.zone"
            :options="zone_list"
            style="width: 100px"
            @change="handleChange"
          />
          <n-select
            v-model:value="formState.area"
            :options="area_list"
            style="width: 200px"
          />

          <n-button type="primary" :disabled="loading" @click="onSave(2)">
            {{ $t('确定') }}
          </n-button>
        </n-space>
        <div class="swap-container-str">
          {{ $t('若时区设置不正确，可能导致服务器时间"不准确"！') }}
        </div>
        <div class="swap-container-str">
          {{ $t('北京时间(CST +0800)，请选择Asia/Shanghai') }}
        </div>
      </div>
    </div>
  </container-layout>
</template>
<script lang="ts" setup>
  import { onActivated, reactive, ref } from 'vue';
  import { linuxGetSyncDateApi, linuxGetZoneApi, linuxSetZoneApi } from '@/api';
  import naiveui from '@/utils/naiveui';
  import ContainerLayout from '@/layout/ContainerLayout.vue';

  const formState = reactive({
    date: '',
    area: '',
    zone: '',
  });
  const area_list = ref<any>([]);
  const zone_list = ref<any>([]);
  const getLoad = async () => {
    area_list.value = [];
    zone_list.value = [];
    const res = await linuxGetZoneApi();
    const data = res.data;
    formState.date = data.zone.date;
    formState.area = data.zone.area;
    formState.zone = data.zone.zone;
    area_list.value = data['zone']['area_list'][data.zone.zone]?.map(
      (item: any) => ({
        label: item,
        value: item,
      })
    );
    zone_list.value = data['zone']['zone_list']?.map((item: any) => ({
      label: item,
      value: item,
    }));
  };
  onActivated(() => {
    getLoad();
  });
  const loading = ref(false);
  const onSave = (val: any) => {
    loading.value = true;
    if (val == 2) {
      linuxSetZoneApi({
        zone: formState['zone'],
        area: formState['area'],
      })
        .then((res) => {
          naiveui.message.success(res.msg);
          getLoad();
        })
        .finally(() => {
          loading.value = false;
        });
    } else {
      linuxGetSyncDateApi(formState['zone'], formState['area'])
        .then((res) => {
          naiveui.message.success(res.msg);
          getLoad();
        })
        .finally(() => {
          loading.value = false;
        });
    }
  };
  const handleChange = (val: any) => {
    linuxGetZoneApi(val).then((res) => {
      area_list.value = [];
      const data = res.data;
      area_list.value = data['zone']['area_list']?.map((item: any) => ({
        label: item,
        value: item,
      }));
      formState.area = area_list.value[0].value;
    });
  };
</script>

<style lang="scss" scoped>
  .swap {
    padding: 30px;
    background: var(--jm-accent-1);
    color: var(--jm-accent-7);
    &-container {
      &-title {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
      }

      &-str {
        @extend .store-dot-str;
        color: var(--jm-accent-5);
      }
    }
  }
</style>
