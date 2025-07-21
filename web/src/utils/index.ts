import naiveui from '@/utils/naiveui';

export const locale = window.$gm?.lang || 'zh-CN';
/**
 * 生成一个随机字母
 *
 */
function getRandomLetter() {
  const alphabet = 'abcdefghijklmnopqrstuvwxyz';
  const randomIndex = Math.floor(Math.random() * alphabet.length);
  return alphabet[randomIndex];
}

/**
 * 随机字符串
 * 包含大小写字母、数字和特殊符号的字符串
 */
export function generateRandomString() {
  const characters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$^&*()=_~?.,';
  const length = Math.floor(Math.random() * (30 - 16 + 1)) + 16;
  let result = getRandomLetter();
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}
// /**
//  * 函数防抖
//  * @param {Function} func 一段时间后，要调用的函数
//  * @param {number} wait 等待的时间，单位毫秒
//  * @returns {Function} 返回一个防抖动函数
//  */
// export function debounce<T extends (...args: any[]) => any>(
//   func: T,
//   wait: number = 400,
// ): (...args: Parameters<T>) => void {
//   // 设置变量，记录 setTimeout 得到的 id
//   let timerId: ReturnType<typeof setTimeout> | null = null;
//   return (...args: Parameters<T>): void => {
//     if (timerId) {
//       // 如果有值，说明目前正在等待中，清除它
//       clearTimeout(timerId);
//     }
//     // 重新开始计时
//     timerId = setTimeout(() => {
//       func(...args);
//     }, wait);
//   };
// }
/**
 * 复制到剪切板
 */

export const copyToClipboard = (text: string) => {
  // 创建一个文本域
  const textArea = document.createElement('textarea');
  // 隐藏掉这个文本域，使其在页面上不显示
  textArea.style.position = 'fixed';
  textArea.style.visibility = '-10000px';
  // 将需要复制的内容赋值给文本域
  textArea.value = text;
  // 将这个文本域添加到页面上
  document.body.appendChild(textArea);
  // 添加聚焦事件，写了可以鼠标选取要复制的内容
  textArea.focus();
  // 选取文本域内容
  textArea.select();

  if (!document.execCommand('copy')) {
    // 检测浏览器是否支持这个方法
    console.warn('浏览器不支持 document.execCommand("copy")');
    // 复制失败将构造的标签 移除
    document.body.removeChild(textArea);
    return false;
  } else {
    naiveui.message.success(
      window.$gm?.lang === 'en' ? 'Copy successful' : '复制成功'
    );
    // 复制成功后再将构造的标签 移除
    document.body.removeChild(textArea);
    return true;
  }
};

/**
 * 唤起文件选择窗口，并获取选择的文件
 * @returns
 */
export async function getWinFiles() {
  // 创建文件选择元素
  const input = document.createElement('input');
  input.setAttribute('type', 'file');
  input.setAttribute('style', 'display:none');
  input.setAttribute('multiple', 'true'); // 多选
  input.setAttribute('accept', ''); // 文件上传格式限制
  // 将文件选择元素添加到文档中
  document.body.appendChild(input);
  // 触发文件选择元素的点击事件
  input.click();
  // 等待文件选择元素的change事件
  return await new Promise((resolve) => {
    input.addEventListener('change', (e) => {
      const files = (e.target as HTMLInputElement).files || [];
      // 从文档中移除文件选择元素
      document.body.removeChild(input);
      // 抛出附件，并生成附件uid
      resolve(files);
    });
  });
}
/**
 *获取根元素css变量
 * @export
 * @param {string} cssVar css根元素变量
 * @return {string}
 */
export function useRootElementCssVariable(cssVar: string) {
  // 获取根元素
  const root = document.documentElement;

  // 获取计算后的样式
  const rootStyle = getComputedStyle(root);

  // 获取CSS变量的值
  function getCssVariable(variableName: string) {
    // 检查CSS变量是否设置
    const isVar = rootStyle.getPropertyValue(`--${variableName}`);
    if (isVar) {
      return rootStyle.getPropertyValue(`--${variableName}`).trim();
    }

    return '';
  }

  return getCssVariable(cssVar);
}
