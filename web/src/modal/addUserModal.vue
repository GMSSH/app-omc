<template>
  <modal-layout :show="visibly" @after-enter="onActive" @after-leave="onLeave">
    <modal-form-layout
      :width="500"
      :title="$t('添加用户')"
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
        <n-form-item :label="$t('用户名')" path="username" size="small">
          <n-input
            v-model:value="formState.username"
            clearable
            placeholder=""
            style="width: 80%"
          />
        </n-form-item>
        <n-form-item :label="$t('所属组')" path="gid" size="small">
          <n-select
            v-model:value="formState.gid"
            :options="options"
            clearable
            label-field="label"
            value-field="value"
            :render-label="renderLabel"
            :placeholder="$t('请选择')"
            style="width: 80%"
          />
        </n-form-item>
        <n-form-item :label="$t('密码')" path="passwd" size="small">
          <n-input
            v-model:value="formState.passwd"
            clearable
            placeholder=""
            style="width: 80%"
          >
            <template #suffix>
              <svg-icon
                icon="icon-chongqi"
                font-size="16"
                style="cursor: pointer"
                color="var(--jm-accent-5)"
                @click="changeMm"
              />
            </template>
          </n-input>
        </n-form-item>
        <n-form-item :label="$t('登录')" path="allow" size="small">
          <n-radio-group v-model:value="formState.allow">
            <n-space>
              <n-radio value="1">
                {{ $t('允许登录') }}
              </n-radio>
              <n-radio value="0">
                {{ $t('禁止登录') }}
              </n-radio>
            </n-space>
          </n-radio-group>
        </n-form-item>
        <n-form-item :label="$t('描述')" path="des" size="small">
          <n-input
            v-model:value="formState.des"
            clearable
            placeholder=""
            style="width: 80%"
          />
        </n-form-item>
      </n-form>
    </modal-form-layout>
  </modal-layout>
</template>

<script lang="ts" setup>
  import { h, ref, toRaw } from 'vue';
  import { FormInst } from 'naive-ui';
  import naiveui from '@/utils/naiveui';
  import { generateRandomString } from '@/utils';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import { useI18n } from 'vue-i18n';
  import modalLayout from '@/layout/ModalLayout.vue';
  import { addSysUserApi, getFetchGroupsApi } from '@/api';
  import SvgIcon from '@/components/IconFont.vue';

  const isLoad = ref(false);
  defineProps<{ visibly: boolean }>();
  const i18n = useI18n();
  const emit = defineEmits(['update:visibly', 'onUpdate']);
  const returnOrgForm = () => ({
    username: '',
    passwd: '',
    gid: '',
    role_id: '',
    allow: '1',
    des: '',
  });
  const rules = {
    username: {
      required: true,
      validator(_, value: string) {
        if (!value) {
          return new Error(i18n.t('请输入用户名'));
        } else if (!/^[a-zA-Z][a-zA-Z0-9]{2,}$/.test(value)) {
          return new Error(i18n.t('须以字母开头，且包含至少2位字母或数字组合'));
        }
        return true;
      },
      trigger: ['input', 'blur'],
    },
    passwd: {
      required: true,
      validator(_, value: string) {
        if (!value) {
          return new Error(i18n.t('请输入密码'));
        } else if (!/^[A-Za-z].{7,}$/.test(value)) {
          return new Error(i18n.t('密码必须字母开头且大于七位'));
        }
        return true;
      },
      trigger: ['input', 'blur'],
    },
    gid: {
      required: true,
      trigger: ['blur', 'change'],
      message: i18n.t('请选择'),
    },
  };
  const formState = ref(returnOrgForm());
  const formRef = ref<FormInst | null>(null);
  const options = ref<{ g_name: string; gid: string; is_sudoers: boolean }[]>(
    []
  );
  const renderLabel = (option: any) => {
    return h(
      'div',
      {
        class: 'select-render-label',
        style: {
          width: '280px',
          display: 'flex',
          flexWrap: 'nowrap',
          alignItems: 'center',
        },
      },
      [
        h(
          'div',
          {
            style: {
              marginRight: '5px',
            },
          },
          option.label
        ),
        h(
          'div',
          {
            class: 'select-render-label-child',
            style: {
              marginRight: 'auto',
              color: 'var(--jm-accent-5)',
              fontSize: '10px',
            },
          },
          option.is_sudoers ? 'sudoers' : ''
        ),
      ]
    );
  };

  function changeMm() {
    isLoad.value = true;
    formState.value.passwd = generateRandomString();
    isLoad.value = false;
  }

  const onActive = () => {
    changeMm();
    getFetchGroupsApi().then((res) => {
      options.value = res.data;
    });
  };
  const onLeave = () => {
    formState.value = returnOrgForm();
  };
  const submit = ({ done }) => {
    formRef.value?.validate((errors) => {
      if (!errors) {
        const data = toRaw(formState.value);
        addSysUserApi(data)
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
<style lang="scss" scoped>
  :deep(.n-base-selection-tags) {
    .select-render-label {
      width: auto !important;

      &-child {
        display: none;
      }
    }
  }

  :deep(.n-base-select-menu) {
    .n-virtual-list {
      max-height: 180px !important;
    }
  }
</style>
