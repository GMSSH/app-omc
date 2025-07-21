<template>
  <n-tooltip trigger="hover">
    <template #trigger>
      <svg-icon
        icon="icon-bianji1"
        color="var(--jm-accent-7)"
        hover-color="var(--jm-primary-1)"
        font-size="18"
        class="icon"
        @click="clickFn"
      />
    </template>
    {{ $t('编辑') }}
  </n-tooltip>
</template>

<script setup lang="ts">
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
