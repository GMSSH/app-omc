<template>
  <modal-layout :show="visibly" @after-enter="onActive" @after-leave="onLeave">
    <modal-form-layout
      :width="400"
      :title="$t('编辑用户')"
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
            disabled
            clearable
            placeholder=""
            style="width: 250px"
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
            style="width: 250px"
          />
        </n-form-item>
        <n-form-item :label="$t('描述')" path="des" size="small">
          <n-input
            v-model:value="formState.des"
            clearable
            placeholder=""
            style="width: 250px"
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
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import { useI18n } from 'vue-i18n';
  import { SysUser } from '@/api/type';
  import modalLayout from '@/layout/ModalLayout.vue';
  import { editSysUserApi, getFetchGroupsApi } from '@/api';

  const props = defineProps<{ visibly: boolean; userInfo: SysUser }>();
  const i18n = useI18n();
  const emit = defineEmits(['update:visibly', 'onUpdate']);
  const returnOrgForm = () => ({
    username: '',
    gid: '',
    des: '',
  });
  const rules = {
    username: {
      required: true,
      trigger: ['blur', 'input'],
      message: i18n.t('请输入用户名'),
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
  const onActive = () => {
    formState.value.username = props.userInfo.username;
    formState.value.des = props.userInfo.des;
    formState.value.gid = props.userInfo.gid?.toString();

    getFetchGroupsApi().then((res) => {
      options.value = res.data;
    });
  };
  const onLeave = () => {
    formState.value = returnOrgForm();
  };
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
  const submit = ({ done }) => {
    formRef.value?.validate((errors) => {
      if (!errors) {
        const data = toRaw(formState.value);
        editSysUserApi(data)
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
</style>
