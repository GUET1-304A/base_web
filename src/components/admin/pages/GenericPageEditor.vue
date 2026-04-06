<template>
  <div class="generic-editor">
    <div class="form-section">
      <h3>页面内容</h3>
      <p class="section-desc">此页面暂无专用编辑器，请使用 JSON 模式编辑</p>
      
      <div class="content-preview">
        <pre>{{ JSON.stringify(modelValue, null, 2).slice(0, 500) }}...</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.generic-editor {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-section {
  padding: 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
}

.form-section h3 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

.section-desc {
  margin: 0 0 16px;
  color: var(--muted);
  font-size: 14px;
}

.content-preview {
  padding: 16px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  overflow: auto;
  max-height: 200px;
}

.content-preview pre {
  margin: 0;
  font-size: 12px;
  font-family: monospace;
  color: var(--muted);
  white-space: pre-wrap;
}
</style>
