<template>
  <div class="cert" :style="{ minHeight: windowHeight - 220 + 'px' }">
    <div class="cert-title">
      <div style="color: var(--jm-accent-7)">
        {{ $t('SSH证书登录') }}
      </div>
      <n-switch
        v-model:value="certLogin"
        style="margin-left: 10px"
        :loading="switchLoading"
        @update:value="handleUpdateSwitch"
      />
    </div>
    <template v-if="certLogin">
      <div class="cert-title">
        <div>{{ $t('SSH证书列表') }}</div>
        <div>
          <select-directory
            v-model:value="path"
            style="width: 230px; margin-right: 10px"
          />
          <n-button
            :color="useRootElementCssVariable('jm-accent-3')"
            style="margin-right: 10px"
            :disabled="!path"
            @click="uploadKey"
          >
            {{ $t('上传公钥') }}
          </n-button>
          <n-button
            :color="useRootElementCssVariable('jm-accent-3')"
            @click="editCertVisibly = true"
          >
            {{ $t('签发SSH证书') }}
          </n-button>
        </div>
      </div>
      <div class="cert-space">
        <n-input
          v-model:value="keyWord"
          clearable
          :placeholder="$t('输入序列号、KeyID，Enter搜索')"
          style="width: 300px"
          @clear="nextTick(getList)"
          @keyup.enter="getList()"
        >
          <template #prefix>
            <svg-icon
              color="var(--jm-accent-7)"
              icon="icon-sousuo"
              font-size="16"
            />
          </template>
        </n-input>
      </div>
      <n-scrollbar x-scrollable>
        <n-spin :show="loading">
          <n-data-table
            :columns="columns"
            :data="data"
            :max-height="windowHeight - 400"
            size="small"
          />
        </n-spin>
      </n-scrollbar>
    </template>

    <!-- 查看密钥 -->
    <modal-layout :show="checkKeyVisibly" :trap-focus="false">
      <modal-form-layout
        :confirm-text="$t('复制')"
        :title="$t('查看SSH证书')"
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
    <edit-cert-modal
      v-model:visibly="editCertVisibly"
      :item-info="itemInfo"
      @on-update="getList"
    />
  </div>
