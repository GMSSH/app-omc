<template>
  <container-layout :title="$t('MFA')">
    <div class="safe">
      <div class="safe-head">
        <svg-icon icon="icon-MFA" color="var(--jm-accent-7)" font-size="24" />

        <div class="safe-head-text">
          <p>{{ $t('MFA二次认证') }}</p>
          <p>{{ $t('登陆时需要使用动态口令进行验证') }}</p>
        </div>
        <n-button
          :color="useRootElementCssVariable('jm-accent-3')"
          :focusable="false"
          @click="bindVisibly = true"
        >
          {{ $t('绑定MFA') }}
        </n-button>
      </div>
      <div class="safe-body">
        <div class="safe-body-title">
          {{ $t('全部MFA') }}
        </div>
        <n-empty v-if="list?.length == 0" :description="$t('暂无数据')" />
        <div class="safe-body-list">
          <div
            v-for="item in list"
            :key="item.uuid"
            class="safe-body-list-item"
          >
            <svg-icon
              icon="icon-yonghu"
              color="var(--jm-accent-7)"
              font-size="24"
            />
            <span class="safe-body-list-item-txt">{{ item.alias }}</span>
            <n-button
              type="primary"
              @click="
                delVisibly = true;
                delItem = item;
              "
            >
              {{ $t('解绑') }}
            </n-button>
          </div>
        </div>
      </div>
    </div>
    <open-mfa-modal v-model:visibly="bindVisibly" @create-update="getList" />
    <del-mfa-modal
      v-model:visibly="delVisibly"
      :item="delItem"
      @on-update="getList"
    />
  </container-layout>
</template>

<script lang="ts" setup>
  import { ref, onActivated } from 'vue';
  import { NButton } from 'naive-ui';
  import ContainerLayout from '@/layout/ContainerLayout.vue';
  import { mfaBindListApi } from '@/api';
  import { MfaItem } from '@/api/type';
  import OpenMfaModal from '@/modal/openMfaModal.vue';
  import DelMfaModal from '@/modal/delMfaModal.vue';
  import { useRootElementCssVariable } from '@/utils';

  onActivated(() => {
    getList();
  });
  const list = ref<MfaItem[]>([]);
  const getList = () => {
    mfaBindListApi().then((res) => {
      list.value = res.data.alias_list || [];
    });
  };
  const delVisibly = ref(false);
  const bindVisibly = ref(false);
  const delItem = ref({} as MfaItem);
</script>

<style lang="scss" scoped>
  .safe {
    &-head {
      padding: 0 20px;
      height: 78px;
      background: var(--jm-accent-1);
      border-radius: 4px;
      @include flex(flex-start);

      &-text {
        margin-left: 20px;
        margin-right: auto;

        p {
          margin: 0;

          &:nth-of-type(1) {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 7px;
            color: var(--jm-accent-7);
          }

          &:nth-of-type(2) {
            font-size: 12px;
            font-weight: 400;
            opacity: 0.7;
            line-height: 12px;
            color: var(--jm-accent-7);
          }
        }
      }
      &-btn {
        background: var(--jm-accent-3);
        color: var(--jm-accent-7);
        --n-border: var(--jm-accent-3) !important
      ;
      }
    }

    &-body {
      background: var(--jm-accent-1);
      border-radius: 4px;
      opacity: 1;
      border-top: none;
      padding-left: 30px;
      padding-top: 20px;
      padding-bottom: 20px;
      box-sizing: border-box;
      margin-top: 10px;
      &-title {
        margin-bottom: 13px;
        font-size: 16px;
        font-weight: normal;
        color: var(--jm-accent-7);
      }

      &-list {
        @include flex(flex-start, center, row, wrap);

        &-item {
          width: 400px;
          height: 80px;
          background: var(--jm-accent-2);
          border-radius: 8px;
          padding-left: 20px;
          padding-right: 30px;
          box-sizing: border-box;
          margin-bottom: 20px;
          margin-right: 20px;
          @include flex(flex-start);

          &-txt {
            width: 275px;
            @include ellipsis();
            font-size: 14px;
            color: var(--jm-accent-7);
            margin-left: 10px;
            margin-right: 10px;
          }
        }
      }
    }
  }
</style>
