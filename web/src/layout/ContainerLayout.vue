<template>
  <div class="container-layout">
    <div class="container-layout-title">
      {{ title }}
    </div>
    <n-scrollbar
      style="height: calc(100% - 45px)"
      :style="{ width: windowWidth - 260 + 'px' }"
      x-scrollable
    >
      <slot name="default" />
    </n-scrollbar>
  </div>
</template>
<script setup lang="ts">
  import { useApp } from '@/hooks/useApp';

  defineProps<{
    title: string;
  }>();
  const { windowWidth } = useApp();
</script>
<style lang="scss" scoped>
  .container-layout {
    height: 100%;
    &-title {
      height: 25px;
      font-weight: bold;
      font-size: 20px;
      color: var(--jm-accent-7);
      margin-bottom: 30px;
    }
  }
</style>
