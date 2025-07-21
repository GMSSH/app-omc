<template>
  <modal-layout :show="visibly" :trap-focus="false" @after-enter="onActive">
    <modal-form-layout
      :width="400"
      :title="`${$t('解绑')}MFA【${item.alias}】`"
      @on-cancel="closeModal"
      @on-confirm="submit"
    >
      <n-form ref="formRef" label-placement="left" label-width="97">
        <n-form-item :label="$t('MFA别名')" size="small">
          <n-input style="width: 250px" :value="item.alias" disabled />
        </n-form-item>
        <n-form-item :label="$t('动态口令')" size="small">
          <n-input
            v-model:value="code"
            clearable
            :placeholder="$t('输入动态口令')"
            style="width: 250px"
          />
        </n-form-item>
      </n-form>
    </modal-form-layout>
  </modal-layout>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import ModalLayout from '@/layout/ModalLayout.vue';
  import { MfaItem } from '@/api/type';
  import { delMfaApi } from '@/api';
  import naiveui from '@/utils/naiveui';

  const props = defineProps<{
    visibly: boolean;
    item: MfaItem;
  }>();

  const emit = defineEmits(['update:visibly', 'onUpdate']);
  const code = ref('');
  const onActive = () => {
    code.value = '';
  };

  const submit = ({ done }) => {
    delMfaApi({
      uuid: props.item.uuid,
      code: code.value,
    })
      .then((res) => {
        emit('update:visibly', false);
        emit('onUpdate');
        naiveui.message.success(res.msg);
      })
      .finally(done);
  };
  const closeModal = () => {
    emit('update:visibly', false);
  };
</script>
<style lang="scss" scoped></style>
