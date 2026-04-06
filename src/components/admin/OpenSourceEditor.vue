<template>
  <div class="editor-section">
    <div class="editor-group">
      <h3 class="group-title">区块信息</h3>
      
      <div class="form-field">
        <label class="field-label">区块标题</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.title"
          @input="update('title', $event.target.value)"
          placeholder="如: 开源精神"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">区块描述</label>
        <textarea 
          class="field-textarea"
          :value="modelValue.description"
          @input="update('description', $event.target.value)"
          placeholder="区块的简短描述"
          rows="2"
        ></textarea>
      </div>
    </div>
    
    <div class="editor-group">
      <div class="group-header">
        <h3 class="group-title">开源理念卡片</h3>
        <button class="add-btn" @click="addItem">+ 添加卡片</button>
      </div>
      
      <div class="items-list">
        <div 
          v-for="(item, index) in modelValue.items" 
          :key="index"
          class="card-item"
        >
          <div class="card-header">
            <span class="card-number">#{{ index + 1 }}</span>
            <button class="remove-btn" @click="removeItem(index)" title="删除">×</button>
          </div>
          
          <div class="form-field">
            <label class="field-label">卡片标题</label>
            <input 
              type="text"
              class="field-input"
              :value="item.title"
              @input="updateItem(index, 'title', $event.target.value)"
              placeholder="如: 共享知识"
            >
          </div>
          
          <div class="form-field">
            <label class="field-label">卡片内容</label>
            <textarea 
              class="field-textarea"
              :value="item.description"
              @input="updateItem(index, 'description', $event.target.value)"
              placeholder="详细描述"
              rows="2"
            ></textarea>
          </div>
        </div>
      </div>
      
      <div v-if="!modelValue.items?.length" class="empty-state">
        <p>暂无卡片，点击上方按钮添加</p>
      </div>
    </div>
    
    <div class="editor-group">
      <h3 class="group-title">加入横幅 (Join Banner)</h3>
      
      <div class="form-field">
        <label class="field-label">横幅标签</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.joinBanner?.eyebrow"
          @input="updateBanner('eyebrow', $event.target.value)"
          placeholder="如: JOIN US"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">横幅标题</label>
        <textarea 
          class="field-textarea"
          :value="modelValue.joinBanner?.title"
          @input="updateBanner('title', $event.target.value)"
          placeholder="呼吁加入的文案"
          rows="2"
        ></textarea>
      </div>
      
      <div class="form-row">
        <div class="form-field">
          <label class="field-label">主按钮文字</label>
          <input 
            type="text" 
            class="field-input"
            :value="modelValue.joinBanner?.primaryButton?.text"
            @input="updateButton('primaryButton', 'text', $event.target.value)"
            placeholder="如: 加入我们"
          >
        </div>
        <div class="form-field">
          <label class="field-label">主按钮链接</label>
          <input 
            type="text" 
            class="field-input"
            :value="modelValue.joinBanner?.primaryButton?.link"
            @input="updateButton('primaryButton', 'link', $event.target.value)"
            placeholder="/pages/join.html"
          >
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-field">
          <label class="field-label">次按钮文字</label>
          <input 
            type="text" 
            class="field-input"
            :value="modelValue.joinBanner?.secondaryButton?.text"
            @input="updateButton('secondaryButton', 'text', $event.target.value)"
            placeholder="如: 招新信息"
          >
        </div>
        <div class="form-field">
          <label class="field-label">次按钮链接</label>
          <input 
            type="text" 
            class="field-input"
            :value="modelValue.joinBanner?.secondaryButton?.link"
            @input="updateButton('secondaryButton', 'link', $event.target.value)"
            placeholder="/pages/recruitment.html"
          >
        </div>
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

function updateItem(index, key, value) {
  const items = [...(props.modelValue.items || [])]
  items[index] = { ...items[index], [key]: value }
  emit('update:modelValue', { ...props.modelValue, items })
}

function addItem() {
  const items = [...(props.modelValue.items || []), { title: '', description: '' }]
  emit('update:modelValue', { ...props.modelValue, items })
}

function removeItem(index) {
  const items = (props.modelValue.items || []).filter((_, i) => i !== index)
  emit('update:modelValue', { ...props.modelValue, items })
}

function updateBanner(key, value) {
  const joinBanner = { ...props.modelValue.joinBanner, [key]: value }
  emit('update:modelValue', { ...props.modelValue, joinBanner })
}

function updateButton(buttonKey, key, value) {
  const button = { ...(props.modelValue.joinBanner?.[buttonKey] || {}), [key]: value }
  const joinBanner = { ...props.modelValue.joinBanner, [buttonKey]: button }
  emit('update:modelValue', { ...props.modelValue, joinBanner })
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
  margin-bottom: 20px;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.form-row:last-child {
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
  min-height: 60px;
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

.items-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-item {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(121, 168, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-number {
  font-size: 12px;
  font-weight: 600;
  color: var(--primary);
  background: rgba(121, 168, 255, 0.1);
  padding: 4px 10px;
  border-radius: 6px;
}

.remove-btn {
  width: 28px;
  height: 28px;
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 6px;
  background: transparent;
  color: #ff6b6b;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 100, 100, 0.1);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--muted);
}
</style>
