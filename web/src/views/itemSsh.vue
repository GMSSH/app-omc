<template>
  <container-layout :title="$t('SSH管理')">
    <div class="ssh">
      <div class="ssh-tabs">
        <div
          class="ssh-tabs-item"
          :class="{ active: type === typeEnum.info }"
          @click="type = typeEnum.info"
        >
          {{ $t('基础设置') }}
        </div>
        <div
          class="ssh-tabs-item"
          :class="{ active: type === typeEnum.cert }"
          @click="type = typeEnum.cert"
        >
          {{ $t('证书管理') }}
        </div>
      </div>
      <ssh-info v-show="type === typeEnum.info" />
      <ssh-cert v-show="type === typeEnum.cert" />
    </div>
  </container-layout>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import sshInfo from '@/views/sshInfo.vue';
  import sshCert from '@/views/sshCert.vue';
  import ContainerLayout from '@/layout/ContainerLayout.vue';

  enum typeEnum {
    info = 1, // 基础设置
    cert = 2, // 证书管理
  }

  const type = ref(typeEnum.info);
</script>

<style lang="scss" scoped>
  .ssh {
    &-tabs {
      @include flex(start);

      &-item {
        box-sizing: border-box;
        width: 120px;
        height: 34px;
        padding: 0 24px;
        border: 1px solid var(--jm-accent-3);
        line-height: 34px;
        text-align: center;
        font-weight: 400;
        font-size: 14px;
        color: var(--jm-accent-7);
        cursor: pointer;
        transition: all 0.3s;
        &:nth-of-type(1) {
          border-radius: 4px 0 0 4px;
        }
        &:nth-of-type(2) {
          border-radius: 0 4px 4px 0;
        }
        &.active {
          background: var(--jm-accent-3);
        }
      }
    }
  }

  .modal-textarea {
    :deep(.n-input-wrapper) {
      resize: none !important;
    }
  }

  .handle-text {
    text-align: center;
    padding: 2px 0;
  }
</style>
