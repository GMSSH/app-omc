<template>
  <div class="menu-list">
    <div
      v-for="(item, index) in list"
      :key="index"
      :class="{ active: index === activeIndex }"
      class="menu-list-item"
      @click="emit('update:activeIndex', index)"
    >
      <div class="square" />
      <img :alt="item.name" :src="item.url" />
      <div>{{ item.name }}</div>
    </div>
  </div>
</template>
<script setup lang="ts">
  defineProps<{
    activeIndex: number;
    list: ({
      name: string;
      url: string;
    } & any)[];
  }>();
  const emit = defineEmits(['update:activeIndex']);
</script>
<style scoped lang="scss">
  .menu-list {
    position: relative;
    box-sizing: border-box;

    &-item {
      width: 200px;
      height: 42px;
      border-radius: 8px;
      margin-bottom: 4px;
      @include flex(flex-start, center);
      transition: background-color 200ms ease-in;

      &:hover {
        background: var(--jm-system-hover-color);
      }

      img {
        width: 20px;
        margin-left: 17px;
        margin-right: 14px;
      }

      div {
        font-size: 14px;
        user-select: none;
        color: rgba(var(--jm-accent-7-rgb), 0.8);
      }

      &.active {
        background: var(--jm-system-hover-color);
        position: relative;
        .square {
          width: 3px;
          height: 20px;
          position: absolute;
          left: 0;
          top: 50%;
          transform: translateY(-50%);
          background: var(--jm-primary-1);
          border-radius: 20px;
        }
      }
    }
  }
</style>
