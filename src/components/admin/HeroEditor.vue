<template>
  <div class="editor-section">
    <div class="editor-group">
      <h3 class="group-title">基本信息</h3>
      
      <div class="form-field">
        <label class="field-label">顶部标签 (Eyebrow)</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.eyebrow"
          @input="update('eyebrow', $event.target.value)"
          placeholder="如: XINGYU STUDIO"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">主标题</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.title"
          @input="update('title', $event.target.value)"
          placeholder="社团主标语"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">描述文字</label>
        <textarea 
          class="field-textarea"
          :value="modelValue.description"
          @input="update('description', $event.target.value)"
          placeholder="社团简短介绍"
          rows="3"
        ></textarea>
      </div>
    </div>
    
    <div class="editor-group">
      <div class="group-header">
        <h3 class="group-title">统计数据</h3>
        <button class="add-btn" @click="addStat">+ 添加</button>
      </div>
      
      <div class="stats-list">
        <div 
          v-for="(stat, index) in modelValue.stats" 
          :key="index"
          class="stat-item"
        >
          <input 
            type="text"
            class="stat-value"
            :value="stat.value"
            @input="updateStat(index, 'value', $event.target.value)"
            placeholder="数值"
          >
          <input 
            type="text"
            class="stat-label"
            :value="stat.label"
            @input="updateStat(index, 'label', $event.target.value)"
            placeholder="标签"
          >
          <button class="remove-btn" @click="removeStat(index)" title="删除">×</button>
        </div>
      </div>
    </div>
    
    <div class="editor-group">
      <h3 class="group-title">信号卡片</h3>
      
      <div class="form-field">
        <label class="field-label">卡片顶部文字</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.signalCard?.eyebrow"
          @input="updateSignalCard('eyebrow', $event.target.value)"
          placeholder="如: 协作 · 创造 · 分享"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">卡片标题</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.signalCard?.title"
          @input="updateSignalCard('title', $event.target.value)"
          placeholder="如: 从 0 到 1"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">卡片描述</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.signalCard?.description"
          @input="updateSignalCard('description', $event.target.value)"
          placeholder="如: 产品策划 / 设计实现 / 持续开源"
        >
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

function updateStat(index, key, value) {
  const stats = [...props.modelValue.stats]
  stats[index] = { ...stats[index], [key]: value }
  emit('update:modelValue', { ...props.modelValue, stats })
}

function addStat() {
  const stats = [...props.modelValue.stats, { value: '', label: '' }]
  emit('update:modelValue', { ...props.modelValue, stats })
}

function removeStat(index) {
  const stats = props.modelValue.stats.filter((_, i) => i !== index)
  emit('update:modelValue', { ...props.modelValue, stats })
}

function updateSignalCard(key, value) {
  const signalCard = { ...props.modelValue.signalCard, [key]: value }
  emit('update:modelValue', { ...props.modelValue, signalCard })
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

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.group-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: var(--text);
}

.group-header .group-title {
  margin: 0;
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

.field-input,
.field-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text);
  font-size: 14px;
  transition: border-color 0.2s, background 0.2s;
}

.field-input:focus,
.field-textarea:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(121, 168, 255, 0.05);
}

.field-textarea {
  resize: vertical;
  min-height: 80px;
  line-height: 1.6;
}

.add-btn {
  padding: 8px 16px;
  border: 1px solid var(--primary);
  border-radius: 8px;
  background: transparent;
  color: var(--primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background: rgba(121, 168, 255, 0.1);
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  gap: 12px;
  align-items: center;
}

.stat-value {
  width: 100px;
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text);
  font-size: 14px;
  font-weight: 600;
}

.stat-label {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text);
  font-size: 14px;
}

.stat-value:focus,
.stat-label:focus {
  outline: none;
  border-color: var(--primary);
}

.remove-btn {
  width: 32px;
  height: 32px;
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 8px;
  background: transparent;
  color: #ff6b6b;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 100, 100, 0.1);
}
</style>
