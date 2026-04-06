<template>
  <div class="yuji-editor">
    <!-- Hero 区域 -->
    <div class="form-section">
      <h3>Hero 区域</h3>
      <div class="form-row">
        <div class="form-group">
          <label>版本号</label>
          <input v-model="content.hero.version" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>产品名称</label>
          <input v-model="content.hero.title" type="text" @input="emitUpdate" />
        </div>
      </div>
      <div class="form-group">
        <label>副标题</label>
        <input v-model="content.hero.subtitle" type="text" @input="emitUpdate" />
      </div>
      
      <div class="sub-section">
        <h4>统计指标</h4>
        <div class="metrics-list">
          <div v-for="(metric, index) in content.hero.metrics" :key="index" class="metric-item">
            <input v-model="metric.value" placeholder="数值" class="metric-value" @input="emitUpdate" />
            <input v-model="metric.label" placeholder="标签" @input="emitUpdate" />
            <button class="remove-btn small" @click="removeMetric(index)">×</button>
          </div>
        </div>
        <button class="add-btn" @click="addMetric">+ 添加指标</button>
      </div>
    </div>

    <!-- 功能特性 -->
    <div class="form-section">
      <h3>功能特性</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sectionTitles.features" type="text" @input="emitUpdate" />
      </div>
      <div class="features-list">
        <div v-for="(feature, index) in content.features" :key="index" class="feature-card">
          <div class="card-header">
            <span>{{ feature.title || `特性 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeFeature(index)">×</button>
          </div>
          <input v-model="feature.title" placeholder="特性标题" @input="emitUpdate" />
          <textarea v-model="feature.description" placeholder="特性描述" rows="3" @input="emitUpdate"></textarea>
          <div class="sub-field">
            <label>标签（逗号分隔）</label>
            <input 
              :value="feature.tags?.join(', ')" 
              @input="updateFeatureTags(index, $event.target.value)"
              placeholder="Vue 3, Rust, WebSocket"
            />
          </div>
        </div>
      </div>
      <button class="add-btn" @click="addFeature">+ 添加特性</button>
    </div>

    <!-- 核心亮点 -->
    <div class="form-section">
      <h3>核心亮点</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sectionTitles.highlights" type="text" @input="emitUpdate" />
      </div>
      <div class="highlights-list">
        <div v-for="(highlight, index) in content.highlights" :key="index" class="highlight-item">
          <span class="check-icon">✓</span>
          <input v-model="content.highlights[index]" placeholder="亮点内容" @input="emitUpdate" />
          <button class="remove-btn small" @click="removeHighlight(index)">×</button>
        </div>
      </div>
      <button class="add-btn" @click="addHighlight">+ 添加亮点</button>
    </div>

    <!-- CTA 区域 -->
    <div class="form-section">
      <h3>CTA 区域</h3>
      <div class="form-row">
        <div class="form-group">
          <label>标题</label>
          <input v-model="content.cta.title" type="text" @input="emitUpdate" />
        </div>
        <div class="form-group">
          <label>链接</label>
          <input v-model="content.cta.link" type="text" @input="emitUpdate" />
        </div>
      </div>
      <div class="form-group">
        <label>按钮文字</label>
        <input v-model="content.cta.buttonText" type="text" @input="emitUpdate" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const defaultContent = {
  hero: { version: '', title: '', subtitle: '', metrics: [] },
  features: [],
  highlights: [],
  sectionTitles: { features: '', highlights: '' },
  cta: { title: '', link: '', buttonText: '' }
}

const content = reactive({ ...defaultContent })

onMounted(() => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...props.modelValue })))
})

watch(() => props.modelValue, (newVal) => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...newVal })))
}, { deep: true })

function emitUpdate() {
  emit('update:modelValue', JSON.parse(JSON.stringify(content)))
}

function addMetric() {
  if (!content.hero.metrics) content.hero.metrics = []
  content.hero.metrics.push({ value: '', label: '' })
  emitUpdate()
}

function removeMetric(index) {
  content.hero.metrics.splice(index, 1)
  emitUpdate()
}

function addFeature() {
  content.features.push({ title: '', description: '', tags: [] })
  emitUpdate()
}

function removeFeature(index) {
  content.features.splice(index, 1)
  emitUpdate()
}

function updateFeatureTags(index, value) {
  content.features[index].tags = value.split(',').map(s => s.trim()).filter(Boolean)
  emitUpdate()
}

function addHighlight() {
  content.highlights.push('')
  emitUpdate()
}

function removeHighlight(index) {
  content.highlights.splice(index, 1)
  emitUpdate()
}
</script>

<style scoped>
.yuji-editor {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  padding: 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
}

.form-section h3 {
  margin: 0 0 20px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-section h3::before {
  content: '';
  width: 4px;
  height: 16px;
  background: var(--primary);
  border-radius: 2px;
}

.sub-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--panel-border);
}

.sub-section h4 {
  margin: 0 0 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--muted);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

.form-group input {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
}

.metrics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
}

.metric-item input {
  padding: 8px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.metric-value {
  width: 80px;
  font-weight: 600;
  color: var(--primary) !important;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.feature-card {
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.feature-card input,
.feature-card textarea {
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.feature-card input:focus,
.feature-card textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.sub-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sub-field label {
  font-size: 12px;
  color: var(--muted);
}

.highlights-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.check-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(121, 168, 255, 0.2);
  display: grid;
  place-items: center;
  font-size: 12px;
  color: var(--primary);
  flex-shrink: 0;
}

.highlight-item input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.highlight-item input:focus {
  outline: none;
  border-color: var(--primary);
}

.add-btn {
  padding: 10px 20px;
  border: 1px dashed var(--panel-border);
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.remove-btn.small {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
  font-size: 14px;
  cursor: pointer;
  flex-shrink: 0;
}

.remove-btn.small:hover {
  background: rgba(255, 100, 100, 0.2);
}
</style>
