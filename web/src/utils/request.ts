import naiveui from '@/utils/naiveui';
import { Result } from '@/api/type';
const request = <T = Result>(
  url: string,
  data: { [key: string]: any } = {}
): Promise<T> => {
  return new Promise((resolve, reject) => {
    return window.$gm
      .request<Result>(url, {
        method: 'post',
        data: {
          version: window.$gm.version,
          transport: 'socket',
          params: {
            lang: window.$gm.lang,
            ...data,
          },
        },
      })
      .then((res) => {
        if (res.code == 200000) {
          if (res?.data?.code == 200) {
            resolve(res.data as T);
          } else if (res?.data?.code == 206) {
            window.$gm.openShell({
              arr: [res.data.data],
            });
            resolve(res.data as T);
          } else {
            reject(res.data);
            naiveui.message.error(res?.data?.msg || '请求失败');
          }
        } else {
          reject(res);
        }
      })
      .catch((err) => {
        reject(err);
        naiveui.message.error('请求失败');
      });
  });
};
export default request;
