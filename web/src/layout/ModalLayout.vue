<template>
  <n-modal
    :show="show"
    :auto-focus="autoFocus"
    @after-enter="emit('after-enter')"
    @after-leave="emit('after-leave')"
  >
    <slot />
  </n-modal>
</template>
<script setup lang="ts">
  defineProps<{
    show: boolean;
    autoFocus?: boolean;
  }>();

  const emit = defineEmits(['after-enter', 'after-leave']);
</script>
<style scoped lang="scss">
  .modal-layout {
    position: fixed;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    background-color: var(--jm-theme);
    z-index: 2000;

    display: flex;
    justify-content: center;
    align-items: center;
    &-content {
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }

  .modal-fade-enter-active,
  .modal-fade-leave-active {
    transition: opacity 0.3s ease;
  }

  .modal-fade-enter-from,
  .modal-fade-leave-to {
    opacity: 0;
  }
</style>
