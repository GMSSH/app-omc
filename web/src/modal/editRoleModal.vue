<template>
  <modal-layout :show="visibly" @after-enter="onActive" @after-leave="onLeave">
    <modal-form-layout
      :width="500"
      :title="formType == 'add' ? $t('添加角色') : $t('修改角色')"
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
        <n-form-item :label="$t('角色名')" path="name" size="small">
          <n-input
            v-model:value="formState.name"
            clearable
            placeholder=""
            style="width: 250px"
          />
        </n-form-item>
        <n-form-item :label="$t('备注')" path="note" size="small">
          <n-input
            v-model:value="formState.note"
            clearable
            placeholder=""
            style="width: 250px"
          />
        </n-form-item>
        <n-form-item :label="$t('权限')" path="note" size="small">
          <n-tree
            virtual-scroll
            style="max-height: 320px"
            block-line
            cascade
            checkable
            :data="roleOptions"
            key-field="id"
            label-field="name"
            children-field="child"
            :checked-keys="checkedKeys"
            @update:checked-keys="updateCheckedKeys"
          />
        </n-form-item>
      </n-form>
    </modal-form-layout>
  </modal-layout>
</template>

<script lang="ts" setup>
  import { computed, ref } from 'vue';
  import { FormInst } from 'naive-ui';
  import naiveui from '@/utils/naiveui';
  import modalFormLayout from '@/layout/ModalFormLayout.vue';
  import { useI18n } from 'vue-i18n';
  import { UserRole } from '@/api/type';
  import modalLayout from '@/layout/ModalLayout.vue';
  import {
    addUserRoleApi,
    getRoleMenuListApi,
    getUserRoleApi,
    updateUserRoleApi,
  } from '@/api';

  const props = defineProps<{ visibly: boolean; item: UserRole }>();
  const formType = computed(() => {
    return props.item?.id ? 'edit' : 'add';
  });
  const i18n = useI18n();
  const emit = defineEmits(['update:visibly', 'onUpdate']);
  const returnOrgForm = () => ({
    name: '',
    note: '',
  });
  const rules = {
    name: {
      required: true,
      trigger: ['blur', 'input'],
      message: i18n.t('请输入角色名'),
    },
  };
  const formState = ref(returnOrgForm());
  const formRef = ref<FormInst | null>(null);
  const roleOptions = ref<[]>([]);
  const checkedKeys = ref();
  const showTree = ref(true);
  const onActive = () => {
    showTree.value = true;
    checkedKeys.value = [];
    getRoleMenuListApi().then((res) => {
      roleOptions.value = res.data.map((item: any) => {
        item.id = item.id + Math.random();
        return item;
      });
    });
    if (formType.value == 'edit') {
      formState.value.name = props.item.name;
      formState.value.note = props.item.note;
      getUserRoleApi(props.item.id).then((res) => {
        checkedKeys.value = res.data.submenu_ids.map((item: any) =>
          parseInt(item)
        );
      });
    }
  };
  const onLeave = () => {
    showTree.value = false;
    formState.value = returnOrgForm();
  };
  const updateCheckedKeys = (keys: any) => {
    checkedKeys.value = keys;
  };
  const submit = ({ done }) => {
    formRef.value?.validate((errors) => {
      if (!errors) {
        if (formType.value == 'add') {
          addUserRoleApi({
            name: formState.value.name,
            note: formState.value.note,
            submenu_ids: JSON.stringify(checkedKeys.value),
          })
            .then((res) => {
              emit('update:visibly', false);
              emit('onUpdate');
              naiveui.message.success(res.msg);
            })
            .finally(done);
        }
        if (formType.value == 'edit') {
          updateUserRoleApi({
            name: formState.value.name,
            note: formState.value.note,
            id: props.item.id,
            submenu_ids: JSON.stringify(checkedKeys.value),
          })
            .then((res) => {
              emit('update:visibly', false);
              emit('onUpdate');
              naiveui.message.success(res.msg);
            })
            .finally(done);
        }
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
