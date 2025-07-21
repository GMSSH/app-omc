import { createI18n } from 'vue-i18n';
import zhCN from './zh-CN';
import en from './en';
import { locale } from '@/utils';

const lang = locale === 'zh-CN' ? 'zhCN' : 'en';
const i18n = createI18n({
  legacy: false,
  locale: lang,
  globalInjection: true, // 全局注册$t方法
  messages: {
    zhCN: zhCN,
    en: en,
  },
});

export default i18n;
