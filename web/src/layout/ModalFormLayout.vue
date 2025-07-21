<template>
  <div :style="{ width: width + 'px' }" class="form-modal">
    <n-spin :show="globLoading ? loading : false">
      <div class="form-modal-head">
        <span class="form-modal-head-title">{{ title }}</span>
        <svg-icon
          color="#fff"
          font-size="16"
          style="margin-left: auto; cursor: pointer; margin-right: 10px"
          icon="icon-a-guanbi"
          @click="emit('onCancel')"
        />
      </div>
      <div class="form-modal-body" :style="{ padding: paddingStyle }">
        <slot />
      </div>
      <div v-if="showBtn" class="form-modal-footer">
        <n-button size="small" :disabled="loading" @click="handleCancel">
          {{ $t(cancelText) }}
        </n-button>
        <n-button
          :disabled="loading"
          type="primary"
          size="small"
          text-color="var(--jm-accent-7)"
          @click="handleConfirm"
        >
          {{ $t(confirmText) }}
        </n-button>
      </div>
    </n-spin>
  </div>
</template>
<script lang="ts" setup>
  import { ref } from 'vue';

  defineProps({
    // 标题
    title: {
      type: String,
      default: '',
    },
    // 宽度
    width: {
      type: Number,
      default: 430,
    },
    // 确定按钮文字
    confirmText: {
      type: String,
      default: '确定',
    },
    // 取消按钮文字
    cancelText: {
      type: String,
      default: '取消',
    },
    // 是否显示按钮
    showBtn: {
      type: Boolean,
      default: true,
    },
    // 自定义 padding
    paddingStyle: {
      type: String,
      default: '20px 0 0 0',
    },
    // 全局loading
    globLoading: {
      type: Boolean,
      default: false,
    },
  });
  const loading = ref(false);
  const handleConfirm = async () => {
    loading.value = true; // 开始 loading
    emit('onConfirm', {
      done: () => {
        loading.value = false; // 成功或失败都结束 loading
      },
    });
  };
  const handleCancel = async () => {
    loading.value = true; // 开始 loading
    emit('onCancel', {
      done: () => {
        loading.value = false; // 成功或失败都结束 loading
      },
    });
  };
  // 方法抛出
  const emit = defineEmits(['onConfirm', 'onCancel']);
</script>
<style lang="scss" scoped>
  .form-modal {
    border-radius: 10px;
    /* overflow: hidden; */
    border: 1px solid var(--jm-accent-2);
    &-head {
      @include flex(space-between);
      box-sizing: border-box;
      height: 40px;
      width: 100%;
      backdrop-filter: blur(5px);
      background-color: var(--jm-accent-1);
      border-radius: 10px 10px 0 0;

      &-title {
        height: 40px;
        line-height: 40px;
        margin-left: 10px;
        align-content: center;
        font-size: 14px;
        color: #fff;
      }

      &-icon {
        width: 40px;
        height: 40px;
        @include flex(center);
      }
    }

    &-body {
      background: var(--jm-theme);
      position: relative;
    }

    &-footer {
      height: 60px;
      background: var(--jm-theme);
      @include flex(flex-end);
      border-radius: 0 0 10px 10px;
      :deep(.n-button) {
        margin-right: 20px;
        min-width: 89px;
      }
    }
  }
</style>
