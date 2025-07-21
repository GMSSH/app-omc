<template>
  <n-tooltip trigger="hover">
    <template #trigger>
      <svg-icon
        icon="icon-uninstall"
        color="var(--jm-accent-7)"
        hover-color="#27b2bc"
        font-size="18"
        @click="clickFn"
      />
    </template>
    {{ $t('卸载') }}
  </n-tooltip>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n';
  const i18n = useI18n();

  const { clickFn } = defineProps<{
    clickFn: () => void;
  }>();
</script>

<style scoped lang="scss">
  svg {
    cursor: pointer;
  }
</style>
