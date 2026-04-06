import { defaultSiteConfig } from '../data/defaultConfig.js';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api';
const TOKEN_KEY = 'xingyu_admin_token';
const SITE_PREVIEW_KEY = 'xingyu_site_preview';
const PAGE_PREVIEW_KEY_PREFIX = 'xingyu_page_preview:';

function normalizeLegacyLink(value) {
  if (typeof value !== 'string') return value;

  const match = value.match(/^\/pages\/([a-z0-9-]+)\.html([?#].*)?$/i);
  if (!match) return value;

  const [, slug, suffix = ''] = match;
  return `/${slug}${suffix}`;
}

function normalizeLegacyData(value) {
  if (Array.isArray(value)) {
    return value.map(normalizeLegacyData);
  }

  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, normalizeLegacyData(item)])
    );
  }

  return normalizeLegacyLink(value);
}

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

function hasWindow() {
  return typeof window !== 'undefined';
}

function getSearchParams() {
  return hasWindow() ? new URLSearchParams(window.location.search) : new URLSearchParams();
}

function readPreviewValue(key) {
  if (!hasWindow()) return null;
  const raw = window.sessionStorage.getItem(key);
  if (!raw) return null;

  try {
    return JSON.parse(raw);
  } catch (error) {
    console.warn('Failed to parse preview data:', error);
    return null;
  }
}

function writePreviewValue(key, value) {
  if (!hasWindow()) return;
  window.sessionStorage.setItem(key, JSON.stringify(value));
}

function removePreviewValue(key) {
  if (!hasWindow()) return;
  window.sessionStorage.removeItem(key);
}

function authHeaders() {
  const token = getToken();
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

async function request(url, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...authHeaders(),
    ...options.headers
  };

  try {
    const response = await fetch(`${API_BASE}${url}`, {
      ...options,
      headers
    });

    if (response.status === 401 || response.status === 422) {
      removeToken();
      // 如果是在浏览器环境中，强制重载页面以返回登录页
      if (typeof window !== 'undefined') {
        window.location.reload();
      }
      throw { status: response.status, message: '登录已过期或凭证无效，请重新登录' };
    }

    const data = await response.json();

    if (!response.ok) {
      throw { status: response.status, message: data.error || '请求失败' };
    }

    return data;
  } catch (error) {
    if (error.status) throw error;
    console.error('API request failed:', error);
    throw { status: 0, message: '网络错误，无法连接到服务器' };
  }
}

export const api = {
  async getSiteConfig() {
    try {
      const params = getSearchParams();
      if (params.get('previewSite') === '1') {
        const preview = readPreviewValue(SITE_PREVIEW_KEY);
        if (preview) return normalizeLegacyData(preview);
      }
      return normalizeLegacyData(await request('/config'));
    } catch (error) {
      console.warn('Failed to fetch config from server, using default:', error);
      return normalizeLegacyData(defaultSiteConfig);
    }
  },

  async getPage(slug) {
    try {
      const params = getSearchParams();
      if (params.get('previewPage') === slug) {
        const preview = readPreviewValue(`${PAGE_PREVIEW_KEY_PREFIX}${slug}`);
        if (preview?.content) {
          return normalizeLegacyData(preview.content);
        }
      }
      const data = await request(`/pages/${slug}`);
      return normalizeLegacyData(data.content);
    } catch (error) {
      console.warn(`Failed to fetch page ${slug}:`, error);
      return null;
    }
  },

  async getAllPages() {
    try {
      return await request('/pages');
    } catch (error) {
      console.warn('Failed to fetch pages:', error);
      return [];
    }
  },

  async login(username, password) {
    const data = await request('/admin/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });

    if (data.token) {
      setToken(data.token);
    }

    return data;
  },

  logout() {
    removeToken();
  },

  isLoggedIn() {
    return !!getToken();
  },

  async getCurrentUser() {
    return await request('/admin/me');
  },

  async updateSiteConfig(config) {
    return await request('/admin/config', {
      method: 'PUT',
      body: JSON.stringify(config)
    });
  },

  async updateConfigSection(key, value) {
    return await request(`/admin/config/${key}`, {
      method: 'PUT',
      body: JSON.stringify(value)
    });
  },

  async getAdminPages() {
    return await request('/admin/pages');
  },

  async getAdminPage(slug) {
    return normalizeLegacyData(await request(`/admin/pages/${slug}`));
  },

  async updatePage(slug, data) {
    return await request(`/admin/pages/${slug}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },

  async createPage(slug, data) {
    return await request('/admin/pages', {
      method: 'POST',
      body: JSON.stringify({ slug, ...data })
    });
  },

  async deletePage(slug) {
    return await request(`/admin/pages/${slug}`, {
      method: 'DELETE'
    });
  },

  async resetPage(slug) {
    return await request(`/admin/pages/${slug}/reset`, {
      method: 'POST'
    });
  },

  async submitApplication(payload) {
    return await request('/applications', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  async getApplications(status = 'all') {
    return await request(`/admin/applications?status=${encodeURIComponent(status)}`);
  },

  async updateApplication(applicationId, payload) {
    return await request(`/admin/applications/${applicationId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    });
  },

  async uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/admin/upload-image`, {
        method: 'POST',
        headers: {
          ...authHeaders()
        },
        body: formData
      });

      if (response.status === 401 || response.status === 422) {
        removeToken();
        if (typeof window !== 'undefined') {
          window.location.reload();
        }
        throw { status: response.status, message: '登录已过期或凭证无效，请重新登录' };
      }

      const data = await response.json();

      if (!response.ok) {
        throw { status: response.status, message: data.error || '图片上传失败' };
      }

      return data;
    } catch (error) {
      if (error.status) throw error;
      throw { status: 0, message: '网络错误，图片上传失败' };
    }
  },

  async exportAll() {
    const data = await request('/admin/export');
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `xingyu-backup-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    return { success: true, message: '数据已导出' };
  },

  async importAll(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const data = JSON.parse(e.target.result);
          const result = await request('/admin/import', {
            method: 'POST',
            body: JSON.stringify(data)
          });
          resolve(result);
        } catch (err) {
          reject({ success: false, message: '导入失败: ' + err.message });
        }
      };
      reader.onerror = () => reject({ success: false, message: '文件读取失败' });
      reader.readAsText(file);
    });
  },

  async resetAllContent() {
    return await request('/admin/reset-all', {
      method: 'POST'
    });
  },

  async resetSiteConfig() {
    return await api.resetAllContent();
  },

  getDefaultConfig() {
    return normalizeLegacyData(JSON.parse(JSON.stringify(defaultSiteConfig)));
  },

  setSitePreview(config) {
    writePreviewValue(SITE_PREVIEW_KEY, config);
  },

  clearSitePreview() {
    removePreviewValue(SITE_PREVIEW_KEY);
  },

  setPagePreview(slug, page) {
    writePreviewValue(`${PAGE_PREVIEW_KEY_PREFIX}${slug}`, page);
  },

  clearPagePreview(slug) {
    removePreviewValue(`${PAGE_PREVIEW_KEY_PREFIX}${slug}`);
  }
};
