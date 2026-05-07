<template>
  <div class="editor-section">
    <div class="editor-group">
      <h3 class="group-title">网站图标</h3>

      <ImageUploadField
        :model-value="modelValue.siteIcon || ''"
        label="网站图标"
        hint="上传后将显示在浏览器标签页和导航栏，建议使用正方形 PNG 或 SVG"
        @update:model-value="val => update('siteIcon', val)"
      />
    </div>

    <div class="editor-group">
      <h3 class="group-title">飞书通知</h3>

      <div class="form-field">
        <label class="field-label">飞书通知方式</label>
        <select
          class="field-input"
          :value="modelValue.feishuMode || 'app'"
          @change="update('feishuMode', $event.target.value)"
        >
          <option value="webhook">Webhook 机器人</option>
          <option value="app">应用机器人</option>
        </select>
        <p class="field-help">
          Webhook 适合静态通知；应用机器人支持卡片回调和原卡片更新。
        </p>
      </div>

      <div class="form-field">
        <label class="field-label">飞书群机器人 Webhook 地址</label>
        <input
          type="text"
          class="field-input"
          :value="modelValue.feishuWebhookUrl || ''"
          @input="update('feishuWebhookUrl', $event.target.value)"
          placeholder="https://open.feishu.cn/open-apis/bot/v2/hook/..."
        >
        <p class="field-help">
          选择 Webhook 模式时使用。
        </p>
      </div>

      <div class="form-field">
        <label class="field-label">飞书应用群 Chat ID</label>
        <input
          type="text"
          class="field-input"
          :value="modelValue.feishuAppChatId || ''"
          @input="update('feishuAppChatId', $event.target.value)"
          placeholder="oc_xxxxxxxxx"
        >
        <p class="field-help">
          选择应用机器人模式时使用。应用凭据和回调 token 仍从后端 .env 读取。
        </p>
      </div>

      <div class="form-field">
        <label class="field-label">卡片回调地址（填到飞书开放平台）</label>
        <p class="field-readonly">
          {{ callbackHint }}
        </p>
        <p class="field-help">
          在飞书应用后台订阅「卡片回传交互」(<code>card.action.trigger</code>)，请求地址填上述 URL；需公网 HTTPS。
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ImageUploadField from './ImageUploadField.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const callbackHint = computed(() => {
  const raw = (import.meta.env.VITE_API_BASE || '').trim() || 'http://localhost:5000/api'
  if (/^https?:\/\//i.test(raw)) {
    const origin = raw.replace(/\/api\/?$/i, '')
    return `${origin}/api/feishu/cards/callback`
  }
  if (typeof window !== 'undefined') {
    return `${window.location.origin}/api/feishu/cards/callback`
  }
  return '/api/feishu/cards/callback'
})

function update(key, value) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}
</script>

<style scoped>
.editor-section {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.editor-group {
  background: rgba(12, 24, 42, 0.5);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  padding: 24px;
}

.group-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: var(--text);
}

.form-field {
  margin-bottom: 16px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  margin-bottom: 8px;
}

.field-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text);
  font-size: 14px;
  transition: border-color 0.2s, background 0.2s;
  box-sizing: border-box;
}

.field-input:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(121, 168, 255, 0.05);
}

.field-help {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.6;
}

.field-readonly {
  margin: 0;
  padding: 12px 14px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--panel-border);
  font-size: 13px;
  color: var(--primary);
  word-break: break-all;
}

.field-help code {
  font-size: 11px;
  color: var(--muted);
}
</style>
