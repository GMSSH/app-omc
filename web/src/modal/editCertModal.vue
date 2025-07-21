<template>
  <modal-layout :show="visibly" @after-enter="onActive" @after-leave="onLeave">
    <modal-form-layout
      :width="500"
      :title="$t('签发SSH证书')"
      @on-cancel="closeModal"
      @on-confirm="submit"
    >
      <n-form
        ref="formRef"
        :model="formState"
        :rules="rules"
        label-placement="left"
        label-width="97"
      >
        <n-form-item :label="$t('公钥路径')" path="path" size="small">
          <select-directory
            v-model:value="formState.path"
            style="width: 340px"
            type="file"
          />
        </n-form-item>

        <n-form-item :label="$t('用户名')" path="user" size="small">
          <n-select
            v-model:value="formState.user"
            :options="options"
            clearable
            multiple
            label-field="username"
            value-field="username"
            :placeholder="$t('请选择')"
            style="width: 340px"
          />
        </n-form-item>
        <n-form-item :label="$t('有效期')" path="date" size="small">
          <n-select
            v-model:value="time"
            :options="dateOptions"
            style="width: 100px; margin-right: 5px"
            :render-option="renderOption"
          />
          <n-input-number
            v-model:value="formState.date"
            step="1"
            :precision="0"
            :placeholder="$t('请输入')"
            :min="1"
          />
          <span style="margin-left: 5px">{{ timeEnum[time] }}</span>
        </n-form-item>
        <n-form-item label="Key ID" path="key" size="small">
          <n-input
            v-model:value="formState.key"
            clearable
            placeholder=""
            style="width: 340px"
          />
        </n-form-item>
        <n-form-item :label="$t('备注')" size="small">
          <n-input
            v-model:value="formState.remark"
            clearable
            placeholder=""
            maxlength="50"
            show-count
            style="width: 340px"
          />
        </n-form-item>
        <p style="padding: 0 40px; font-size: 12px; color: var(--jm-accent-5)">
          {{
            $t(
              '若使用当前公钥签发的证书无法登录，请尝试更换其他加密算法类型的公钥后重试'
            )
          }}
        </p>
      </n-form>
    </modal-form-layout>
  </modal-layout>
</template>

<script lang="ts" setup>
  import { h, ref, toRaw, VNode } from 'vue';
  import { FormInst, NTooltip, SelectOption } from 'naive-ui';
  import naiveui from '@/utils/naiveui';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import { useI18n } from 'vue-i18n';
  import { SysUser, SysCert } from '@/api/type';
  import modalLayout from '@/layout/ModalLayout.vue';
  import SelectDirectory from '@/components/SelectDirectory.vue';
  import { generateCert, getSysUserListApi } from '@/api';

  const props = defineProps<{ visibly: boolean; itemInfo: SysCert }>();
  const i18n = useI18n();
  const emit = defineEmits(['update:visibly', 'onUpdate']);
  const returnOrgForm = () => ({
    path: '',
    user: [] as string[],
    date: 1,
    key: '',
    remark: '',
  });
  const renderOption = ({
    node,
    option,
  }: {
    node: VNode;
    option: SelectOption;
  }) =>
    h(
      NTooltip,
      { style: 'width: 110px' },
      {
        trigger: () => node,
        default: () => option.label,
      }
    );
  const rules = {
    path: {
      required: true,
      trigger: ['blur', 'input'],
      message: i18n.t('请输入公钥路径'),
    },
    user: {
      type: 'array',
      required: true,
      trigger: ['blur', 'change'],
      message: i18n.t('请输入用户名'),
    },
    date: {
      type: 'number',
      required: true,
      trigger: ['blur', 'input'],
      message: i18n.t('请输入'),
    },
    key: {
      required: true,
      trigger: ['blur', 'input'],
      message: i18n.t('请输入Key ID'),
    },
  };
  const formState = ref(returnOrgForm());
  const formRef = ref<FormInst | null>(null);
  const options = ref<SysUser[]>([]);
  const time = ref('y');

  enum timeEnum {
    y = i18n.t('年') as any,
    m = i18n.t('月') as any,
    w = i18n.t('周') as any,
    d = i18n.t('日') as any,
  }

  const dateOptions = [
    {
      label: i18n.t('IssueCertificateTime', { time: timeEnum.y }),
      value: 'y',
    },
    {
      label: i18n.t('IssueCertificateTime', { time: timeEnum.m }),
      value: 'm',
    },
    {
      label: i18n.t('IssueCertificateTime', { time: timeEnum.w }),
      value: 'w',
    },
    {
      label: i18n.t('IssueCertificateTime', { time: timeEnum.d }),
      value: 'd',
    },
  ];

  const onActive = () => {
    getSysUserListApi().then((res) => {
      options.value = res.data;
    });
    if (props.itemInfo) {
      formState.value.path = props.itemInfo.certificate_path;
      formState.value.user = props.itemInfo.user_principal;
      formState.value.key = props.itemInfo.key_id;
      formState.value.remark = props.itemInfo.remark;
    }
  };
  const onLeave = () => {
    formState.value = returnOrgForm();
  };
  const submit = ({ done }) => {
    formRef.value?.validate((errors) => {
      if (!errors) {
        const data = toRaw(formState.value);
        let validityPeriod = formState.value.date + time.value;
        // 月和年要单独处理
        if (time.value == 'y') {
          validityPeriod = `${365 * formState.value.date}d`;
        }
        if (time.value == 'm') {
          validityPeriod = `${30 * formState.value.date}d`;
        }
        generateCert({
          key_id: data.key,
          user_key_path: data.path,
          user_principal: data.user.join(','),
          validity_period: validityPeriod,
          remark: data.remark,
        })
          .then((res) => {
            emit('update:visibly', false);
            emit('onUpdate');
            naiveui.message.success(res.msg);
          })
          .finally(done);
      } else {
        done();
      }
    });
  };
  const closeModal = () => {
    emit('update:visibly', false);
  };
</script>
<style lang="scss" scoped></style>