</template>
<script setup lang="ts">
  import { useApp } from '@/hooks/useApp';
  import { h, nextTick, ref } from 'vue';
  import { useI18n } from 'vue-i18n';
  import svgIcon from '@/components/IconFont.vue';
  import modalLayout from '@/layout/ModalLayout.vue';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import { NTooltip } from 'naive-ui';
  import naiveui from '@/utils/naiveui';
  import {
    copyToClipboard,
    getWinFiles,
    useRootElementCssVariable,
  } from '@/utils';
  import SelectDirectory from '@/components/SelectDirectory.vue';
  import editCertModal from '@/modal/editCertModal.vue';
  import { SysCert } from '@/api/type';
  import {
    disableCert,
    enableCert,
    getCertKey,
    getCertList,
    getCertStatus,
    revokeCert,
  } from '@/api';

  const { windowHeight } = useApp();
  const checkKeyVisibly = ref(false);
  const sshkey = ref('');
  const path = ref('');

  const certLogin = ref(false);
  const switchLoading = ref(false);
  const editCertVisibly = ref(false);
  const handleUpdateSwitch = (value: boolean) => {
    switchLoading.value = true;
    // 打开
    if (value) {
      enableCert()
        .then((res) => {
          naiveui.message.success(res.msg);
        })
        .finally(() => {
          switchLoading.value = false;
          getStatus();
        });
    } else {
      // 关闭
      disableCert()
        .then((res) => {
          naiveui.message.success(res.msg);
        })
        .finally(() => {
          switchLoading.value = false;
          getStatus();
        });
    }
  };
  const copyKey = ({ done }) => {
    naiveui.message.success(i18n.t('复制成功'));
    copyToClipboard(sshkey.value as string);
    done();
  };
  const i18n = useI18n();
  const keyWord = ref('');
  const loading = ref(false);
  const getList = () => {
    loading.value = true;
    getCertList(keyWord.value)
      .then((res) => {
        data.value = res.data;
      })
      .finally(() => {
        loading.value = false;
      });
  };
  const getStatus = () => {
    getCertStatus().then((res) => {
      certLogin.value = res.data == 'yes';
    });
  };
  getStatus();
  getList();
  const uploadKey = async () => {
    const files = await getWinFiles();
    window.$gm.openUpload({ files, path: path.value });
  };
  const itemInfo = ref<SysCert>({} as SysCert);
  const columns = [
    {
      title: 'Key ID',
      key: 'key_id',
      minWidth: 80,
      ellipsis: {
        tooltip: {
          maxWidth: 400,
        },
      },
      resizable: true,
    },
    {
      title: i18n.t('用户名'),
      key: 'user_principal',
      minWidth: 80,
      ellipsis: {
        tooltip: {
          maxWidth: 400,
        },
      },
      resizable: true,
      render(row: SysCert) {
        return h('span', row.user_principal?.join('、'));
      },
    },
    {
      title: i18n.t('序列号'),
      key: 'serial_number',
      minWidth: 80,
      ellipsis: {
        tooltip: true,
      },
      resizable: true,
    },
    {
      title: i18n.t('签发开始日期'),
      key: 'valid_from',
      minWidth: 120,
      ellipsis: {
        tooltip: true,
      },
      resizable: true,
    },
    {
      title: i18n.t('签发结束日期'),
      key: 'valid_to',
      minWidth: 120,
      ellipsis: {
        tooltip: true,
      },
      resizable: true,
    },
    {
      title: i18n.t('备注'),
      key: 'remark',
      minWidth: 80,
      ellipsis: {
        tooltip: true,
      },
      resizable: true,
    },
    {
      title: i18n.t('状态'),
      key: 'status',
      minWidth: 60,
      ellipsis: {
        tooltip: true,
      },
      resizable: true,
      render(row: SysCert) {
        return h('span', row.status ? i18n.t('有效') : i18n.t('无效'));
      },
    },
    {
      title: i18n.t('操作'),
      width: 100,
      render(row: SysCert) {
        if (row.status) {
          return h('div', [
            h(
              NTooltip,
              {},
              {
                trigger: () =>
                  h(svgIcon, {
                    icon: 'icon-cert-2',
                    color: 'var(--jm-accent-7)',
                    style: { cursor: 'pointer', marginRight: '15px' },
                    title: i18n.t('查看'),
                    fontSize: '18',
                    onClick: () => {
                      itemInfo.value = {} as SysCert;
                      getCertKey(row.serial_number).then((res) => {
                        sshkey.value = res.data;
                        checkKeyVisibly.value = true;
                      });
                    },
                  }),
                default: () => i18n.t('查看'),
              }
            ),

            h(
              NTooltip,
              {},
              {
                trigger: () =>
                  h(svgIcon, {
                    icon: 'icon-xz',
                    color: 'var(--jm-accent-7)',
                    style: { cursor: 'pointer', marginRight: '15px' },
                    fontSize: '18',
                    onClick: () => {
                      itemInfo.value = {} as SysCert;
                      window.$gm.downloadFile(row.certificate_path);
                    },
                  }),
                default: () => i18n.t('下载'),
              }
            ),
            h(
              NTooltip,
              {},
              {
                trigger: () =>
                  h(svgIcon, {
                    icon: 'icon-uninstall',
                    color: 'var(--jm-accent-7)',
                    fontSize: '18',
                    style: { cursor: 'pointer' },

                    onClick: () => {
                      itemInfo.value = {} as SysCert;
                      naiveui.dialog.warning({
                        title: i18n.t('警告'),
                        content: `${i18n.t('您真的要吊销客户端证书吗?')}`,
                        positiveText: `${i18n.t('确定')}`,
                        negativeText: `${i18n.t('取消')}`,
                        class: 'dialog-warning',
                        maskClosable: false,
                        onPositiveClick: () => {
                          revokeCert(row.serial_number)
                            .then((res) => {
                              naiveui.message.success(res.msg);
                            })
                            .finally(() => {
                              getList();
                            });
                        },
                      });
                    },
                  }),
                default: () => i18n.t('删除'),
              }
            ),
          ]);
        } else {
          return h('div', [
            h(
              NTooltip,
              {},
              {
                trigger: () =>
                  h(svgIcon, {
                    icon: 'icon-cert-3',
                    color: 'var(--jm-accent-7)',
                    style: { cursor: 'pointer' },
                    fontSize: '18',
                    onClick: () => {
                      itemInfo.value = row;
                      editCertVisibly.value = true;
                    },
                  }),
                default: () => i18n.t('编辑'),
              }
            ),
          ]);
        }
      },
    },
  ];
  const data = ref<SysCert[]>([]);
</script>
<style scoped lang="scss">
  .modal-textarea {
    :deep(.n-input-wrapper) {
      resize: none !important;
    }
  }
  .cert {
    :deep(.n-input__input-el) {
      height: auto !important;
    }

    &-title {
      height: 60px;
      padding: 0 20px;
      border-radius: 4px;
      background: var(--jm-accent-1);
      @include flex(left);
      justify-content: space-between;
      font-weight: 400;
      font-size: 14px;
      color: var(--jm-accent-7);
      margin-top: 20px;
    }

    &-space {
      height: 60px;
      padding: 0 20px;
      background: var(--jm-accent-1);
      @include flex(left);
      margin-top: 20px;
      margin-bottom: 1px;
    }
  }
</style>
