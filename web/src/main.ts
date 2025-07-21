import { createApp } from 'vue';
import '@/style/index.scss';
import App from './App.vue';
import i18n from '@/lang';
import IconFont from '@/components/IconFont.vue';
const app = createApp(App);
app.component('SvgIcon', IconFont);
app.use(i18n);
app.mount('#app');
