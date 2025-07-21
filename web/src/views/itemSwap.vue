<template>
  <container-layout :title="$t('Swap/虚拟内存')">
    <div class="swap">
      <div class="swap-container">
        <div class="swap-container-disk">
          <img src="@/assets/cp.png" />
          <div class="swap-container-disk-right">
            <p class="swap-container-disk-right-title">
              {{ $t('Swap/虚拟内存') }}
            </p>
            <div class="swap-container-disk-right-progress">
              <div
                :style="{
                  width: (formState.used / formState.total) * 100 + '%',
                }"
                class="swap-container-disk-right-progress-fill"
              />
            </div>
            <p class="swap-container-disk-right-text">
              {{ $t('总容量') }}: {{ formState.total }} MB，{{ $t('已用') }}:{{
                formState.used
              }}
              MB，{{ $t('可用') }}:{{ formState.free }} MB
            </p>
          </div>
        </div>
        <n-space
          align="center"
          style="padding: 30px; background: var(--jm-accent-1)"
        >
          <n-input-number
            v-model:value="formState.size"
            :placeholder="$t('请输入数字')"
            style="width: 140px"
            clearable
            :min="0"
            :max="10240000"
            :precision="0"
            :show-button="false"
          >
            <template #suffix>
              <div style="color: var(--jm-accent-7); font-size: 12px">MB</div>
            </template>
          </n-input-number>
          <n-button
            type="primary"
            :disabled="!(formState.size > 0 || formState.size === 0)"
            @click="onSave"
          >
            {{ $t('设置') }}
          </n-button>
        </n-space>
        <div style="padding: 0 30px 30px; background: var(--jm-accent-1)">
          <div class="swap-container-str">
            {{
              $t('swap是Linux下的虚拟内存，设置适当的swap可增加服务器稳定性')
            }}
          </div>
          <div class="swap-container-str">
            {{
              $t(
                '建议swap容量在真实内存容量的1.5倍左右，若您的服务器内存大于4GB，可设1-2GB的固定值'
              )
            }}
          </div>
          <div class="swap-container-str">
            {{ $t('swap文件默认保存在/www/swap，设置前请确保磁盘空间够用') }}
          </div>
          <div class="swap-container-str">
            {{ $t('若您不需要swap，请将容量设为0') }}
          </div>
          <div class="swap-container-str">
            {{ $t('OVZ虚拟架构机器不可用此功能') }}
          </div>
        </div>
      </div>
    </div>
  </container-layout>
</template>
<script lang="ts" setup>
  import { onActivated, reactive } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { linuxGetSwapApi, linuxSetSwapApi } from '@/api';
  import naiveui from '@/utils/naiveui';
  import ContainerLayout from '@/layout/ContainerLayout.vue';

  const i18n = useI18n();

  const formState = reactive({
    free: 0,
    size: 0,
    total: 0,
    used: 0,
  });

  const getLoad = async () => {
    const res = await linuxGetSwapApi();
    formState['free'] = res.data['swap'].free;
    formState['size'] = res.data['swap'].size;
    formState['total'] = res.data['swap'].total;
    formState['used'] = res.data['swap'].used;
  };
  onActivated(() => {
    getLoad();
  });
  const onSave = () => {
    naiveui.dialog.info({
      title: i18n.t('通知'),
      content: i18n.t('是否确认修改swap？'),
      positiveText: `${i18n.t('确定')}`,
      negativeText: `${i18n.t('取消')}`,
      class: 'dialog-warning',
      maskClosable: false,
      onPositiveClick: () => {
        linuxSetSwapApi(formState.size.toString()).then((res) => {
          getLoad();
          naiveui.message.success(res.msg);
        });
      },
    });
  };
</script>

<style lang="scss" scoped>
  .swap {
    color: var(--jm-accent-7);
    &-container {
      &-title {
        margin-top: 20px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
      }

      &-disk {
        background: var(--jm-accent-1);
        border-radius: 4px 4px 0 0;
        margin-bottom: 1px;
        @include flex(flex-start);
        padding: 30px;
        white-space: nowrap;
        img {
          width: 50px;
          height: 50px;
        }

        &-right {
          width: 180px;
          margin-left: 10px;

          &-title {
            height: 20px;
            font-size: 14px;
            font-weight: bold;
            //color: #000000;
            line-height: 20px;
            margin: 0;
          }

          &-progress {
            width: 180px;
            height: 16px;
            background: var(--jm-theme);
            border-radius: 4px;
            /* border: 1px solid #dddddd; */
            margin: 6px 0;
            position: relative;

            &-fill {
              height: 18px;
              position: absolute;
              left: -1px;
              top: -1px;
              bottom: 0;
              background: var(--jm-primary-1);
              border-radius: 4px;
            }
          }

          &-text {
            height: 18px;
            font-size: 12px;

            font-weight: 400;
            //color: #555555;
            line-height: 18px;
            margin: 0;
          }
        }
      }

      &-str {
        height: auto;
        padding-left: 15px;
        white-space: normal;
        text-indent: 0;
        display: flex;
        align-items: center;
        @extend .store-dot-str;
        color: var(--jm-accent-5);
        margin: 0 0 10px 0;
        &::before {
          top: 10px;
          left: 0;
        }
      }
    }
  }
</style>
