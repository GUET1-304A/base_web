<template>
  <div class="editor-section">
    <div class="editor-group">
      <h3 class="group-title">页脚信息</h3>
      
      <div class="form-field">
        <label class="field-label">品牌名称</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.brand"
          @input="update('brand', $event.target.value)"
          placeholder="如: 星雨作坊 Xingyu Studio"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">标语 (Slogan)</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.slogan"
          @input="update('slogan', $event.target.value)"
          placeholder="如: 以协作连接灵感，以开源延续成长。"
        >
      </div>
    </div>
    
    <div class="preview-group">
      <h3 class="group-title">预览效果</h3>
      <div class="footer-preview">
        <p class="preview-brand">{{ modelValue.brand || '品牌名称' }}</p>
        <p class="preview-slogan">{{ modelValue.slogan || '标语' }}</p>
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

.editor-group,
.preview-group {
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

.form-field:last-child {
  margin-bottom: 0;
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
}

.field-input:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(121, 168, 255, 0.05);
}

.footer-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  border: 1px solid var(--panel-border);
}

.preview-brand {
  margin: 0;
  font-weight: 500;
  color: var(--text);
}

.preview-slogan {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}
</style>
