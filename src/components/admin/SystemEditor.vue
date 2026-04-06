<template>
  <div class="editor-section">
    <div class="editor-group">
      <h3 class="group-title">系统设置</h3>

      <div class="form-field">
        <label class="field-label">飞书群机器人 Webhook 地址</label>
        <input
          type="text"
          class="field-input"
          :value="modelValue.feishuWebhookUrl"
          @input="update('feishuWebhookUrl', $event.target.value)"
          placeholder="https://open.feishu.cn/open-apis/bot/v2/hook/..."
        >
        <p class="field-help">
          用于“加入我们”报名后推送通知到飞书群。
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

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
</style>
