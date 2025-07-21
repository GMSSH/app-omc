<template>
  <n-tooltip v-if="row.disable == '1'" trigger="hover">
    <template #trigger>
      <svg-icon
        icon="icon-recover"
        color="var(--jm-accent-7)"
        hover-color="var(--jm-primary-1)"
        font-size="18"
        class="icon"
        @click="clickFn"
      />
    </template>
    {{ $t('恢复') }}
  </n-tooltip>
  <n-tooltip v-else trigger="hover">
    <template #trigger>
      <svg-icon
        color="var(--jm-accent-7)"
        hover-color="var(--jm-primary-1)"
        icon="icon-shanchu"
        font-size="18"
        class="icon"
        @click="clickFn"
      />
    </template>
    {{ $t('删除') }}
  </n-tooltip>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n';
  import { SysUser } from '@/api/type';
  const i18n = useI18n();

  const { row, clickFn } = defineProps<{
    row: SysUser;
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
