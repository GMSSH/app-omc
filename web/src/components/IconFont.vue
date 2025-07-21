<template>
  <svg
    :class="className"
    :height="fontSize"
    :width="fontSize"
    aria-hidden="true"
  >
    <use :fill="color" :xlink:href="`#${icon}`" />
  </svg>
</template>

<script>
  import { defineComponent } from 'vue';
  import '@/utils/iconfont.js';

  export default defineComponent({
    props: {
      class: String,
      icon: String, // 需要添加的字体图标类
      color: {
        // 图标颜色
        type: String,
        default: 'rgba(81, 88, 111, 1)',
      },
      fontSize: {
        // 图标大小
        type: [String, Number],
        default: 16,
      },
    },
    computed: {
      className() {
        return `icon ${this.class}`.split(' ');
      },
    },
  });
</script>

<style scoped>
  .icon {
    vertical-align: -0.15em;
    fill: currentColor;
    overflow: hidden;
  }
  svg {
    outline: none; /* 移除默认 outline */
  }
</style>
