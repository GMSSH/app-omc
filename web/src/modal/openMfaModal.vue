<template>
  <modal-layout
    :show="visibly"
    :trap-focus="false"
    @after-enter="onActive"
    @after-leave="onClose"
  >
    <modal-form-layout
      :width="410"
      :title="$t('创建MFA')"
      :confirm-text="mfaStatus == 'one' ? $t('下一步') : $t('确认')"
      @on-cancel="closeModal"
      @on-confirm="submit"
    >
      <template v-if="mfaStatus == 'one'">
        <n-form
          ref="formRef"
          :model="formState"
          label-placement="left"
          label-width="97"
        >
          <template v-if="mfaOptions.length">
            <n-form-item :label="$t('MFA别名')" size="small">
              <n-select
                v-model:value="formState.name"
                :options="mfaOptions"
                :placeholder="$t('选择MFA别名')"
                style="width: 250px"
              />
            </n-form-item>
            <n-form-item :label="$t('动态口令')" size="small">
              <n-input
                v-model:value="formState.code"
                clearable
                :placeholder="$t('输入动态口令')"
                style="width: 250px"
              />
            </n-form-item>
          </template>
          <n-form-item :label="$t('绑定别名')" size="small">
            <n-input
              v-model:value="formState.new_name"
              clearable
              :placeholder="$t('输入MFA别名')"
              style="width: 250px"
            />
          </n-form-item>
        </n-form>
      </template>
      <template v-if="mfaStatus == 'two'">
        <n-form label-placement="left" size="small" label-width="97">
          <n-form-item>
            <n-button
              size="small"
              type="primary"
              style="margin-left: 20px"
              @click="onBack"
            >
              <svg-icon
                color="var(--jm-accent-7)"
                font-size="14"
                icon="icon-a-Arrow-leftjiantouzuo"
                style="margin-right: 5px"
              />

              {{ $t('返回') }}
            </n-button>
          </n-form-item>
          <div class="add-modal-body-title" style="margin-top: 10px">
            {{ $t('第一步：使用xxx扫码二维码或使用密钥绑定') }}
          </div>

          <n-form-item :label="$t('密钥')" size="small">
            <div>
              <n-space>
                <span style="font-size: 14px">{{
                  isBol ? '*********************' : secret
                }}</span>
              </n-space>
              <div style="margin-top: 10px">
                <svg-icon
                  :icon="isBol ? 'icon-chakan' : 'icon-yincang'"
                  color="var(--jm-accent-7)"
                  font-size="16"
                  style="cursor: pointer; margin-right: 10px"
                  @click="isBol = !isBol"
                />
                <n-button
                  text
                  type="primary"
                  size="small"
                  @click="copyToClipboard(secret)"
                >
                  {{ $t('复制') }}
                </n-button>
                <n-button
                  text
                  type="primary"
                  size="small"
                  style="margin-left: 10px"
                  @click="downTxtFile"
                >
                  {{ $t('下载') }}
                </n-button>
              </div>
            </div>
          </n-form-item>
          <n-form-item :label="$t('二维码')" size="small">
            <div>
              <div>
                <qrcode-vue
                  :size="150"
                  :value="verifyUrl"
                  :margin="1"
                  render-as="svg"
                />
              </div>
              <p style="color: var(--jm-accent-5); font-size: 12px">
                {{ $t('绑定后输入动态口令校验') }}
              </p>
            </div>
          </n-form-item>
          <div class="add-modal-body-title">
            {{ $t('第二步：绑定后输入动态口令校验') }}
          </div>
          <n-form-item :label="$t('动态口令')" size="small">
            <n-input
              v-model:value="verifyCode"
              clearable
              maxlength="6"
              :placeholder="$t('输入六位口令')"
              type="text"
              style="width: 250px"
            />
          </n-form-item>
        </n-form>
      </template>
    </modal-form-layout>
  </modal-layout>
</template>
<script lang="ts" setup>
  import QrcodeVue from 'qrcode.vue';
  import { reactive, ref } from 'vue';
  import naiveui from '@/utils/naiveui';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import ModalLayout from '@/layout/ModalLayout.vue';
  import { FormInst } from 'naive-ui';
  import { addMfaApi, authMfaApi, mfaBindListApi } from '@/api';
  import { copyToClipboard } from '@/utils';
  defineProps<{ visibly: boolean }>();
  const emit = defineEmits(['update:visibly', 'createUpdate']);
  const verifyCode = ref('');
  const verifyUrl = ref('');
  const verifyUuid = ref('');
  const closeModal = () => {
    emit('update:visibly', false);
  };
  const isBol = ref(false);
  const secret = ref('');
  const formState = reactive<{ name: any; code: string; new_name: string }>({
    name: '',
    code: '',
    new_name: '',
  });
  const formRef = ref<FormInst | null>(null);
  const mfaOptions = ref<{ label: string; value: string }[]>([]);
  const mfaStatus = ref('one');
  const rest = () => {
    verifyCode.value = '';
    formState.name = null;
    formState.new_name = '';
    formState.code = '';
    mfaStatus.value = 'one';
  };
  const onActive = () => {
    getMfaOptions();
    rest();
  };
  const getMfaOptions = () => {
    mfaBindListApi().then((res) => {
      mfaOptions.value = res.data.alias_list.map((item) => {
        return {
          label: item.alias,
          value: item.uuid,
        };
      });
    });
  };
  const onClose = () => {
    rest();
    mfaStatus.value = 'one';
  };
  const onBack = () => {
    mfaStatus.value = 'one';
    rest();
  };

  const submit = ({ done }) => {
    // 第一步
    if (mfaStatus.value == 'one') {
      const params = {
        existing_uuid: formState.name,
        existing_code: formState.code,
        alias: formState.new_name,
      };
      addMfaApi(params)
        .then((res) => {
          mfaStatus.value = 'two';
          verifyUrl.value = res.data.url;
          verifyUuid.value = res.data.uuid;
          secret.value = res.data.secret;
        })
        .finally(() => {
          done();
        });
    }
    // 第二步
    if (mfaStatus.value == 'two') {
      authMfaApi({
        uuid: verifyUuid.value,
        code: verifyCode.value,
      })
        .then((res) => {
          naiveui.message.success(res.msg);
          emit('update:visibly', false);
          emit('createUpdate');
        })
        .finally(() => {
          done();
        });
    }
  };

  const downTxtFile = () => {
    const text = secret.value;
    const fileName = 'mfa.txt';
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const downloadLink = document.createElement('a');
    downloadLink.download = fileName;
    downloadLink.href = URL.createObjectURL(blob);
    downloadLink.click();
  };
</script>
<style lang="scss" scoped>
  .add-modal-body {
    &-card {
      &-cell {
        align-items: flex-start;
        margin-top: 18px;
        &-label {
          font-size: 12px;
          margin: 5px 0;
        }
      }
    }
    &-title {
      font-size: 12px;
      margin: 5px 0 20px 30px;
      color: var(--jm-accent-5);
    }
  }
</style>
