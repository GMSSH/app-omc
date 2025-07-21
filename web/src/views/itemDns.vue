<template>
  <container-layout :title="$t('DNS设置')">
    <div class="container">
      <n-form
        ref="formRef"
        :label-width="87"
        :model="formState"
        label-placement="left"
        :rules="rules"
      >
        <n-form-item :label="$t('主要DNS')" path="dns1">
          <n-input
            v-model:value="formState.dns1"
            clearable
            placeholder=""
            style="width: 300px"
          />
        </n-form-item>
        <n-form-item :label="$t('备用DNS')" path="dns2">
          <n-input
            v-model:value="formState.dns2"
            clearable
            placeholder=""
            style="width: 300px"
          />
        </n-form-item>
        <n-form-item label=" ">
          <n-button
            style="width: 72px"
            type="primary"
            :disabled="loading"
            @click="onSave"
          >
            {{ $t('保存') }}
          </n-button>
          <n-button
            :color="useRootElementCssVariable('jm-accent-3')"
            style="width: 72px; margin-left: 10px"
            :disabled="loading"
            @click="onTest"
          >
            {{ $t('测试') }}
          </n-button>
        </n-form-item>
      </n-form>
      <div class="container-str">
        {{
          $t(
            '设置后将在选择若DNS设置错误，会导致您的服务器无法解析域名，即无法通过服务器访问域名!'
          )
        }}
      </div>
      <div class="container-str">
        {{
          $t(
            '请在保存之前先点击测试按钮以测试您设置的DNS是否有效!目录下新建redis_cache目录并赋予redis权限!'
          )
        }}
      </div>
    </div>
  </container-layout>
</template>
<script lang="ts" setup>
  import { onActivated, reactive, ref } from 'vue';
  import { useRootElementCssVariable } from '@/utils';
  import ContainerLayout from '@/layout/ContainerLayout.vue';
  import { linuxGetDnsApi, linuxSetDnsApi, linuxTestDnsApi } from '@/api';
  import naiveui from '@/utils/naiveui';

  const loading = ref(false);
  const formRef = ref();
  const formState = reactive({
    dns1: '',
    dns2: '',
  });
  const validatorDns = (_, value: string) => {
    if (!value) {
      return new Error('dns不能为空');
    } else if (
      !/^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$/.test(
        value
      )
    ) {
      return new Error('请输入正确的dns');
    }
    return true;
  };
  const rules = {
    dns1: [
      {
        required: true,
        validator: validatorDns,
        trigger: ['blur'],
      },
    ],
    dns2: [
      {
        required: true,
        validator: validatorDns,
        trigger: ['blur'],
      },
    ],
  };
  const getLoad = async () => {
    const res = await linuxGetDnsApi();
    const dns = res.data.dns;
    formState['dns1'] = dns.dns1;
    formState['dns2'] = dns.dns2;
  };
  onActivated(() => {
    getLoad();
    formRef.value?.restoreValidation();
  });
  const onSave = () => {
    formRef.value?.validate((errors: any) => {
      if (!errors) {
        loading.value = true;
        linuxSetDnsApi(formState)
          .then((res) => {
            naiveui.message.success(res.msg);
          })
          .finally(() => {
            loading.value = false;
          });
      }
    });
  };
  const onTest = () => {
    formRef.value?.validate((errors: any) => {
      if (!errors) {
        loading.value = true;
        linuxTestDnsApi(formState)
          .then((res) => {
            naiveui.message.success(res.msg);
          })
          .finally(() => {
            loading.value = false;
          });
      }
    });
  };
</script>

<style lang="scss" scoped>
  .container {
    border-radius: 4px;
    background: var(--jm-accent-1);
    padding: 30px 15px;
    &-str {
      @extend .store-dot-str;
      color: var(--jm-accent-5);
      height: auto;
      margin-top: 0;
      padding-top: 10px;
      white-space: normal;
      &::before {
        top: 16px;
        transform: none;
      }
    }
  }
</style>
