<template>
  <n-tooltip v-if="row.is_login == '1'" trigger="hover">
    <template #trigger>
      <svg-icon
        icon="icon-forbiddenLogin"
        color="var(--jm-accent-7)"
        hover-color="var(--jm-primary-1)"
        font-size="18"
        @click="clickFn"
      />
    </template>
    {{ $t('禁止登录') }}
  </n-tooltip>
  <n-tooltip v-else trigger="hover">
    <template #trigger>
      <svg-icon
        icon="icon-allowLogin"
        color="var(--jm-accent-7)"
        hover-color="var(--jm-primary-1)"
        font-size="18"
        @click="clickFn"
      />
    </template>
    {{ $t('允许登录') }}
  </n-tooltip>
</template>

<script setup lang="ts">
  import { SysUser } from '@/api/type';

  const { row, clickFn } = defineProps<{
    row: SysUser;
    clickFn: () => void;
  }>();
</script>

<style scoped lang="scss">
  svg {
    cursor: pointer;
  }
</style>
