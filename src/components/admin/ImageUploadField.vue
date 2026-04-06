<template>
  <div class="image-upload-field">
    <div class="field-head">
      <label>{{ label }}</label>
      <span v-if="hint" class="field-hint">{{ hint }}</span>
    </div>

    <div class="upload-panel">
      <div class="preview-box">
        <img v-if="modelValue" :src="modelValue" :alt="label" class="preview-image" />
        <div v-else class="preview-placeholder">暂无图片</div>
      </div>

      <div class="upload-actions">
        <div class="action-row">
          <button class="upload-btn" type="button" :disabled="uploading" @click="openFileDialog">
            {{ uploading ? '上传中...' : '上传图片' }}
          </button>
          <button v-if="modelValue" class="clear-btn" type="button" @click="clearImage">
            清除
          </button>
        </div>

        <input
          ref="fileInput"
          class="hidden-input"
          type="file"
          accept="image/png,image/jpeg,image/jpg,image/gif,image/webp"
          @change="handleFileChange"
        />

        <input
          :value="modelValue"
          class="url-input"
          type="text"
          placeholder="或直接填写图片 URL"
          @input="updateUrl"
        />

        <span v-if="errorMessage" class="error-text">{{ errorMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '../../services/api.js'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: '图片'
  },
  hint: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const uploading = ref(false)
const errorMessage = ref('')

function openFileDialog() {
  fileInput.value?.click()
}

async function handleFileChange(event) {
  const file = event.target.files?.[0]
  if (!file) return

  errorMessage.value = ''
  uploading.value = true

  try {
    const result = await api.uploadImage(file)
    emit('update:modelValue', result.url)
  } catch (error) {
    errorMessage.value = error.message || '图片上传失败'
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

function clearImage() {
  emit('update:modelValue', '')
}

function updateUrl(event) {
  emit('update:modelValue', event.target.value)
}
</script>

<style scoped>
.image-upload-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
  container-type: inline-size;
}

.field-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.field-head label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

.field-hint {
  font-size: 12px;
  color: var(--muted);
}

.upload-panel {
  display: grid;
  grid-template-columns: minmax(0, 140px) minmax(0, 1fr);
  gap: 14px;
  align-items: start;
}

.preview-box {
  width: 100%;
  max-width: 140px;
  height: 140px;
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.25);
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  color: var(--muted);
  font-size: 12px;
}

.upload-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
}

.action-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.upload-btn,
.clear-btn {
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--panel-border);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s;
  max-width: 100%;
}

.upload-btn:hover:not(:disabled),
.clear-btn:hover {
  border-color: var(--primary);
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.url-input {
  width: 100%;
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
  box-sizing: border-box;
}

.url-input:focus {
  outline: none;
  border-color: var(--primary);
}

.error-text {
  font-size: 12px;
  color: #ff6b6b;
}

.hidden-input {
  display: none;
}

@container (max-width: 440px) {
  .upload-panel {
    grid-template-columns: 1fr;
  }

  .preview-box {
    max-width: none;
    height: 180px;
  }
}
</style>
