<template>
  <n-input
    ref="inputRef"
    :placeholder="`${type == 'folder' ? $t('directory') : $t('file')}`"
    :value="value"
    @input="handleInput"
  >
    <template #suffix>
      <div class="suffix-box" @click="open">
        <img src="@/assets/wj1.png" alt="" />
        <span>{{ $t('browse') }}</span>
      </div>
    </template>
  </n-input>
</template>
<script lang="ts" setup>
  import { InputInst } from 'naive-ui';
  import { PropType, ref, toRaw } from 'vue';
  const props = defineProps({
    value: { type: String },
    type: {
      type: String as PropType<'file' | 'folder'>,
      default: 'folder',
    },
    disabled: { type: Boolean, default: false },
  });
  const collapseSlashes = (str: string) => {
    return str.replace(/\/+/g, '/');
  };
  const inputRef = ref<InputInst | null>(null);
  const emit = defineEmits(['update:value', 'path-selected']);
  const handleInput = (v: string) => {
    emit('update:value', collapseSlashes(v));
  };
  const open = () => {
    if (props.disabled) {
      return;
    }
    if (props.type == 'folder') {
      window?.$gm?.chooseFolder((v: any) => {
        if (v) {
          emit('update:value', collapseSlashes(v)); // 更新输入框的值
          emit('path-selected', v); // 向父组件发送选择的路径
        }
      }, props.value);
    } else {
      let path = toRaw(props.value) as string;
      const lastSlashIndex = path?.lastIndexOf('/');
      path = path?.substring(0, lastSlashIndex) || '/';
      window?.$gm?.chooseFile((v: any) => {
        if (v) {
          emit('update:value', collapseSlashes(v)); // 更新输入框的值
          emit('path-selected', v); // 向父组件发送选择的路径
        }
      }, path);
    }
  };
</script>
<style lang="scss" scoped>
  .suffix-box {
    // width: 78px;
    border-left: 1px solid var(--jm-accent-3);
    cursor: pointer;
    height: calc(100% - 10px);
    display: flex;
    align-items: center;

    img {
      width: 16px;
      margin-left: 14px;
      margin-right: 10px;
    }
  }
</style>
