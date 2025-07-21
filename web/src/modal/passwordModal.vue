<template>
  <modal-layout :show="visibly" @after-enter="onActive" @after-leave="onLeave">
    <modal-form-layout
      :width="400"
      :title="modalType"
      @on-cancel="closeModal"
      @on-confirm="submit"
    >
      <n-form
        ref="formRef"
        :model="formState"
        label-placement="left"
        label-width="97"
      >
        <n-form-item :label="$t('密码')" path="password" size="small">
          <n-input
            v-model:value="formState.password"
            clearable
            placeholder=""
            style="width: 250px"
          />
          <svg-icon
            icon="icon-chongqi"
            font-size="16"
            style="cursor: pointer; margin-left: 5px"
            color="var(--jm-accent-5)"
            @click="changeMm"
          />
        </n-form-item>
      </n-form>
    </modal-form-layout>
  </modal-layout>
</template>

<script lang="ts" setup>
  import { computed, reactive, ref } from 'vue';
  import { FormInst } from 'naive-ui';
  import naiveui from '@/utils/naiveui';
  import { generateRandomString } from '@/utils';
  import { SysUser } from '@/api/type';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import modalLayout from '@/layout/ModalLayout.vue';
  import {
    allowSysUserApi,
    changeSysUserPasswdApi,
    deactivateSysUserApi,
  } from '@/api';
  import SvgIcon from '@/components/IconFont.vue';
  import { useI18n } from 'vue-i18n';
  const i18n = useI18n();
  const isLoad = ref(false);
  const props = defineProps<{ visibly: boolean; userInfo: SysUser }>();
  const modalType = computed(() => {
    if (props.userInfo.disable == '1') {
      return i18n.t('恢复账号');
    } else if (props.userInfo.is_login == '1') {
      return i18n.t('修改密码');
    } else {
      return i18n.t('允许登录');
    }
  });
  const emit = defineEmits(['update:visibly', 'onUpdate']);
  const formState = reactive({
    password: '',
  });
  const formRef = ref<FormInst | null>(null);

  function changeMm() {
    isLoad.value = true;
    formState.password = generateRandomString();
    isLoad.value = false;
  }

  const onActive = () => {
    changeMm();
  };
  const onLeave = () => {
    formState.password = '';
  };
  const submit = ({ done }) => {
    if (modalType.value == i18n.t('修改密码')) {
      changeSysUserPasswdApi(props.userInfo.username, formState.password)
        .then((res) => {
          emit('update:visibly', false);
          emit('onUpdate');
          naiveui.message.success(res.msg);
        })
        .finally(done);
    }
    if (modalType.value == i18n.t('允许登录')) {
      allowSysUserApi(props.userInfo.username, '1', formState.password)
        .then((res) => {
          emit('update:visibly', false);
          emit('onUpdate');
          naiveui.message.success(res.msg);
        })
        .finally(done);
    }
    if (modalType.value == i18n.t('恢复账号')) {
      deactivateSysUserApi(props.userInfo.username, '0', formState.password)
        .then((res) => {
          emit('update:visibly', false);
          emit('onUpdate');
          naiveui.message.success(res.msg);
        })
        .finally(done);
    }
  };
  const closeModal = () => {
    emit('update:visibly', false);
  };
</script>
<style lang="scss" scoped></style>
