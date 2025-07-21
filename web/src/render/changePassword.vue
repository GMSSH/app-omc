<template>
  <n-tooltip trigger="hover">
    <template #trigger>
      <svg-icon
        icon="icon-xiugaimima"
        color="var(--jm-accent-7)"
        hover-color="var(--jm-primary-1)"
        font-size="18"
        class="icon"
        @click="clickFn"
      />
    </template>
    {{ $t('修改密码') }}
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
