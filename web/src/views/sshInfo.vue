<template>
  <div class="ssh">
    <n-form
      class="ssh-form"
      :label-width="120"
      :show-require-mark="false"
      label-placement="left"
      size="small"
    >
      <n-form-item :label="$t('SSH端口')" path="name">
        <n-input
          v-model:value="info.port"
          clearable
          placeholder=""
          style="width: 225px"
        >
          <template #suffix>
            <n-button class="changePort" text @click="changePort">
              <span style="padding: 0 4px; color: var(--jm-accent-3)">|</span
              >{{ $t('修改') }}
            </n-button>
          </template>
        </n-input>
      </n-form-item>
      <n-form-item :label="$t('ROOT登录设置')">
        <n-select
          v-model:value="info.root_login_type"
          :options="rootOptions"
          placeholder=""
          style="width: 225px"
        />
      </n-form-item>
      <n-form-item :label="$t('SSH密钥登录')">
        <n-space align="center">
          <n-switch
            v-model:value="info.pubkey_auth"
            :loading="loading"
            checked-value="yes"
            unchecked-value="no"
            @update:value="onPubKeyAuthChange"
          />
        </n-space>
      </n-form-item>
      <n-form-item :label="$t('设置密钥类型')">
        <n-select
          v-model:value="formState.type"
          :disabled="info.pubkey_auth !== 'yes'"
          :options="keyOptions"
          :placeholder="$t('设置密钥类型')"
          style="width: 225px"
          @update:value="onKeyConfirm"
        />
      </n-form-item>
      <n-form-item label=" ">
        <n-space align="center">
          <n-button
            type="primary"
            :disabled="info.pubkey_auth !== 'yes'"
            @click="chaKey"
          >
            {{ $t('查看密钥') }}
          </n-button>
          <n-button
            v-if="info.key_path"
            :color="useRootElementCssVariable('jm-accent-3')"
            @click="downloadKey"
          >
            {{ $t('下载') }}
          </n-button>
          <span style="font-size: 12px; color: var(--jm-accent-5)">{{
            $t('推荐使用密钥登录，关闭密码，安全性更高')
          }}</span>
        </n-space>
      </n-form-item>
    </n-form>
    <div class="ssh-title">
      <svg-icon icon="icon-rizhi" color="var(--jm-accent-7)" font-size="24" />
      <div class="ssh-title-left">
        <div>{{ $t('SSH登录日志') }}</div>
        <div v-if="listCount.success != 0 || listCount.failed != 0">
          {{ $t('SSH登录详情') }}（{{ $t('当前页') }}）：
          <span>{{ $t('成功') }}：{{ listCount.success }}</span> /
          <span>{{ $t('失败') }}：{{ listCount.failed }}</span>
        </div>
      </div>
      <div class="ssh-title-right">
        <n-select
          v-model:value="searchType"
          :options="options"
          style="width: 140px"
          @update:value="handleKeyUp"
        />
      </div>
    </div>
    <n-infinite-scroll
      :style="{ height: windowHeight - 640 + 'px', marginTop: '10px' }"
      :distance="10"
      @load="handleLoad"
    >
      <n-table :bordered="false" :single-line="false">
        <thead>
          <tr>
            <th>{{ $t('IP地址') }}</th>
            <th>{{ $t('端口') }}</th>
            <th>{{ $t('用户') }}</th>
            <th>{{ $t('状态') }}</th>
            <th>{{ $t('操作时间') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in list" :key="index">
            <td>{{ item.address }}</td>
            <td>{{ item.port }}</td>
            <td>{{ item.user }}</td>
            <td>
              <span
                v-if="item.status === 1"
                style="color: var(--jm-success-color)"
                >{{ $t('登录成功') }}</span
              >
              <span v-else style="color: var(--jm-error-color)">{{
                $t('登录失败')
              }}</span>
            </td>
            <td>{{ item.time }}</td>
          </tr>
        </tbody>
      </n-table>
      <div v-if="handleLoading" class="handle-text">{{ $t('加载中') }}...</div>
      <div v-if="handleNoMore" class="handle-text">
        {{ $t('没有更多了') }}
      </div>
    </n-infinite-scroll>
    <!-- 开启SSH密钥登录 -->
    <!--    <n-modal :show="openKeyVisibly" :trap-focus="false">-->
    <!--      <modal-form-layout-->
    <!--        :title="$t('开启SSH密钥登录')"-->
    <!--        @on-cancel="closeKeyPop"-->
    <!--        @on-confirm="onKeyConfirm"-->
    <!--      >-->
    <!--        <n-form-->
    <!--          ref="formRef"-->
    <!--          :label-width="125"-->
    <!--          :model="formState"-->
    <!--          :show-require-mark="false"-->
    <!--          label-placement="left"-->
    <!--          size="medium"-->
    <!--        >-->
    <!--          <n-form-item :label="$t('密钥加密方式')" size="small">-->
    <!--            <n-select-->
    <!--              v-model:value="formState.type"-->
    <!--              :options="keyOptions"-->
    <!--              style="width: 225px"-->
    <!--            />-->
    <!--          </n-form-item>-->
    <!--        </n-form>-->
    <!--      </modal-form-layout>-->
    <!--    </n-modal>-->
    <!-- 查看密钥 -->
    <modal-layout :show="checkKeyVisibly" :trap-focus="false">
      <modal-form-layout
        :confirm-text="$t('复制')"
        :title="$t('开启SSH密钥登录')"
        @on-cancel="checkKeyVisibly = false"
        @on-confirm="copyKey"
      >
        <n-form
          :label-width="120"
          :show-require-mark="false"
          label-placement="left"
          size="medium"
        >
          <n-form-item label="" size="small">
            <n-input
              :value="sshkey"
              placeholder=""
              style="height: 134px; margin: 0 20px"
              type="textarea"
              class="modal-textarea"
            />
          </n-form-item>
        </n-form>
      </modal-form-layout>
    </modal-layout>
  </div>
</template>

<script lang="ts" setup>
  import { h, onActivated, reactive, ref, toRaw } from 'vue';
  import {
    NButton,
    NForm,
    NFormItem,
    NInput,
    NSelect,
    NSpace,
    NSwitch,
  } from 'naive-ui';
  import modalLayout from '@/layout/ModalLayout.vue';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import naiveui from '@/utils/naiveui';
  import {
    copyToClipboard,
    useRootElementCssVariable,
    // logOut,
  } from '@/utils';
  import { SshInfo, SshLog } from '@/api/type';
  import { useI18n } from 'vue-i18n';
  import { useApp } from '@/hooks/useApp';
  import {
    closeSshKey,
    getSshInfoApi,
    getSshKey,
    getSshLogApi,
    setSshKey,
    setSshPort,
  } from '@/api';

  const i18n = useI18n();

  const { windowHeight } = useApp();
  onActivated(() => {
    page.value = 1;
    list.value = [];
    getSshInfo();
    getSshLog();
  });
  const loading = ref(false);
  // const formRef: any = ref(null);
  // const openKeyVisibly = ref(false);
  const checkKeyVisibly = ref(false);
  const sshkey = ref('');
  const info = ref<SshInfo>({} as SshInfo);

  function downloadKey() {
    window.$gm.downloadFile(`${info.value.key_path}`);
  }

  const formState = reactive({
    ssh: 'yes',
    type: '',
  });
  // 设置ssh 的key
  const onKeyConfirm = async () => {
    await setSshKey(toRaw(formState));
    naiveui.message.success(i18n.t('操作成功'));
    info.value.pubkey_auth = 'yes';
    // openKeyVisibly.value = false;
    await getSshInfo();
  };
  // SSH设置登录
  const onPubKeyAuthChange = async (value: any) => {
    if (value === 'no') {
      loading.value = true;
      const res = await closeSshKey();
      loading.value = false;
      naiveui.message.success(res.msg);
      info.value.pubkey_auth = 'no';
      await getSshInfo();
    }
    if (value == 'yes') {
      formState.type = keyOptions[0].value;
      onKeyConfirm();
    }
  };
  let keyOptions: any[] = [];
  let rootOptions: any[] = [];
  // 获取ssh基本信息
  const getSshInfo = async () => {
    const res = await getSshInfoApi();
    info.value = res.data;
    rootOptions = [];
    for (const i in res.data.root_login_type_list) {
      rootOptions.push({
        label: res.data.root_login_type_list[i],
        value: i,
      });
    }
    keyOptions = [];
    res.data.ssh_key_list.forEach((item: any) => {
      keyOptions.push({
        label: item,
        value: item,
      });
    });
    // if (res.data.type === '') {
    //   formState.type = keyOptions[0].value;
    // } else {
    //   formState.type = res.data.type;
    // }
    formState.type = res.data.type;
  };
  // SSH端口保存
  const changePort = async () => {
    naiveui.dialog.warning({
      title: `${i18n.t('警告')}`,
      content: () =>
        h(
          'div',
          {
            style: {
              whiteSpace: 'pre-line',
            },
          },
          i18n.t(
            '修改会导致连接失败，确认修改？\n连接失败后请重新编辑连接信息！'
          )
        ),
      positiveText: `${i18n.t('确定')}`,
      negativeText: `${i18n.t('取消')}`,
      class: 'dialog-warning',
      maskClosable: false,
      onPositiveClick: async () => {
        const res = await setSshPort({ port: info.value.port });
        naiveui.message.success(res.msg);
        setTimeout(() => {
          // logOut();
        }, 2000);
      },
    });
  };
  // 查看key
  const chaKey = async () => {
    const res = await getSshKey();
    if (res.code > 0) {
      checkKeyVisibly.value = true;
      sshkey.value = res.data;
    }
  };

  // 复制key
  function copyKey({ done }) {
    naiveui.message.success(i18n.t('复制成功'));
    copyToClipboard(sshkey.value as string);
    done();
  }

  // function closeKeyPop() {
  //   info.value.pubkey_auth = 'no';
  //   openKeyVisibly.value = false;
  // }

  // 日志
  const searchType = ref('2');
  const keywords = ref<string>('');
  const listCount = reactive({
    success: 0,
    failed: 0,
  });
  const options = reactive([
    {
      label: i18n.t('全部'),
      value: '2',
    },
    {
      label: i18n.t('登录成功'),
      value: '1',
    },
    {
      label: i18n.t('登录失败'),
      value: '0',
    },
  ]);
  // type RowData = {
  //   key: number;
  //   name: string;
  //   age: string;
  //   address: string;
  //   status: number;
  // };
  type SslData = {
    time: string;
    user: string;
    address: string;
    port: string;
    status: number;
  };
  const list = ref<SshLog[]>([]);
  const pageSize = ref(20);
  const page = ref(1);
  const pageCount = ref(0);
  // 获取ssh登录日志
  const getSshLog = async (isRefresh = true) => {
    getSshLogApi(searchType.value, keywords.value, page.value, pageSize.value)
      .then((res) => {
        if (isRefresh) {
          list.value = res.data.data;
        } else {
          list.value = [...toRaw(list.value), ...res.data.data];
        }
        if (res.data.data.length < pageSize.value) {
          handleNoMore.value = true;
        }
        pageCount.value = res.data.total;
        listCount.success = list.value.filter((item: SslData) => {
          return item.status === 1;
        }).length;
        listCount.failed = list.value.filter((item: SslData) => {
          return item.status === 0;
        }).length;
      })
      .finally(() => {
        handleLoading.value = false;
      });
  };
  const handleKeyUp = () => {
    page.value = 1;
    getSshLog();
  };
  const handleLoading = ref(false);
  const handleNoMore = ref(false);
  const handleLoad = async () => {
    if (handleLoading.value || handleNoMore.value) {
      return;
    }
    handleLoading.value = true;
    await new Promise((resolve) => setTimeout(resolve, 1000));
    page.value++;
    getSshLog(false);
  };
</script>

<style lang="scss" scoped>
  .ssh {
    &-form {
      margin-top: 20px;
      background: var(--jm-accent-1);
      padding: 30px 0;
      border-radius: 4px;
    }
    &-title {
      @include flex(start);
      height: 80px;
      padding: 0 20px;
      margin-top: 20px;
      border-radius: 4px;
      background: var(--jm-accent-1);
      margin-bottom: 15px;
      color: var(--jm-accent-7);
      &-left {
        margin-left: 10px;
        margin-right: auto;
        & > div:nth-of-type(1) {
          font-weight: bold;
          font-size: 14px;
        }
        & > div:nth-of-type(2) {
          font-weight: 400;
          font-size: 12px;
          color: #afafaf;
        }
      }
    }
  }
  .changePort {
    color: #ffffff;
    font-size: 12px;
  }
  .modal-textarea {
    :deep(.n-input-wrapper) {
      resize: none !important;
    }
  }

  .handle-text {
    text-align: center;
    padding-top: 5px;
    color: var(--jm-accent-7);
    font-size: 12px;
  }
  .n-table {
    background: var(--jm-accent-1) !important;
    th,
    td {
      background: var(--jm-accent-1) !important;
      color: var(--jm-accent-7) !important;
      font-size: 12px !important;
      border-color: var(--jm-theme);
      border-right: none;
    }
    th {
      position: relative;
    }
    th::after {
      content: '';
      position: absolute;
      right: 0;
      top: 50%;
      transform: translateY(-50%);
      display: block;
      width: 1px;
      height: 12px;
      background: var(--jm-accent-3);
    }
    th:last-of-type::after {
      display: none;
    }
  }
</style>
