<template>
  <n-config-provider
    style="height: 100%"
    :theme="theme"
    :theme-overrides="themeOverrides"
    :locale="localeSetting.locale"
    :date-locale="localeSetting.dateLocale"
  >
    <n-spin class="omc-spin" :show="loading" style="height: 100%; flex: 1">
      <div class="omc-container">
        <side-layout
          v-model:active-index="activeIndex"
          style="margin-left: 10px; margin-right: 30px"
          :list="menuList"
        />
        <div class="omc-container-main">
          <keep-alive>
            <component
              :is="loading ? 'div' : menuList[activeIndex].component"
            />
          </keep-alive>
        </div>
      </div>
    </n-spin>
  </n-config-provider>
</template>
<script setup lang="ts">
  import { computed, ref } from 'vue';
  import {
    darkTheme,
    dateEnUS,
    dateZhCN,
    enUS,
    NConfigProvider,
    zhCN,
  } from 'naive-ui';
  import { locale } from '@/utils';
  import SideLayout from '@/layout/SideLayout.vue';
  import { useI18n } from 'vue-i18n';

  import ItemUser from '@/views/itemUser.vue';
  import ItemSsh from '@/views/itemSsh.vue';
  import ItemLog from '@/views/itemLog.vue';
  import ItemDns from '@/views/itemDns.vue';
  import ItemSwap from '@/views/itemSwap.vue';
  import ItemTime from '@/views/itemTime.vue';
  import ItemStorage from '@/views/itemStorage.vue';
  import ItemMFA from '@/views/itemSafe.vue';

  import userImg from '@/assets/user.png';
  import sshImg from '@/assets/ssh.png';
  import logImg from '@/assets/log.png';
  import dnsImg from '@/assets/dns.png';
  import timeImg from '@/assets/swap.png';
  import swapImg from '@/assets/time.png';
  import storageImg from '@/assets/storage.png';
  import mfaImg from '@/assets/mfa.png';

  // 国际化
  const localeSetting = computed(() => {
    let lang = {
      locale: zhCN,
      dateLocale: dateZhCN,
    };
    if (locale === 'en') {
      lang = {
        locale: enUS,
        dateLocale: dateEnUS,
      };
    }
    return lang;
  });
  const theme = ref(darkTheme);
  const themeOverrides = window?.$gm?.naiveUiTheme;

  const i18n = useI18n();

  const menuList = [
    ...(window.$gm.isExperiencesServer
      ? []
      : [
          {
            url: userImg,
            name: i18n.t('用户管理'),
            component: ItemUser,
          },
          {
            url: sshImg,
            name: i18n.t('SSH管理'),
            component: ItemSsh,
          },
        ]),
    {
      url: logImg,
      name: i18n.t('系统日志'),
      component: ItemLog,
    },
    {
      url: dnsImg,
      name: i18n.t('DNS设置'),
      component: ItemDns,
    },
    // Swap/虚拟内存仅在非体验服务器环境下显示
    ...(window.$gm.isExperiencesServer
      ? []
      : [
          {
            url: swapImg,
            name: i18n.t('Swap/虚拟内存'),
            component: ItemSwap,
          },
        ]),
    {
      url: timeImg,
      name: i18n.t('时区设置'),
      component: ItemTime,
    },
    {
      url: storageImg,
      name: i18n.t('内存盘'),
      component: ItemStorage,
    },
    ...(window.$gm.isExperiencesServer
      ? []
      : [
          {
            url: mfaImg,
            name: i18n.t('MFA'),
            component: ItemMFA,
          },
        ]),
  ];
  const loading = ref(true);
  const activeIndex = ref(0);

  // 初始化
  window.$gm.init().then(() => {
    loading.value = false;
  });
</script>
<style lang="scss" scoped>
  .omc-container {
    height: 100%;
    box-sizing: border-box;
    @include flex(start, flex-start);
    padding: 20px 0;
    overflow: hidden;
    &-main {
      height: 100%;
      margin-right: 30px;
    }
  }
</style>
<style lang="scss">
  .omc-spin {
    > .n-spin-content {
      height: 100%;
    }
  }
</style>
