<template>
  <div>
    <div class="active-title">
      {{ $t('授权系统享不中断最佳体验') }}
    </div>
    <div class="active-tip">
      {{
        $t(
          '产品密钥应该在GMSSH销售方或经销方发送给你的电子邮件中或者销售网站上'
        )
      }}
    </div>
    <n-input
      ref="input"
      v-model:value="code"
      :autofocus="true"
      spellcheck="false"
      :placeholder="$t('输入32位授权码')"
      maxlength="32"
      clearable
    />
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, nextTick } from 'vue';

  const code = ref('');
  defineExpose({
    code,
  });
  const input = ref();
  onMounted(() => {
    nextTick(() => {
      input.value.focus();
    });
  });
</script>

<style lang="scss" scoped>
  .active-title {
    font-weight: bold;
    font-size: 16px;
    color: var(--jm-accent-7);
  }
  .active-tip {
    font-weight: 400;
    font-size: 12px;
    color: var(--jm-accent-5);
    margin-top: 10px;
    margin-bottom: 20px;
  }
</style>
