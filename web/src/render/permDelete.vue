<template>
  <n-tooltip trigger="hover">
    <template #trigger>
      <svg-icon
        icon="icon-shanchu"
        color="var(--jm-accent-7)"
        hover-color="var(--jm-primary-1)"
        font-size="18"
        class="icon"
        @click="clickFn"
      />
    </template>
    {{ $t('彻底删除') }}
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
  .icon {
    margin-right: 12px;
  }
</style>
