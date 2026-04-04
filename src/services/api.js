import { defaultSiteConfig } from '../data/defaultConfig.js';

const CONFIG_KEY = 'xingyu_site_config';

export const api = {
  // 获取全站配置
  getSiteConfig() {
    return new Promise((resolve) => {
      // 模拟网络延迟
      setTimeout(() => {
        const localData = localStorage.getItem(CONFIG_KEY);
        if (localData) {
          try {
            resolve(JSON.parse(localData));
          } catch (e) {
            resolve(defaultSiteConfig);
          }
        } else {
          resolve(defaultSiteConfig);
        }
      }, 300);
    });
  },

  // 更新全站配置
  updateSiteConfig(newConfig) {
    return new Promise((resolve) => {
      setTimeout(() => {
        localStorage.setItem(CONFIG_KEY, JSON.stringify(newConfig));
        resolve({ success: true, message: '配置保存成功' });
      }, 500);
    });
  },

  // 恢复默认配置
  resetSiteConfig() {
    return new Promise((resolve) => {
      setTimeout(() => {
        localStorage.removeItem(CONFIG_KEY);
        resolve({ success: true, message: '已恢复默认配置' });
      }, 300);
    });
  }
};
