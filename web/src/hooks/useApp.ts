import { ref } from 'vue';

export function useApp() {
  const rectSize = window.$gm?.getRectSize();
  const windowWidth = ref(rectSize?.width);
  const windowHeight = ref(rectSize?.height);
  // 监听外部窗口大小变化
  window.$gm.childRectListener((res) => {
    const { width, height } = res;
    windowWidth.value = width;
    windowHeight.value = height;
  });
  return {
    windowHeight,
    windowWidth,
  };
}
