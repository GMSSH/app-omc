<template>
  <input v-if="isEdit" v-focus :value="value" type="text" @blur="onblur" />
  <span v-else @click="isEdit = true" :title="value">{{ value }}</span>
</template>
<script lang="ts" setup>
  import { ref } from 'vue';

  defineProps({
    value: String,
  });
  const emit = defineEmits(['onChange']);
  const isEdit = ref(false);
  const onblur = () => {
    emit('onChange');
    isEdit.value = false;
  };
</script>

<style lang="scss" scoped>
  input {
    max-width: 100%;
    outline: none;
    box-sizing: border-box;
    position: relative;
    border: 1px solid var(--jm-global-color);
    border-radius: 4px;
  }

  span {
    cursor: pointer;
    @include ellipsis();
  }
</style>
